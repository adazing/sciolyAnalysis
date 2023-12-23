# notes
# need grade distribution stuff!!!, collect from school emails?
# a lot of stuff below NOT implemented yet!!!!

'''
Number of teams generated:
    int
        ex. 2
            --A and B teams are made.
'''
num_of_teams=2

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
# available_events=["It's About Time", 'Remote Sensing', 'Cell Biology', 'Anatomy & Physiology', 'Chem Lab', 'Codebusters', 'Dynamic Planet', 'Environmental Chemistry', 'Green Generation', 'Experimental Design', 'Trajectory', 'Write It Do It', 'Flight', 'Disease Detectives', 'Rocks and Minerals', 'Detector Building', 'Forestry', 'Fermi Questions', 'Scrambler', 'Bridge', 'Astronomy', 'Forensics']
available_events=["Air Trajectory", "Anatomy and Physiology", "Astronomy", "Chem Lab", "Codebusters(3)", "Detector Building", "Disease Detectives", "Dynamic Planet", "Ecology", "Experimental Design(3)", "Fermi Questions", "Flight", "Forensics", "Forestry", "Fossils", "GeoLogic Mapping", "Microbe Mission", "Optics", "Robot Tour", "Scrambler", "Tower", "Write It Do It", "Wind Power"]

'''
Event Types for competition:
    list[(list)] (list of lists of events that are of the same type - used for making inferences about what other events members might like)
        ex. [['Cell Biology','Astronomy'],['Remote Sensing','Disease Detectives']]
            -- Cell Biology and Astronomy happen at the same time
            -- Remote Sensing and Disease Detectives happen at the same time
'''
# event_types = [["Air Trajectory", "Flight", "Robot Tour", "Scrambler", "Tower", "Write It Do It—Doer", "Write It Do It—Writer","Wind Power"], ["Anatomy and Physiology", "Astronomy", "Code Analysis (trial)", "Codebusters", "Disease Detectives", "Dynamic Planet", "Ecology","Fermi Questions", "Forensics", "Fossils", "Geocaching (Trial)", "Geologic Mapping", "Horticulture (Trial)", "Microbe Mission", "Mystery Architecture (Trial)", "Precision Medicine (Trial)"], ["Chem Lab","Experimental Design", "Optics"], ["Detector Building"]]
event_types = [["Anatomy and Physiology", "Disease Detectives", "Ecology", "Forestry", "Microbe Mission"], ["Astronomy", "Dynamic Planet", "Fossils", "GeoLogic Mapping"],["Air Trajectory", "Chem Lab", "Detector Building", "Forensics", "Optics", "Wind Power"], ["Flight", "Robot Tour", "Scrambler", "Tower"], ["Codebusters(3)","Experimental Design(3)", "Fermi Questions", "Write It Do It"]]
'''
Events allowed to have 3 members:
    list[(string)] (list of all events that have 3 members allowed)
'''
events_with_3_members=['Codebusters(3)', 'Experimental Design(3)']

'''
Members available for competition:
    None (Everyone in all past competitions are available)
    list[(string)] (list of all available members names, the same way they are named in the competitions data.)
'''
available_members=None

'''
Officers:
    list[(string)] (list of all officer names, the same way they are named in the competitions data. This makes them have priority in putting them on a team/put on the best team.)
'''

officers=["Albert Ming Wei", "Brian Zhao", "David Huang", "Joning Wang", "Kelly Deng", "Kevin Daniel", "Rick Yang"]
# officers=[]

'''
Required members:
    list[(string)] (list of all required members names, the same way they are named in the competitions data. This requires them to be on a team, but they may or may not be put on the A team.)
    NOTE: do not include officers!
'''

# required_members=["Adrian Wang", "Alina Yang", "Sonja Xie", "Eric Kwon", "Anish Mehta", "Mora Menajovsky", "Alina Peng", "Drew Kaplan", "Hila Savir", "Marina Miranda", "Leia Patel", "Peter Lin", "Bryan Chung"]
required_members=["Ian Rozens", "David Duan", "Eden Hoong", "Linda Zhang", "Eli Tabak", "Ada Langford", "Sarah Kobi", "Kevin Dong", "Raymond Tong", "Eric Kwon", "Rishi Singhal", "Bryan Chung", "Peter Lin", "Ema Zheng", "Wentao He", "Arjun Sriskanthan", "Sam Junnarkar", "Justin Zhang", "Sophia Wu", "Adrian Wang", "Alina Yang", "Sonja Xie", "Armita Ahmed"]

'''
Upper Threshold Grade distribution: NOT IMPLEMENTED YET
    None (Any combination)
    list[(int)#_of_freshmen, (int)#_of_sophomores, (int)#_of_juniors, (int)#_of_seniors] (make sure it adds up to max_team_size or less)
        ex. [4,5,5,1]
            -- four freshmen, 5 sophomores, 5 juniors, 1 senior
'''
upper_threshold_grade_distribution=None

'''
Lower Threshold Grade distribution: NOT IMPLEMENTED YET
    None (Any combination)
    list[(int)#_of_freshmen, (int)#_of_sophomores, (int)#_of_juniors, (int)#_of_seniors] (make sure it adds up to max_team_size or less)
        ex. [4,5,5,1]
            -- four freshmen, 5 sophomores, 5 juniors, 1 senior
'''
lower_threshold_grade_distribution=None

'''
Maximum number of events assigned to each member on a team:
    int
'''
max_events_per_member=4

'''
Minimum number of events assigned to each member on a team:
    int
'''
min_events_per_member=3


'''
Conflicting events:
    list[(list)] (list of lists of events that happen at the same time)
        ex. [['Cell Biology','Astronomy'],['Remote Sensing','Disease Detectives']]
            -- Cell Biology and Astronomy happen at the same time
            -- Remote Sensing and Disease Detectives happen at the same time
'''
conflicting_events=[["Detector Building","Fossils","Write It Do It"],
                    ["Disease Detectives", "Fermi Questions","Forensics"],
                    ["Experimental Design(3)","GeoLogic Mapping", "Microbe Mission"],
                    ["Chem Lab","Codebusters(3)","Ecology"],
                    ["Anatomy and Physiology", "Astronomy","Optics"],
                    ["Dynamic Planet","Forestry","Wind Power"]]

'''
experience threshold: NOT IMPLEMENTED YET
    int (number of times that a person must have done an event in order to count their scores for that event) * Prevents people getting carried to have high scores
        ex. 0 (Everyone's scores are counted)
'''
experience_threshold=0

'''
total experience threshold: NOT IMPLEMENTED YET
    int (total number of events done necessary to count the person's scores) * Prevents people getting carried to have high scores
        ex. 0 (Everyone's scores are counted)
        ex. 7 (Everyone who has done at least 7 events has their scores counted, while people with less than 7 events automatically are given lowest possible scores)
'''
total_experience_threshold=7

'''
preferences file name:
    None (only skill level is taken into account, not people's preferences)
    str (str of the name of the csv file that stores people's preferences)
'''
preferences_file_name="cmu copy.csv"

'''
member-member preferences:
    list[(tuples)]:
        list of tuples (size 3) of people who want to be together in a specific event. If not for a specific event, say None.
        ex:
            [("Bob", "Alice", None), ("Alice", "Samantha", None), ("Bob", "Samantha", "Robot Tour")]
'''
# member_member_preferences = [("Ada Langford", "Eli Tabak", "Detector Building"),("Jerry Jin", "Justin Zhang", "Robot Tour"), ("Adrian Wang", "Justin Zhang", None), ("Sarah Kung", "Sophie Lammer", None), ("Sarah Kung", "Armita Ahmed", None), ("Sarah Kung", "Sonja Xie", None), ("Sarah Kung", "Alina Yang", None), ("Ada Langford", "Joyce Liu", "Forensics"), ("Ada Langford", "Brian Zhao", "Forensics"), ("Ada Langford", "Brian Zhao", "Robot Tour")]
member_member_preferences = [("Eli Tabak", "Ada Langford", "Detector Building"), ("Justin Zhang", "Jerry Jin", "Write It Do It"), ("Stella Van Arsdale", "Leia Patel", None), ("Brian Zhao", "Ada Langford", "Forensics"), ("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"),("Brian Zhao", "Ada Langford", "Robot Tour"), ("Adrian Wang", "Derrick Kuo", "Write It Do It"), ("Mora Menajovsky", "Alina Peng", "Write It Do It"), ("Sarah Kobi", "Linda Zhang", "Microbe Mission"), ("Sam Junnarkar", "Eden Hoong", "GeoLogic Mapping"), ("Sam Junnarkar", "Eden Hoong", "Experimental Design"), ("Arjun Sriskanthan", "Eden Hoong", "Experimental Design"), ("Marina Miranda", "Sophie Lammer", "Astronomy"), ("Xuanchang Zheng", "Eden Hoong", "Wind Power"), ("Sam Junnarkar", "Eden Hoong", "Geologic Mapping"), ("Arjun Sriskanthan", "Sam Junnarkar", "Dynamic Planet"), ("Eric Kwon", "Rishi Singhal", "Anatomy"),("Adrian Wang", "Justin Zhang", "Write It Do It"), ("Sarah Kung","Sonja Xie", None), ("Sarah Kung","Sarah Kobi", None), ("Sarah Kung","Linda Zhang", None), ("Sarah Kung","Sophie Lammer", None), ("Sarah Kung","Alina Yang", None), ("Sarah Kung","Alina Yang", "Write It Do It"), ("Sarah Kung","Armita Ahmed", None), ("Sarah Kung","Ada Langford", None), ("Sarah Kung","Joyce Liu", None), ("Sarah Kung","Sofia Corriggio", None)]

'''
Randomness:
    only changes settings when Randomness mode is not on 'none'
    float (range 0.0-1.0)
'''
randomness_num = 0.5

'''
Randomness mode:
    String:
        - 'high'
            - best team is affected by randomness_num
        - 'low'
            - best team is not affected by randomness_num
        - 'none'
'''
randomness_mode = 'high'

'''
Required members on events
    list[(tuples)]:
        list of tuples (size 2) of people who need to be on a specific event for their team.
        ex:
            [("Bob", "Robot Tour"), ("Alice", "Chem Lab")]
'''
required_members_on_events = [("Alina Yang","Write It Do It"),("Sonja Xie", "Write It Do It")]

'''
Required members NOT on events
    list[(tuples)]:
        list of tuples (size 2) of people who need to not be on a specific event for their team.
        ex:
            [("Bob", "Robot Tour"), ("Alice", "Chem Lab")]
'''
required_members_not_on_events = []
