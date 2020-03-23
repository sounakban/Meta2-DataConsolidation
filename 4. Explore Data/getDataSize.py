import os

file_list = open("../1. Fetch Files/MetaTwo_fileList.txt")
total_size = 0
    
for dataFile in file_list:
    if "eye" in dataFile:
        continue

    dataFile = dataFile.strip()
    file_stats = os.stat(dataFile)
    total_size += (file_stats.st_size/(1024 * 1024 * 1024))

print(total_size)