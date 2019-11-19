import pandas as pd
import re
from io import StringIO

# info=pd.read_csv('../input/UserInfo.tsv',delimiter='\t',encoding='utf-8')
# print(list(info.columns.values)) #file header

file_list = open("../Fetch Files/MetaTwo_fileList.txt")
fileCount=0
header_list=[]
for dataFile in file_list:
    if "eye" in dataFile:       # Skip if data is eye data
        continue
    dataFile = dataFile.strip()     # Remove spaces from begining or end of file name
    
    skip_lines = 0
    with open(dataFile) as temp:
        while temp.readline().count('\t') < 4:
            skip_lines+=1
        # print(temp.readline(), skip_lines)

    # with open(dataFile) as temp:
    #     lines = temp.readlines()
    #     print(lines[20:21])

    with open(dataFile) as temp:
        lines = temp.read()
        lines = re.sub('\t\t+','',lines)
    
    print(dataFile)
    content=pd.read_csv(StringIO(lines), delimiter='\t', skiprows=skip_lines)
    # content=pd.read_csv(dataFile, delimiter='\t', encoding='utf-8', skiprows=skip_lines-1)
    # print(list(content.columns.values)) #file header
    if not set(content.columns.values) in header_list:
        header_list.append(set(content.columns.values))
    fileCount+=1
    # if fileCount == 5:
    #     break

with open('header_list.txt', 'w') as f:
    for header in header_list:
        f.write("%s\n" % header)
print("Total number of files parsed : ", fileCount)