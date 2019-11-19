import pandas as pd
import re
from io import StringIO

file_list = open("../Fetch Files/MetaTwo_fileList.txt")
fileCount=0
header_list=[]
for dataFile in file_list:
    if "eye" in dataFile:       # Skip if data is eye data
        continue
    dataFile = dataFile.strip()     # Remove spaces from begining or end of file name
    
    # Gets the number of lines before the header containing meta-data
    skip_lines = 0
    with open(dataFile) as temp:
        while temp.readline().count('\t') < 4:
            skip_lines+=1

    # Replaces extra tabs in the file for pandas suitable format
    with open(dataFile) as temp:
        lines = temp.read()
        lines = re.sub('\t\t+','',lines)
    
    print(dataFile)
    content=pd.read_csv(StringIO(lines), delimiter='\t', encoding='utf-8', skiprows=skip_lines)
    # print(list(content.columns.values)) #file header
    if not set(content.columns.values) in header_list:      # Create a list of header combinations
        header_list.append(set(content.columns.values))
    fileCount+=1

with open('header_list.txt', 'w') as f:
    for header in header_list:
        f.write("%s\n" % header)
print("Total number of files parsed : ", fileCount)