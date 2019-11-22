import re
from io import StringIO

def get_sessionInfo():
    import json
    file_list = open("../1. Fetch Files/MetaTwo_fileList.txt")

    session_dict={}
    game_dict={}
    counter = 0
    for dataFile in file_list:
        if "eye" in dataFile:       # Skip if data is eye data
            continue
        dataFile = dataFile.strip()     # Remove spaces from begining or end of file name
        counter+=1

        # Get individual inormation from each level of the file path
        # event = dataFile.split("/")[6]
        event = "/".join(dataFile.split("/")[5:-2])
        session = dataFile.split("/")[-2]
        game = dataFile.split("/")[-1]

        # if[event == "/RPI Tournaments/2019_Genericon_Tournament/Tournament Laptop 2"]:
        #     print(type(session))

        # Create Event-Session mappings
        if event in session_dict:
            session_dict[event].add(session)
        else:
            session_dict[event] = set()
            session_dict[event].add(session)

        # Create Session-Game mappings
        if session in game_dict:
            game_dict[session].append(game)
        else:
            game_dict[session] = [game]

    # set objects cannot be written to file
    for k, v in session_dict.items():
        session_dict[k] = list(v)

    sessionCount = len([item for sublist in session_dict.values() for item in sublist])
    print("Number of sessions: ", sessionCount)

    gameCount = len([item for sublist in game_dict.values() for item in sublist])
    print("Number of games: ", gameCount)

    print("Total games should be equal to (For error check) :", counter)

    with open('session_list.txt', 'w') as f:
        f.write("This is session data list of sessions for each event")
        f.write("Total session count : %s\n" % sessionCount)
        f.write("-----------------------------------------------------------\n")
        json.dump(session_dict, f, sort_keys=True, indent=4)
        f.write("\n-----------------------------------------------------------\n\n\n")
        f.write("This is session data list of games for each session")
        f.write("Total game count : %s\n" % gameCount)
        f.write("-----------------------------------------------------------\n")
        json.dump(game_dict, f, sort_keys=True, indent=4)



def get_subjectInfo():
    import pandas as pd
    import json
    file_list = open("../1. Fetch Files/MetaTwo_fileList.txt")
    
    subject_dict={}
    for dataFile in file_list:
        if "eye" in dataFile:       # Skip if file contains eye data
            continue
        dataFile = dataFile.strip()     # Remove white spaces from either end of file name
        
        
        # Gets the number of lines before the header containing meta-data
        with open(dataFile) as temp:
            skip_lines = 0
            while temp.readline().count('\t') < 4:
                skip_lines+=1

        # Replaces extra tabs in the file for pandas suitable format
        with open(dataFile) as temp:
            lines = temp.read()
            lines = re.sub('\t\t+','',lines)

        event = "/".join(dataFile.split("/")[5:-2])
        
        print(dataFile)
        # Extract subject ID from files
        content=pd.read_csv(StringIO(lines), delimiter='\t', encoding='utf-8', skiprows=skip_lines)
        if not "SID" in content.columns.values:
            #############################################################
            subject_ID = [0]
            #############################################################
        else: 
            subject_ID = content["SID"].unique()

        if len(subject_ID) > 1:
            print("More than one subjects found for file: ", dataFile)

        # Create Session-Game mappings
        if event in subject_dict:
            subject_dict[event].extend(subject_ID)
        else:
            subject_dict[event] = list(subject_ID)


    print(subject_dict)

    # with open('subject_list.txt', 'w') as f:
    #     f.write("Total subject count : %s\n" % len([item for sublist in subject_dict.values() for item in sublist]))
    #     f.write("-----------------------------------------------------------\n")
    #     json.dump(subject_dict, f, sort_keys=True, indent=4)


# get_sessionInfo()
get_subjectInfo()