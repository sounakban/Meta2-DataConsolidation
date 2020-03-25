import pandas as pd
import re
from io import StringIO
from utilities import get_schema, get_SQLConnection, get_metaDataColumns, get_dataColumns


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
    
    # Some old data files have inconsistent number of delimeters at the end of the rows
    extra_columns = updated_content[1].count("\t") - updated_content[0].count("\t")
    updated_content[0] = updated_content[0].replace("\n", ("\t"*extra_columns)+"\n")

    # Convert list of lines to one whole text (for pandas compatibility)
    updated_content = "\n".join(updated_content)
    extra_columns = updated_content[1].count("\t") - updated_content[0].count("\t")
    temp = pd.read_csv(StringIO(updated_content), delimiter='\t', encoding='utf-8')
    temp.insert(0, "gameID", [gameID]*temp.shape[0], True)
    temp = temp[get_dataColumns()]
    
    return temp


def grab_metadata(file_content, gameID, filePath):
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
    temp.insert(0, "gameID", [gameID], True)
    temp.insert(0, "filePath", [filePath], True)
    return temp


def change_format(df):
    if 'GameType' in df.columns:
        new_df = df
        new_df.rename(columns={'GameType':'Environment', 'GameTask':'Task', 'Session':'SessionNr.'}, inplace=True)
        new_df.insert(len(new_df.columns), "md5sum study", [""], True)
        new_df.insert(len(new_df.columns), "md5sum task", [""], True)
        new_df.insert(len(new_df.columns), "md5sum environment", [""], True)
        if not "USID" in new_df.columns:
            new_df.insert(6, "USID", new_df['SID'], True)
        if not "Connected Inputs" in new_df.columns:
            new_df.insert(13, "Connected Inputs", [""], True)
        return new_df
    else:
        return df


def merge_dataFrames(main_df, new_df, type):
    if type == "meta":
        new_df = change_format(new_df)
    main_df = pd.concat([main_df, new_df], sort=False)
    return main_df


def execute(gameID, begin, end):
    data, metaData = get_schema()

    file_list = open("../1. Fetch Files/MetaTwo_fileList.txt")
    fileCount=0

    for dataFile in file_list:
        fileCount+=1
        if fileCount < begin:
            continue
        print(fileCount)
        if "eye" in dataFile:       # Skip if data is eye data
            fileCount-=1
            continue
        gameID+=1
        dataFile = dataFile.strip()     # Remove spaces from begining or end of file name
        print('/'.join(dataFile.split('/')[3:]))

        # Replace extra tabs in the file for pandas suitable format
        with open(dataFile) as temp:
            content = temp.readlines()

        # Donot change order of the following function calls 'grab_data' modifies 'content'
        new_metaData = grab_metadata(content, gameID, dataFile[dataFile.find('Tetris'):])
        new_data = grab_data(content, gameID)

        data = merge_dataFrames(data, new_data, "data")
        metaData = merge_dataFrames(metaData, new_metaData, "meta")

        # To avoid running out of emory write current data and clear out old data
        if fileCount%30 == 0:
            writemode = 'a'
            header = False
            if  fileCount == 30:
                writemode = 'w'
                header = True
            metaData.to_csv(r'./metaFile.csv', index=False, mode=writemode, header=header)
            data.to_csv(r'./File.csv', index=False, mode=writemode, header=header)
            data, metaData = get_schema()

        if fileCount > 2:
            break

    if  fileCount < 30:
        writemode = 'w'
        header = True
    else:
        writemode = 'a'
        header = False
    metaData.to_csv(r'./metaFile.csv', index=False, mode=writemode, header=header)
    data.to_csv(r'./File.csv', index=False, mode=writemode, header=header)

    # print("Total number of files parsed : ", fileCount)


for i in range(0, 1300, 100):
    begin = i
    end = begin+30
    gameID = 0
    execute(gameID, begin, end)
