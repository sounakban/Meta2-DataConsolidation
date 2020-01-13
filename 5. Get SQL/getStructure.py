import pandas as pd
import re
from io import StringIO

columns_data = ['ts', 'episode_number', 'score', 'evt_data1', 'lines_cleared', 'board_rep', \
            'curr_zoid', 'level', 'system_ticks', 'evt_data2', 'event_type', 'evt_id', \
            'zoid_rep', 'next_zoid']
columns_metadata = ["Meta-Two build", "Exp. Start Time", "Game Start", "GameStart Tick", \
            "CPU Tick Frequency", "SID", "USID", "ECID", "Environment", "Task", \
            "SessionNr.", "GameNr.", "Input type", "Connected Inputs", "randSeed", \
            "Screen resolution", "Screen dpi", "Fullscreen", "Window height", \
            "Window width", "md5sum study", "md5sum task", "md5sum environment"]


def grab_data(file_content, gameID):
    index = 0
    updated_content = file_content
    while index < len(updated_content):
        if not "\tGAME\tBEGIN\t" in updated_content[index+1]:
            if "system_ticks" in updated_content[index]:            # For old builds (before 2019)
                index=+1
                continue
            updated_content.pop(index)
        else:
            if not "system_ticks" in updated_content[index]:            # For new builds (since 2019)
                updated_content.pop(index)
            break
    
    updated_content = "\n".join(updated_content)
    temp = pd.read_csv(StringIO(updated_content), delimiter='\t', encoding='utf-8')
    temp['gameID'] = pd.Series([gameID]*temp.shape[0])
    return temp


def grab_metadata(file_content, gameID):
    metadata = {}
    for line in file_content:
        temp = re.sub('\t\t+','\t',line).strip()        # make new build data compatible to old build data
        temp = temp.split("\t")
        if not "\tGAME\tBEGIN\t" in line:
            if "zoid_rep" in line:                      # For new builds (since 2019)
                continue
            metadata[temp[-2]] = [temp[-1]]
        else:
            break

    temp = pd.DataFrame.from_dict(metadata)
    temp['gameID'] = pd.Series([gameID]*temp.shape[0])
    return temp


def change_format(df):
    return new_df


def merge_dataFrames(main_df, new_df, type):
    if type == "meta":
        check_format(new_df)
    # Check whether data is from old build based on presence of extra column
    elif 'game_duration' in new_df.columns:
        # Get rid of extra columns 
        new_df = new_df[columns_data]
    ############ Add code for merge dataframes ###########
    return main_df

def execute(gameID):
    file_list = open("../1. Fetch Files/MetaTwo_fileList.txt")
    fileCount=gameID

    data = pd.DataFrame(columns=columns_data)
    metadata = pd.DataFrame(columns=columns_metadata)

    for dataFile in file_list:
        if "eye" in dataFile:       # Skip if data is eye data
            continue
        dataFile = dataFile.strip()     # Remove spaces from begining or end of file name
        print(dataFile)

        # Replace extra tabs in the file for pandas suitable format
        with open(dataFile) as temp:
            content = temp.readlines()
            # print(content[0:25])

        # Donot change order of the following function calls 'grab_data' modifies 'content'
        new_metaData = grab_metadata(content, fileCount)
        new_data = grab_data(content, fileCount)

        # merge_dataFrames(data, new_data, "data")
        # merge_dataFrames(metadata, new_metaData, "meta")


        new_metaData.to_csv(r'./File2.csv')
        new_data.to_csv(r'./File.csv')
        fileCount+=1
        # break

    # print("Total number of files parsed : ", fileCount)




# The parameter to the execute function is the number to start the primary key for each game
execute(1)