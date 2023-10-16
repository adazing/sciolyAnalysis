from config import *
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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
    members=[] #members in all the competitions so far
    events=[] #events in all the competitions so far
    experience_data={}
    score_data={}
    
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
                event=row.iloc[0]
                first=row.iloc[1]
                second=row.iloc[2]
                third=row.iloc[3] if not pd.isna(row.iloc[3]) else None
                event_performance=average_event_rank/num_of_teams_total - event_score/num_of_teams_total            
                events.append(event)
                members.append(first)
                
                if first in experience_data:
                    if event in experience_data[first]:
                        score_data[first][event]+=event_performance*0.5
                        experience_data[first][event]+=1
                    else:
                        score_data[first][event]=event_performance*0.5
                        experience_data[first][event]=1
                else:
                    score_data[first]={event:event_performance*0.5}
                    experience_data[first]={event:1}
                    
                members.append(second)
                
                if second in experience_data:
                    if event in experience_data[second]:
                        score_data[second][event]+=event_performance*0.5
                        experience_data[second][event]+=1
                    else:
                        score_data[second][event]=event_performance*0.5
                        experience_data[second][event]=1
                else:
                    score_data[second]={event : event_performance*0.5}
                    experience_data[second]={event:1}
                if third is not None:
                    if third in experience_data:
                        if event in experience_data[third]:
                            score_data[third][event]+=event_performance/3
                            experience_data[third][event]+=1
                        else:
                            score_data[third][event]=event_performance/3
                            experience_data[third][event]=1
                    else:
                        score_data[third]={event:event_performance/3}
                        experience_data[second]={event:1}
                    members.append(third)
    print(experience_data)
    print(score_data)
    members=list(members)
    events=list(events)
    return list(members),list(events),experience_data,score_data

# def make_scores(model, data,events, members, experience_data):
#     # print(data)
#     print(experience_data)
#     for i in range(0, 100):
#         for e in data:
#             model.learn(e)
#     scores=[]
#     for e in events:
#         event_data=[]
#         for m in members:
#             prediction=model.predict("| "+m+":1.0 Event:"+e)
#             # print(list(experience_data[m].values()))
#             if sum(list(experience_data[m].values()))<total_experience_threshold:
#                 prediction=-1.0
#             elif e in experience_data[m]:
#                 if experience_data[m][e]<experience_threshold:
#                     prediction=-1.0
#             elif experience_threshold>=1:
#                 prediction=-1.0
#             event_data.append(prediction)
            
#         scores.append(event_data)
#     scores=np.asarray(scores)
#     # print(scores)
#     return scores

def display_data(raw_data, title, members, events):
    # print(members)
    # print(events)
    data_min=min([min(raw_data[m].values()) for m in raw_data])
    data=np.asarray([[data_min]*len(members)]*len(events))
    # print(data.shape)
    for m in raw_data:
        for e in raw_data[m]:
            data[events.index(e)][members.index(m)]=raw_data[m][e]
    print(data.shape)
    fig, ax = plt.subplots(figsize=(13,8))         # Sample figsize in inches
    hm = sns.heatmap(data = data,xticklabels=members,yticklabels=events, linewidths=1,linecolor="g")
    hm.set_title(title)
    hm.set_ylabel("Events")
    hm.set_xlabel("Members")
    plt.subplots_adjust(left=0.2, right=1.0, top=0.95, bottom=0.2)
    # displaying the plotted heatmap
    plt.show()

if __name__ == "__main__":
    members, events, experience_data, score_data = process()
    # scores = make_scores(model, data,events, members, experience_data)
    display_data(score_data, "Scores", members, events)
