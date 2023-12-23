from config import *
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import csv
import random
import munkres
import copy
import random

#IDEAS
#make sure not too many build events per person
#make sure not one person has too many events they dont want
#make sure that events get filled out completely!

# NOTE: SOMETIMES GIVES PPL ONLY 1 EVENT - WHY?

def process():
    #checking formatting of config
    # error_msg=" is not formatted correctly in config.py"
    # if type(num_of_teams)!=int:
    #     raise Exception("num_of_teams"+error_msg)
    # if type(max_team_size)!=int:
    #     raise Exception("max_team_size"+error_msg)
    # if type(available_events)!=list or any([type(event)!=str for event in available_events]):
    #     raise Exception("available_events"+error_msg)
    # if type(events_with_3_members)!=list or any([type(event)!=str for event in events_with_3_members]):
    #     raise Exception("events_with_3_members"+error_msg)
    # if (type(available_members)!=list and available_members!=None):
    #     raise Exception("available_members"+error_msg)
    # if type(available_members)==list:
    #     if any([type(member)!=str for member in available_members]):
    #         raise Exception("available_members"+error_msg)
    # if type(unavailable_members)!=list or any([type(member)!=str for member in unavailable_members]):
    #     raise Exception("unavailable_members"+error_msg)
    # if type(required_members)!=list or any([type(member)!=str for member in required_members]):
    #     raise Exception("required_members"+error_msg)
    # if (type(grade_distribution)!=list and grade_distribution!=None):
    #     raise Exception("grade_distribution"+error_msg)
    # if type(grade_distribution)==list:
    #     if any([type(grade)!=int for grade in grade_distribution]) or not sum(grade_distribution)<=max_team_size:
    #         raise Exception("grade_distribution"+error_msg)
    # if type(max_events_per_member)!=int:
    #     raise Exception("max_events_per_member"+error_msg)
    
    # if (type(conflicting_events)!=list and conflicting_events!=None):
    #     raise Exception("conflicting_events"+error_msg)
    # if type(conflicting_events)==list:
    #     if any([type(event_list)!=list for event_list in conflicting_events]) and any([type(event)!=str for eventlist in conflicting_events for event in eventlist]):
    #         raise Exception("conflicting_events"+error_msg)
    # if type(experience_threshold)!=int:
    #     raise Exception("experience_threshold"+error_msg)
    # if type(total_experience_threshold)!=int:
    #     raise Exception("total_experience_threshold"+error_msg)

    #gathering competition data info
    members=set() #members in all the competitions so far
    events=set() #events in all the competitions so far
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
                if event_score < num_of_teams_total: # did not quit
                    # if "Eden Hoong" in [first, second, third]:
                    #     print(event)
                    #     print(first, second, third)
                    #     print(event_performance)
                    event_performance=average_event_rank/num_of_teams_total - event_score/num_of_teams_total
            # else:
            #     event_performance=-0.5
                # print(event_performance)
                # else:
                #     event_performance=average_event_rank/num_of_teams_total - 0.75
                    events.add(event)
                    members.add(first)
                
                    if first in experience_data:
                        if event in experience_data[first]:
                            score_data[first][event]+=event_performance
                            experience_data[first][event]+=1
                        else:
                            score_data[first][event]=event_performance
                            experience_data[first][event]=1
                    else:
                        score_data[first]={event:event_performance}
                        experience_data[first]={event:1}
                    
                    members.add(second)
                
                    if second in experience_data:
                        if event in experience_data[second]:
                            score_data[second][event]+=event_performance
                            experience_data[second][event]+=1
                        else:
                            score_data[second][event]=event_performance
                            experience_data[second][event]=1
                    else:
                        score_data[second]={event : event_performance}
                        experience_data[second]={event:1}
                    if third is not None:
                        if third in experience_data:
                            if event in experience_data[third]:
                                score_data[third][event]+=event_performance
                                experience_data[third][event]+=1
                            else:
                                score_data[third][event]=event_performance
                                experience_data[third][event]=1
                        else:
                            score_data[third]={event:event_performance}
                            experience_data[second]={event:1}
                        members.add(third)

    members=list(members)
    events=list(events)
    return list(members),list(events),experience_data,score_data

def check_if_members_can_fill_rest_of_events(event, member, empty_spots, num_of_required_members_not_yet_on_team, team, team_members):

    if sum(empty_spots)<(num_of_required_members_not_yet_on_team*min_events_per_member):
        return False
    else:
        temp_empty_spots=copy.deepcopy(empty_spots)
        for m in range(num_of_required_members_not_yet_on_team):
            teams_put_on=0
            for e in range(len(temp_empty_spots)):
                if temp_empty_spots[e]>0:
                    temp_empty_spots[e]-=1
                    teams_put_on+=1
                    if teams_put_on>=min_events_per_member:
                        break
            if teams_put_on<min_events_per_member:
                return False
    return True
        
            
        

def is_valid_team_addition(event, member, team):
    events_done_by_member=[x for x in team if member in team[x]]
    team_members=set([x for y in team for x in team[y]])
    empty_spots=[2-len(team[e])+int(e in events_with_3_members) for e in team]
    # member_to_events={p:{e for e in team if p in team[e]} for p in team_members}
    # Check if adding the participant to the event violates the max amount of events a person can have at once.

    if len(events_done_by_member)>=max_events_per_member:
        # print('1 ' + str(events_done_by_member))
        return False
    # too many members in event
    #temporary, should change!
        # elif member=="Joning Wang" and event=="Robot Tour":
        #     return False
    elif (member, event) in required_members_not_on_events:
        return False
    
    elif len(team[event])>=2+int(event in events_with_3_members):
        # print('2')
        return False
    # member is already in the event
    elif member in team[event]:
        # print('3')
        return False
    # all the team members + required members left + 1 (the new member) > max team size (given that member is not already on the team)
    # sees if adding new member makes it so that there is not enough space for required members that are left
    elif len(team_members)+1>max_team_size and member not in team_members:
        return False
    #event space for unwanted events:

    
    
    conflicts=[0 for x in conflicting_events]
    events_done_by_member.append(event)
    for e in events_done_by_member:
        for x in range(len(conflicting_events)):
            if e in conflicting_events[x]:
                conflicts[x]+=1
                # break
        if any([x>=2 for x in conflicts]):
            return False
    return True

def display_data(raw_data, title, members, events):

    data_min=min([min(raw_data[m].values()) for m in raw_data])
    data=np.asarray([[data_min]*len(members)]*len(events))
    for m in raw_data:
        for e in raw_data[m]:
            data[events.index(e)][members.index(m)]=raw_data[m][e]
    fig, ax = plt.subplots(figsize=(13,8))         # Sample figsize in inches
    hm = sns.heatmap(data = data,xticklabels=members,yticklabels=events, linewidths=1,linecolor="g")
    hm.set_title(title)
    hm.set_ylabel("Events")
    hm.set_xlabel("Members")
    plt.subplots_adjust(left=0.2, right=1.0, top=0.95, bottom=0.2)
    # displaying the plotted heatmap
    plt.show()
    return data

def make_fake_preferences_data(members, events):
    with open('fake_preferences.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for m in members:
            writer.writerow(["Name", "Event1", "Event2", "Event3"])
            first_choice=random.choice(events)
            second_choice=random.choice(list(set(events)-{first_choice}))
            third_choice=random.choice(list(set(events)-{first_choice}-{second_choice}))
            print([m, first_choice, second_choice, third_choice])
            writer.writerow([m, first_choice, second_choice, third_choice])

def calculate_preferences_score(team, score_data):
    preferences=pd.read_csv(preferences_file_name)
    empty_spots=[2-len(team[e])+int(e in events_with_3_members) for e in team]
    data={preferences.iloc[m,0]:(preferences.iloc[m, 1:]).tolist() for m in range(preferences.shape[0])}
    worst_preference_amount=preferences.shape[1]
    total_preference_score=0
    for e in team:
        
        for m_1,m_2, wanted_e in member_member_preferences:
            if wanted_e is None or wanted_e==e:
                if {m_1, m_2} <= set(team[e]):
                    total_preference_score-=worst_preference_amount # SHOULD MAKE VARIABLE THAT CHANGES THAT
                elif len(team[e])==1+int(e in events_with_3_members): # 1 more person left in event
                    if m_1 or m_2 in team[e] and (e in preferences[m_1] or e in preferences[m_2]):
                        total_preference_score-=1.0
        
        for m in team[e]:
            if m in score_data:
                if e in score_data[m]:
                    total_preference_score -= score_data[m][e]*worst_preference_amount
                else:
                    total_preference_score += 1
            else:
                total_preference_score += 1
            # print(team)
            if e in data[m]:
                # print("hi1")
                total_preference_score+=data[m].index(e)
            else:
                #calculate similarities
                similar_events = [0 for x in event_types]
                for x in data[m]:
                    for et in range(len(event_types)):
                        if x in event_types[et]:
                            similar_events[et]+=1
                # total_preference_score+=
                idx=0
                for et in range(len(event_types)):
                    if e in event_types[et]:
                        idx=et
                if sum(similar_events)!=0:
                    total_preference_score+=worst_preference_amount-(similar_events[idx]/sum(similar_events))
    total_preference_score+=(worst_preference_amount*2)*sum(empty_spots)*100
    return total_preference_score



def make_preferences_team(events, team_members, score_data):
    best_team = {event: [] for event in events}
    best_score = float('inf')
    
    for m, e in required_members_on_events:
        if m in team_members:
            print("hi")
            best_team[e].append(m)
    
    while True:
        team = copy.deepcopy(best_team)
        
        changed = False

        for event in events:
            for member in list(team_members):
                if is_valid_team_addition(event, member, team):
                    new_team = copy.deepcopy(team)
                    new_team[event].append(member)
                    new_score = calculate_preferences_score(new_team, score_data)

                    if new_score < best_score:
                        # print('hi2')
                        changed = True
                        best_score = new_score
                        best_team = copy.deepcopy(new_team)
        print(best_team)
        if not changed:
            # for x in best_team
            return best_team


def make_teams(score_data, experience_data):
    people_and_skill_level = {}
    preferences = pd.read_csv(preferences_file_name)
    minimum_score=min([(sum(score_data[x].values()))/sum(experience_data[x].values()) for x in score_data]) # finds minimum possible score
    for x in list(set(preferences["Name"])):
        people_and_skill_level[x]=minimum_score
        if x in score_data and sum(experience_data[x].values())>=total_experience_threshold:
            sum_events=sum(score_data[x].values())/sum(experience_data[x].values())
            people_and_skill_level[x]=sum_events
    print(people_and_skill_level)

    
    ranked_people=list(dict(sorted(people_and_skill_level.items(), key=lambda item: item[1], reverse=True)).keys())
    print(ranked_people)

    #officers have priority
    officers_and_skill_level = {o:people_and_skill_level[o] for o in people_and_skill_level if o in officers}
    if max_team_size*num_of_teams<len(ranked_people):
        max_number_included = max_team_size*num_of_teams
    else:
        max_number_included = len(ranked_people)
    #officers have priority
    ranked_officers = list(dict(sorted(officers_and_skill_level.items(), key=lambda item: item[1], reverse=True)).keys())
    ranked_people = ranked_officers + [m for m in ranked_people if m not in officers]
    
    required_members_and_skill_level = {r:people_and_skill_level[r] for r in people_and_skill_level if r in required_members}
    required_members_not_yet_on_team= [r for r in list(dict(sorted(required_members_and_skill_level.items(), key=lambda item: item[1], reverse=True)).keys()) if r in ranked_people[max_number_included:]]
    if required_members_not_yet_on_team!=[]:
        for i, m in reversed(list(enumerate(ranked_people[:max_number_included]))):
            if m not in required_members and m not in officers:
                ranked_people[i]=required_members_not_yet_on_team.pop()
                if required_members_not_yet_on_team==[]:
                    break
    print(ranked_people)
    teams=[]
    team_members_list=[]
    for t in range(num_of_teams):
        if len(ranked_people)>=max_team_size:
            team_members = ranked_people[:max_team_size]
            ranked_people = ranked_people[max_team_size:]
        else:
            team_members=ranked_people
            ranked_people = []
        team=make_preferences_team(available_events, team_members, score_data)
        teams.append(team)
        team_members_list.append(team_members)
    print("HIII")
    print(team_members_list)
    return teams, team_members_list
        
def make_team_csv_files(teams):
    folder_path="teams"
    os.mkdir(folder_path)
    for x in range(len(teams)):
        with open(os.path.join(folder_path, "team"+str(x)+".csv"), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Event", "Person1", "Person2", "Person3"])
            for e in teams[x]:
                data=[e]+teams[x][e]
                writer.writerow(data)
                
def fix_teams(teams, team_members_list, score_data):
    result=[]
    for team in range(num_of_teams):

        people_to_events={m:[e for e in teams[team] if m in teams[team][e]] for m in team_members_list[team]}
        people_that_need_more_events=[m for m in people_to_events.keys() if len(people_to_events[m])<min_events_per_member]
        people_that_can_give_away_events=[x[0] for x in list(sorted([(m, len(people_to_events[m]),team_members_list[team].index(m)) for m in list(people_to_events.keys()) if len(people_to_events[m])>min_events_per_member], key=lambda item: (item[1],item[2]), reverse=True))]

        temp_team=copy.deepcopy(teams[team])
        best_team=copy.deepcopy(temp_team)
        for m_0 in people_that_need_more_events:

            orig_team=copy.deepcopy(best_team)
            while len([e for e in best_team if m_0 in best_team[e]])<min_events_per_member: # repeat until m_0 has enough events
                best_score=float("inf")
                orig_team=copy.deepcopy(best_team)
                people_to_events={m:[e for e in best_team if m in best_team[e]] for m in team_members_list[team]}
                people_that_need_more_events=[m for m in people_to_events.keys() if len(people_to_events[m])<min_events_per_member]
                #ORDERING PROB NOT MATTER! CHECK THISSSS
                people_that_can_give_away_events=[x[0] for x in list(sorted([(m, len(people_to_events[m]),team_members_list[team].index(m)) for m in list(people_to_events.keys()) if len(people_to_events[m])>min_events_per_member], key=lambda item: (item[1],item[2]), reverse=True))]
                for m_1 in people_that_can_give_away_events:
                    for event in people_to_events[m_1]:
                        if (m_1,event) not in required_members_on_events:
                            temp_team=copy.deepcopy(orig_team)
                            del temp_team[event][temp_team[event].index(m_1)]
                            if is_valid_team_addition(event, m_0, temp_team):
                                temp_team[event].append(m_0)
                                member_to_events_temp_team = {m:[e for e in temp_team if m in temp_team[e]] for m in team_members_list[team]}
                                number_of_events_of_members_with_less_than_min = sum([min_events_per_member-len(member_to_events_temp_team[m]) for m in member_to_events_temp_team if len(member_to_events_temp_team[m])<min_events_per_member])
                                team_score = calculate_preferences_score(temp_team, score_data)+number_of_events_of_members_with_less_than_min*100000
                                if team_score<best_score:
                                    best_score=team_score
                                    best_team=temp_team
        result.append(best_team)
    return result

if __name__ == "__main__":
    # pass
    members, events, experience_data, score_data = process()
    teams, team_members_list = make_teams(score_data, experience_data)
    teams = fix_teams(teams, team_members_list, score_data)
    make_team_csv_files(teams)
    print(teams)
    # make_team_csv_files(teams)
    # print(make_preferences_team(available_events))
    # make_preferences_team(events)
    # make_fake_preferences_data(members, events)
    # scores = make_scores(model, data,events, members, experience_data)
    # display_data(score_data, "Scores", members, events)

