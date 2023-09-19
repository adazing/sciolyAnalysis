from config import *
import pandas as pd
import os
import vowpalwabbit
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

model = vowpalwabbit.Workspace("-q :: -f scioly.model --noconstant --l1 1e-6")

def process():
    #checking formatting of config
    error_msg=" is not formatted correctly in config.py"
    if type(num_of_teams)!=int:
        raise Exception("num_of_teams"+error_msg)
    if type(max_team_size)!=int:
        raise Exception("max_team_size"+error_msg)
    if type(available_events)!=list or any([type(event)!=str for event in available_events]):
        raise Exception("available_events"+error_msg)
    if type(events_with_3_members)!=list or any([type(event)!=str for event in events_with_3_members]):
        raise Exception("events_with_3_members"+error_msg)
    if (type(available_members)!=list and available_members!=None):
        raise Exception("available_members"+error_msg)
    if type(available_members)==list:
        if any([type(member)!=str for member in available_members]):
            raise Exception("available_members"+error_msg)
    if type(unavailable_members)!=list or any([type(member)!=str for member in unavailable_members]):
        raise Exception("unavailable_members"+error_msg)
    if type(required_members)!=list or any([type(member)!=str for member in required_members]):
        raise Exception("required_members"+error_msg)
    if (type(grade_distribution)!=list and grade_distribution!=None):
        raise Exception("grade_distribution"+error_msg)
    if type(grade_distribution)==list:
        if any([type(grade)!=int for grade in grade_distribution]) or not sum(grade_distribution)<=max_team_size:
            raise Exception("grade_distribution"+error_msg)
    if type(max_events_per_member)!=int:
        raise Exception("max_events_per_member"+error_msg)
    
    if (type(conflicting_events)!=list and conflicting_events!=None):
        raise Exception("conflicting_events"+error_msg)
    if type(conflicting_events)==list:
        if any([type(event_list)!=list for event_list in conflicting_events]) and any([type(event)!=str for eventlist in conflicting_events for event in eventlist]):
            raise Exception("conflicting_events"+error_msg)
    if type(experience_threshold)!=int:
        raise Exception("experience_threshold"+error_msg)
    if type(total_experience_threshold)!=int:
        raise Exception("total_experience_threshold"+error_msg)

    #gathering competition data info
    members=set() #members in all the competitions so far
    events=set() #events in all the competitions so far
    experience_data={}
    data=np.asarray([])#data to feed into the machine learning model
    
    for competition_name in os.listdir("competitions"):
        f = os.path.join("competitions", competition_name)
        competition=pd.read_csv(f)
        average_event_rank=float(competition.iloc[-1,1])
        num_of_teams_total=float(competition.iloc[-3,1])
        for index, row in competition.iloc[:,range(5)].iterrows():
            if pd.isna(row.iloc[0]):
                break
            else:
                event_score=float(row.iloc[4])
                event=row.iloc[0].replace(" ","_")
                first=row.iloc[1].replace(" ","_")
                second=row.iloc[2].replace(" ","_")
                third=row.iloc[3].replace(" ","_") if not pd.isna(row.iloc[3]) else None
                event_data=str(average_event_rank/num_of_teams_total - event_score/num_of_teams_total)+" | "                
                events.add(event)
                members.add(first)
                if first in experience_data:
                    if event in experience_data[first]:
                        experience_data[first][event]+=1
                    else:
                        experience_data[first][event]=1
                else:
                    experience_data[first]={event:1}
                members.add(second)
                if second in experience_data:
                    if event in experience_data[second]:
                        experience_data[second][event]+=1
                    else:
                        experience_data[second][event]=1
                else:
                    experience_data[second]={event:1}
                if third==None:
                    event_data+=first+":0.5 "+second+":0.5 Event:"+event
                else:
                    if third in experience_data:
                        if event in experience_data[third]:
                            experience_data[third][event]+=1
                        else:
                            experience_data[third][event]=1
                    else:
                        experience_data[second]={event:1}
                    members.add(third)
                    event_data+=first+":"+str(1/3)+" "+second+":"+str(1/3)+" "+third+":"+str(1/3)+" Event:"+event
            data=np.append(data, event_data)
    print(experience_data)
    members=list(members)
    events=list(events)
    return list(members),list(events),experience_data,data

def make_scores(model, data,events, members, experience_data):
    # print(data)
    print(experience_data)
    for i in range(0, 100):
        for e in data:
            model.learn(e)
    scores=[]
    for e in events:
        event_data=[]
        for m in members:
            prediction=model.predict("| "+m+":1.0 Event:"+e)
            # print(list(experience_data[m].values()))
            if sum(list(experience_data[m].values()))<total_experience_threshold:
                prediction=-1.0
            elif e in experience_data[m]:
                if experience_data[m][e]<experience_threshold:
                    prediction=-1.0
            elif experience_threshold>=1:
                prediction=-1.0
            event_data.append(prediction)
            
        scores.append(event_data)
    scores=np.asarray(scores)
    # print(scores)
    return scores

def display_scores(scores, title):
    fig, ax = plt.subplots(figsize=(13,8))         # Sample figsize in inches
    hm = sns.heatmap(data = scores,xticklabels=members,yticklabels=events, linewidths=1,linecolor="g")
    hm.set_title(title)
    hm.set_ylabel("Events")
    hm.set_xlabel("Members")
    plt.subplots_adjust(left=0.2, right=1.0, top=0.95, bottom=0.2)
    # displaying the plotted heatmap
    plt.show()

def is_valid_addition(event, participant, team, experience_data):
    if participant not in members:
        return False
    if experience_data[participant]<5:
        return False
    members=set([x for y in team for x in team[y]])
    member_events={m:{e for e in team if m in team[e]} for m in members}
    if participant in team[event]: # Participant is already in the event
        return False
    if len(members) + len([m for m in required_members if m not in members]) >= max_team_size and participant not in members: # if there are enough members already
        return False
    if len(team[event]) >= 2 + int(event in events_with_3_members): # if there are too many members in the event already
        return False
    if participant in member_events:
        if len(member_events[participant])>=max_events_per_member: # if participant is already in the max amount of events
            return False
    if grade_distribution!=None:
        member_grades={row["Name"].replace(" ","_"):row["Grade"] for index, row in pd.read_csv("grades.csv").iterrows()}
        participant_grade=member_grades[participant]
        if len([m for m in member_grades if member_grades[m]==participant_grade and m in members])>=grade_distribution[participant_grade]: # too many people in the same grade as the participant
            return False
        if participant not in required_members:
            required_members_grade_dist=[0,0,0,0]
            for m in required_members:
                if m not in members:
                    required_members_grade_dist[member_grades[m]]+=1
            if not all([grade_distribution[y]-len([x for x in member_grades if member_grades[x]==y and x in members])>required_members_grade_dist[y] for y in range(4)]):
                return False
    for m in member_events:
        conflicts=[0 for x in conflicting_events]
        for e in member_events[m]:
            if any([x>=2 for x in conflicts]):
                return False
            for x in range(len(conflicting_events)):
                for e in conflicting_events[x]:
                    conflicts[x]+=1
                    break
                
if __name__ == "__main__":
    members, events, experience_data, data = process()
    scores = make_scores(model, data,events, members, experience_data)
    display_scores(scores, "Scores")