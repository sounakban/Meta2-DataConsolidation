import pandas as pd
import re
from io import StringIO

def grab_data(file_content):
    flag = 1
    index = 0
    updated_content = file_content
    while index < len(updated_content):
        if updated_content[index].count('\t') < 6:
            updated_content.pop(index)
            flag = 0
        else:
            index=+1
            if flag==1:
                continue
            break
    
    updated_content = "\n".join(updated_content)
    return pd.read_csv(StringIO(updated_content), delimiter='\t', encoding='utf-8')


def grab_metadata(file_content):
    metadata = {}
    flag = 1
    for line in file_content:
        if line.count('\t') < 6:
            temp = line.split("\t")
            metadata[temp[0]] = [temp[1]]
            flag = 0
        else:
            if flag==1:
                continue
            break

    return pd.DataFrame.from_dict(metadata)


def change_format(df):
    return df


def merge_dataFrames(main_df, new_df, type):
    if type == "meta":
        check_format(df)


def execute():
    file_list = open("../1. Fetch Files/MetaTwo_fileList.txt")
    fileCount=0
    
    data = ['ts', 'episode_number', 'score', 'evt_data1', 'lines_cleared', 'board_rep', 'curr_zoid', 'level', 'system_ticks', 'evt_data2', 'event_type', 'evt_id', 'zoid_rep', 'next_zoid']
    metadata = []
    data = pd.DataFrame(columns=columns_data)
    metadata = pd.DataFrame(columns=columns_metadata)

    for dataFile in file_list:
        if "eye" in dataFile:       # Skip if data is eye data
            continue
        dataFile = dataFile.strip()     # Remove spaces from begining or end of file name
        print(dataFile)

        # Replace extra tabs in the file for pandas suitable format
        with open(dataFile) as temp:
            content = temp.read()
            content = re.sub('\t\t+','',content)
            #Splits to list, easier to remove unwanted lines without parsing entire file
            content = content.splitlines()

        new_data = grab_data(content)
        new_metaData = grab_metadata(content)

        merge_dataFrames(data, new_data, "data")
        merge_dataFrames(metadata, new_metadata, "meta")

        fileCount+=1
        break

    # with open('header_list.txt', 'w') as f:
    #     for header in header_list:
    #         f.write("%s\n" % header)
    # print("Total number of files parsed : ", fileCount)


execute()