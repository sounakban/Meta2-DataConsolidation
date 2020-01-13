import pandas as pd
import re
from io import StringIO

def grab_data(file_content):
    flag = 1
    updated_content = file_content
    for line in updated_content:
        if line.count('\t') < 4:
            updated_content = re.sub(line,'',updated_content)
            flag = 0
        else:
            if flag==1:
                continue
            break

    print(updated_content)
    return pd.read_csv(StringIO(updated_content), delimiter='\t', encoding='utf-8', skiprows=skip_lines)

def grab_Metadata(file_content):


def execute():
    file_list = open("../1. Fetch Files/MetaTwo_fileList.txt")
    fileCount=0
    header_list=[]
    for dataFile in file_list:
        if "eye" in dataFile:       # Skip if data is eye data
            continue
        dataFile = dataFile.strip()     # Remove spaces from begining or end of file name
        print(dataFile)

        # Get the number of lines before the header containing meta-data
        # skip_lines = 0
        # with open(dataFile) as temp:
        #     while temp.readline().count('\t') < 4:
        #         skip_lines+=1

        # Replace extra tabs in the file for pandas suitable format
        with open(dataFile) as temp:
            content = temp.read()
            content = re.sub('\t\t+','',content)

        data = grab_data(file_content)
        # metaData = grab_metadata(file_content)

        # print(list(data.columns.values)) #file header
        # if not set(data.columns.values) in header_list:      # Create a list of header combinations
        #     header_list.append(set(data.columns.values))

        fileCount+=1
        break

    # with open('header_list.txt', 'w') as f:
    #     for header in header_list:
    #         f.write("%s\n" % header)
    # print("Total number of files parsed : ", fileCount)


execute()