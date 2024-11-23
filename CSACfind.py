# This program looks through all the programs turned in for an assignment
# for matches to a list of regular expressions in the python list named
# patterns below.

import os
import re
from CSACgradesData import ASSIGNMENTS
from CSACcustomize import rootDir,classPeriodNames,diffPgm
from math import ceil
import subprocess       # module is in python standard library

# THESE ARE THE PATTERNS TO LOOK FOR
patterns = [r'symvbol',r'ascivar']  


# searches for patterns in a directory and returns files that match the pattern
def search_patterns_in_directory(classPeriod,directory, patterns):   
    compiled_patterns = [re.compile(pattern) for pattern in patterns] # Compile the patterns to avoid recompiling them for every file
    filesMatched = []
    fileCount = 0
    prevName = ''
    if not os.path.isdir(directory):
        print(f"Skipping {directory}: Not a valid directory.")
    else:
        # Walk through all files in the directory
        for filename in os.listdir(directory):
            fileCount += 1
            file_path = os.path.join(directory, filename)
            if os.path.isdir(file_path):  # Skip directories and only process files
                continue
            # Open the file and search for patterns line by line
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line_number, line in enumerate(file, start=1):
                    for pattern in compiled_patterns:
                        if pattern.search(line):
                            if file_path not in filesMatched:
                                filesMatched.append(file_path)
                            name = ' '.join(filename.split()[:2])
                            if name != prevName:
                                print(f"{classPeriod:3s} {name:25s} {line.strip()}")
                            else:    
                                print(f"{'':3s} {'':25s} {line.strip()}")
                            prevName = name
                            break  # Stop after the first match in the line
    return filesMatched,fileCount

assignmentNames = []
for assignment in ASSIGNMENTS:    # ASSIGNMENTS is dictionary defined in grades4ACdata.py
    value = ASSIGNMENTS[assignment]
    assignmentGroup = value[1]
    gradingTuple = value[2]
    assignmentTuples = gradingTuple[1:]
    if assignmentGroup == 'CodingBat':
        assignmentNames = 'various'
    else:
        for assignmentTuple in assignmentTuples:
            assignmentNames.append((assignmentTuple[0],assignmentGroup))
assignmentNames.sort()
for i in range(len(assignmentNames)):
    assignmentNames[i] = (i+1,assignmentNames[i][0],assignmentNames[i][1])

# print options in columns
cols = 5
rows = ceil(len(assignmentNames) / cols)     # divide into columns
fullCols = len(assignmentNames) % cols       # columns that are full (i.e. have data in every row)
for r in range(rows):
    rowStr = ''
    for c in range(cols):
        idx = (c*rows)+r
        if idx < len(assignmentNames):
           rowStr += f'{assignmentNames[idx][0]:2d} {assignmentNames[idx][1]:10}   '
    print(rowStr)    
response = input(f'Select an assignment 1-{len(assignmentNames)}: ')

assignment = assignmentNames[int(response)-1][1]
assignmentGroup = assignmentNames[int(response)-1][2]
print()
directories = []
directory_count = 0
allFileCount = 0
allMatchedFiles = []
for classPeriodName in classPeriodNames:
    assignmentsDir = os.path.join(rootDir,classPeriodName,assignmentGroup,"00PLAGIARISM",assignment)
    if os.path.isdir(assignmentsDir):
        directory_count += 1  
        matchedFiles,fileCount = search_patterns_in_directory(classPeriodName,assignmentsDir, patterns)
        allFileCount += fileCount
        allMatchedFiles = allMatchedFiles + matchedFiles

print(f"\nSearched {directory_count} directories and {allFileCount} files.\n")

response = input("Enter to 'd' to move on to diff, anything else to exit: ")
if response == 'd':
    while True:
        num = 0
        for matchedFile in allMatchedFiles:
            num += 1
            filename = matchedFile.split('\\')[-1]
            print(f"{num:2d} {filename}")
        response = input('Enter two numbers for the files you wish to diff (x to exit): ')
        if response == 'x':
            break
        else:
            num1, num2 = response.split()
            num1 = int(num1)
            num2 = int(num2)

            diffCmd = [diffPgm,allMatchedFiles[num1-1],allMatchedFiles[num2-1]]
            process = subprocess.Popen(diffCmd, shell=True)     # run diff program


