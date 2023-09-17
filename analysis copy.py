from config import *
import pandas as pd
import os
import vowpalwabbit
import matplotlib.pyplot as plt
import seaborn as sns
import math
import numpy as np

model = vowpalwabbit.Workspace("-q :: -f scioly.model --quiet --noconstant")

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
    if type(min_events_per_member)!=int:
        raise Exception("min_events_per_member"+error_msg)
    if (type(conflicting_events)!=list and conflicting_events!=None):
        raise Exception("conflicting_events"+error_msg)
    if type(conflicting_events)==list:
        if any([type(event_list)!=list for event_list in conflicting_events]) and any([type(event)!=str for eventlist in conflicting_events for event in eventlist]):
            raise Exception("conflicting_events"+error_msg)
    if type(min_events_done_per_member)!=int and min_events_done_per_member!=None:
        raise Exception("min_events_done_per_member"+error_msg)
    #gathering competition data info
    members=set() #members in all the competitions so far
    events=set() #events in all the competitions so far
    # num_of_events_done_per_member={} #number of events each member competed in
    # unique_events_done_per_member={} #unique events each member competed in
    # events_data=[]# data on each event for each competition
    for competition_name in os.listdir("competitions"):
        f = os.path.join("competitions", competition_name)
        competition=pd.read_csv(f)
        for index, row in competition.iloc[:,range(5)].iterrows():
            if pd.isna(row.iloc[0]):
                break
            else:
                events.add(row.iloc[0])
                members.add(row.iloc[1])
                members.add(row.iloc[2])
                members.add(row.iloc[3])
    members=[m for m in members if not pd.isna(m)]
    print(members)
    print(events)
        # members.dropna().unique().tolist()
        # print(members)
    members=list(members)
    events=list(events)
        # print(events)
    events_experience=np.asarray([[0]*len(members)]*len(events))
    scores_data=np.asarray([[0.0]*len(members)]*len(events)) #rows=events columns=members
    for competition_name in os.listdir("competitions"):
        f = os.path.join("competitions", competition_name)
        competition=pd.read_csv(f)
        average_event_rank=float(competition.iloc[-1,1])
        num_of_teams_total=float(competition.iloc[-3,1])+1
        for index, row in competition.iloc[:,range(5)].iterrows():
            if pd.isna(row.iloc[0]):
                break
            else:
                # print(events_experience)
                # print(events.index(row.iloc[0]))
                # print(members.index(row.iloc[1]))
                scores_data[events.index(row.iloc[0])][members.index(row.iloc[1])]+=average_event_rank/num_of_teams_total-float(row.iloc[4])/num_of_teams_total
                events_experience[events.index(row.iloc[0])][members.index(row.iloc[1])]+=1
                scores_data[events.index(row.iloc[0])][members.index(row.iloc[2])]+=average_event_rank/num_of_teams_total-float(row.iloc[4])/num_of_teams_total
                events_experience[events.index(row.iloc[0])][members.index(row.iloc[2])]+=1
                if not pd.isna(row.iloc[3]):
                    scores_data[events.index(row.iloc[0])][members.index(row.iloc[3])]+=average_event_rank/num_of_teams_total-float(row.iloc[4])/num_of_teams_total
                    events_experience[events.index(row.iloc[0])][members.index(row.iloc[3])]+=1
    for e in range(len(events_experience)):
        for p in range(len(events_experience[e])):
            if events_experience[e][p]<2:
                scores_data[e][p]=-1.0
            else:
                scores_data[e][p]=(scores_data[e][p]/events_experience[e][p])
    fig, ax = plt.subplots(figsize=(12,7))         # Sample figsize in inches
    hm = sns.heatmap(data = scores_data,xticklabels=members,yticklabels=events, linewidths=1,linecolor="k")
    # displaying the plotted heatmap
    plt.subplots_adjust(left=0.2, right=1.0, top=0.95, bottom=0.2)
    plt.show()
    fig, ax = plt.subplots(figsize=(12,7))         # Sample figsize in inches
    hm = sns.heatmap(data = events_experience,xticklabels=members,yticklabels=events, linewidths=1,linecolor="k")
    plt.subplots_adjust(left=0.2, right=1.0, top=0.95, bottom=0.2)
    # displaying the plotted heatmap
    plt.show()
    # for competition_name in os.listdir("competitions"):
    #     f = os.path.join("competitions", competition_name)
    #     competition=pd.read_csv(f)
    #     average_event_rank=float(competition.iloc[-1,1])
    #     num_of_teams_total=float(competition.iloc[-3,1])
    #     for index, row in competition.iloc[:,range(5)].iterrows():
    #         if pd.isna(row.iloc[0]):
    #             break
    #         else:
    #             event_data=[float(row.iloc[4])/num_of_teams_total-average_event_rank/num_of_teams_total]
    #             events.add(row.iloc[0])
    #             members.add(row.iloc[1])
    #             members.add(row.iloc[2])
    #             for i in range(1,3):
    #                 if row.iloc[i]in unique_events_done_per_member:
    #                     unique_events_done_per_member[row.iloc[i]].add(row.iloc[0])
    #                     num_of_events_done_per_member[row.iloc[i]]+=1
    #                 else:
    #                     unique_events_done_per_member[row.iloc[i]]=set([row.iloc[0]])
    #                     num_of_events_done_per_member[row.iloc[i]]=1
    #             if pd.isna(row.iloc[3]):
                    
    #                 event_data.append(row.iloc[1].replace(" ","_")+":0.5 "+row.iloc[2].replace(" ","_")+":0.5 Event:"+row.iloc[0].replace(" ","_"))
    #             else:
    #                 if row.iloc[3].replace(" ","_") in unique_events_done_per_member:
    #                     unique_events_done_per_member[row.iloc[3].replace(" ","_")].add(row.iloc[0].replace(" ","_"))
    #                     num_of_events_done_per_member[row.iloc[3].replace(" ","_")]=1
    #                 else:
    #                     unique_events_done_per_member[row.iloc[3].replace(" ","_")]=set([row.iloc[0].replace(" ","_")])
    #                     num_of_events_done_per_member[row.iloc[3].replace(" ","_")]=1
    #                 members.add(row.iloc[3].replace(" ","_"))
    #                 event_data+=row.iloc[1].replace(" ","_")+":"+str(1/3)+" "+row.iloc[2].replace(" ","_")+":"+str(1/3)+" "+row.iloc[3].replace(" ","_")+":"+str(1/3)+" Event:"+row.iloc[0].replace(" ","_")
    #         data.append(event_data)
    # return list(members),list(events),num_of_events_done_per_member,unique_events_done_per_member,data

if __name__ == "__main__":
    members, events, num_of_events_done_per_member, unique_events_done_per_member,data = process()
    print(data)