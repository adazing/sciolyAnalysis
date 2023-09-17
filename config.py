'''
Number of teams generated:
    int
        ex. 2
            --A and B teams are made.
'''
num_of_teams=1

'''
Maximum number of members on a team:
    int
'''
max_team_size=15

'''
Events for competition:
    None (All events from past competitions are available)
    list[(string)] (list of all events offered during the competition, the same way they are named in the competitions data.)
'''
available_events=["It's About Time", 'Remote Sensing', 'Cell Biology', 'Anatomy & Physiology', 'Chem Lab', 'Codebusters', 'Dynamic Planet', 'Environmental Chemistry', 'Green Generation', 'Experimental Design', 'Trajectory', 'Write It Do It', 'Flight', 'Disease Detectives', 'Rocks and Minerals', 'Detector Building', 'Forestry', 'Fermi Questions', 'Scrambler', 'Bridge', 'Astronomy', 'Forensics']

'''
Events allowed to have 3 members:
    list[(string)] (list of all events that have 3 members allowed)
'''
events_with_3_members=[]

'''
Members available for competition:
    None (Everyone in all past competitions are available)
    list[(string)] (list of all available members names, the same way they are named in the competitions data.)
'''
available_members=None

'''
Members not available for competition:
    list[(string)] (list of all unavailable members names, the same way they are named in the competitions data.)
'''
unavailable_members=[]

'''
Required members:
    list[(string)] (list of all required members names, the same way they are named in the competitions data.)
'''
required_members=[]

'''
Grade distribution:
    None (Any combination)
    list[(int)#_of_freshmen, (int)#_of_sophomores, (int)#_of_juniors, (int)#_of_seniors] (make sure it adds up to max_team_size or less)
        ex. [4,5,5,1]
            -- four freshmen, 5 sophomores, 5 juniors, 1 senior
'''
grade_distribution=None

'''
Maximum number of events assigned to each member on a team:
    int
'''
max_events_per_member=4

'''
Minimum number of events assigned to each member on a team:
    int
'''
min_events_per_member=4


'''
Conflicting events:
    list[(list)] (list of lists of events that happen at the same time)
        ex. [['Cell Biology','Astronomy'],['Remote Sensing','Disease Detectives']]
            -- Cell Biology and Astronomy happen at the same time
            -- Remote Sensing and Disease Detectives happen at the same time
'''
conflicting_events=[]

'''
experience threshold:
    int (number of times that a person must have done an event in order to count their scores for that event)
        ex. 0 (Everyone's scores are counted)
'''
experience_threshold=1

'''
total experience threshold:
    int (total number of events done necessary to count the person's scores)
        ex. 0 (Everyone's scores are counted)
'''
total_experience_threshold=5
