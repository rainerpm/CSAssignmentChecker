
# sudo mount -t drvfs d: /mnt/d
#
#
# This program checks all the files for an assignment to see if students cheated.
# For each assignment user can select to run these cheating detection tools
#   compare50 (https://cs50.readthedocs.io/projects/compare50/en/latest/)
#         * assumption is that compare50 has been setup in the Windows Subsystem for Linux
#         * compare50 inital run is to compare all students against each other, listing
#           out top TOP_MATCHES results
#         * after initial run it's possible to run it again by specifying the number of
#            the top result followed by 'a' for the left student/pgm or 'b' for the right.
#   moss      (https://theory.stanford.edu/~aiken/moss/)
#         requires the CSAClogin.txt file which has a line that has the word 'moss' followed
#         by 1 or more spaces followed by your moss id.
#   variable frequency
#         function in this program that checks (python programs only for now) how often the same
#         variable name is used by different student's programs.
#   find strings
#         finds strings/text in student programs.
#   find regex(s)
#         finds all the files that match 1 or more provided regular expressions
# Assignments can be in the CSAC directory structure or in the customAssignments dictionary.


import os
import glob
import re
from CSACgradesData import ASSIGNMENTS
from CSACcustomize import rootDir,classPeriodNames,diffPgm
from math import ceil
import subprocess       # module is in python standard library
from   shutil   import rmtree    # module is in python standard library
import webbrowser
import mosspy  # Tools -> Open System Shell and then pip install mossypy;  https://github.com/soachishti/moss.py which was linke on moss website (https://theory.stanford.edu/~aiken/moss/)
from plagcheck.plagcheck import check, insights, share_scores
import pprint
from   pathlib  import Path      # module is in python standard library
from datetime import datetime

from bs4 import BeautifulSoup   # Thonny (import beautifulsoup4)

MATCHES = 100  # -n MATCHES compare50 parameter indicates number of matches to output for web results
TOP_MATCHES = 30 # matches that I extract from web results and print on the screen (has to be less than MATCHES above)
HIDE_NAMES = False

# Drive names for files
drives4WSL = ["C","D"]

# Assignments that are not in CSAC
#    name : list of files
# customAssignments = {'FunMidterm' : ['C:/Users/E151509/Desktop/Midterm/submissions/*.jsc']}
customAssignments = {'CodingBat' : [r'"C:/Users/E151509/My Drive/My LASA/CodingBat/CodingBat Plagiarism/PYTHON/onlineSolutions/Logic-2/close_far/*.py"',
                                    r'"C:/Users/E151509/Desktop/misc/CodingBatResults/CodingBat (Various)/close_far/2025_Feb_25/*.py"']}
#customAssignments = {'CodingBat' : [r'"C:\Users\E151509\My Drive\My LASA\CodingBat\CodingBat Plagiarism\PYTHON\onlineSolutions\Logic-2\make_bricks\*.py"',
#                                    r'"C:/Users/E151509/Desktop/misc/CodingBatResults/CodingBat-Various/make_bricks/2025_Feb_25/*.py"']}


#customAssignments = {}

# print list in columns
def printInColumns(listN,columns,textWidth,listElementIndex=-1):
    rows = ceil(len(listN) / columns)     # divide into columns
    fullCols = len(listN) % columns       # columns that are full (i.e. have data in every row)
    for r in range(rows):
        rowStr = ''
        for c in range(columns):
            idx = (c*rows)+r
            if idx < len(listN):
                if listElementIndex == -1:
                   rowStr += f'{idx+1:2d} {listN[idx]:{textWidth}}   '
                else:
                   rowStr += f'{idx+1:2d} {listN[idx][listElementIndex][:textWidth]:<{textWidth}} '
        print(rowStr)    

def getAssignment():
    assignmentNames = []
    for assignment in ASSIGNMENTS:    # ASSIGNMENTS is dictionary defined in grades4ACdata.py
        assignmentData = ASSIGNMENTS[assignment]
        assignmentGroup = assignmentData[1]
        gradingTuple = assignmentData[2]
        assignmentTuples = gradingTuple[1:]
        if assignmentGroup == 'CodingBat':
            assignmentNames = 'various'
        else:
            for assignmentTuple in assignmentTuples:
                assignmentNames.append((assignmentTuple[0].replace('(opt)',''),assignmentGroup))
    assignmentNames.sort()
    for key in customAssignments:
        assignmentNames.append((key,"Custom"))
    for i in range(len(assignmentNames)):
        assignmentNames[i] = (i+1,assignmentNames[i][0],assignmentNames[i][1])
    printInColumns(assignmentNames,5,14,1)
    response = input(f'Select an assignment 1-{len(assignmentNames)}: ')

    assignment = assignmentNames[int(response)-1]
    return assignment

def getDistroFile(assignment):
    assignmentName = assignment[1]
    assignmentGroup = assignment[2]
    assignmentFile = os.path.join(rootDir.replace('/','\\'), "ASSIGNMENT_GROUPS",assignmentGroup,assignmentName,"solutions","compare50_distro.py").replace('\\','/').replace('C:','/mnt/c')
    if Path(assignmentFile).is_file():    # if compare50_distro file exists for this assignment
        return assignmentFile

# searches for patterns in a directory and returns files that match the pattern
def search_patterns_in_directory(classPeriod,directory, patterns):
    #compiled_patterns = [re.compile(pattern) for pattern in patterns] # Compile the patterns to avoid recompiling them for every file
    #print(f'{patterns = }')
    #print(patterns[0],patterns[0].replace('\\\\', '\\'))
    # from CSAC.py pattern = re.compile(regex.replace('\\\\', '\\'),re.M)
    compiled_patterns = [re.compile(pattern.replace('\\\\', '\\'),re.M) for pattern in patterns] # Compile the patterns to avoid recompiling them for every file
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
                            printName = name
                            if HIDE_NAMES:
                                printName = f'Student {fileCount}'
                            if name != prevName:
                                print(f"{classPeriod:3s} {printName:25s} {line.strip()}")
                            else:    
                                print(f"{'':3s} {'':25s} {line.strip()}")
                            prevName = name
                            break  # Stop after the first match in the line
    return filesMatched,fileCount

def diffFiles(filesList):
    if len(filesList) == 2:
        num1 = 0
        num2 = 1
        diffCmd = [diffPgm,filesList[num1-1],filesList[num2-1]]
        process = subprocess.Popen(diffCmd, shell=True)     # run diff program
    else:
        while True:
            num = 0
            for matchedFile in filesList:
                num += 1
                filename = matchedFile.split('\\')[-1]
                print(f"{num:2d} {filename}")
            response = input('Enter two numbers for the files you wish to diff (x to exit): ')
            num1, num2 = response.split()
            num1 = int(num1)
            num2 = int(num2)            
            if response == 'x':
                break
            diffCmd = [diffPgm,filesList[num1-1],filesList[num2-1]]
            process = subprocess.Popen(diffCmd, shell=True)     # run diff program


def findPatterns(patternOrListOfPatterns,assignment,isRegEx):
    if patternOrListOfPatterns.startswith('['):
        initialList = eval(patternOrListOfPatterns)
        patterns = []
        for item in InitialList:
            if isRegEx:
               patterns.append(item) 
            else:
               patterns.append(re.escape(item))
    else:
        if isRegEx:
           patterns = [patternOrListOfPatterns]
        else:
           patterns = [re.escape(patternOrListOfPatterns)]
    print(f'Searching with {patterns =}')
    assignmentName = assignment[1]
    assignmentGroup = assignment[2]
    print()
    directories = []
    directory_count = 0
    allFileCount = 0
    allMatchedFiles = []
    for classPeriodName in classPeriodNames:
        assignmentDir = os.path.join(rootDir,classPeriodName,assignmentGroup,"00PLAGIARISM",assignmentName)
        if os.path.isdir(assignmentDir):
            directory_count += 1  
            matchedFiles,fileCount = search_patterns_in_directory(classPeriodName,assignmentDir, patterns)
            allFileCount += fileCount
            allMatchedFiles = allMatchedFiles + matchedFiles

    print(f"\nSearched {directory_count} directories and {allFileCount} files.\n")

    response = input("Enter to 'd' to move on to diff, anything else to exit: ")
    if response == 'd':
        diffFiles(allMatchedFiles)

## https://cs50.readthedocs.io/projects/compare50/en/latest/
# structure
#     Compares code structure by removing whitespace and comments; normalizing
#     variable names, string literals, and numeric literals; and then running the
#     winnowing algorithm.
# text 
#     Removes whitespace, then uses the winnowing algorithm to compare
#     submissions.
# exact 
#     Removes nothing, not even whitespace, then uses the winnowing algorithm to
#     compare submissions.                
def compare50(assignment,compare50OutputDir,individual=None):
    assignmentName = assignment[1]
    assignmentGroup = assignment[2]    
    if assignmentName not in customAssignments:   # regular CSAC assignment
        compare50Files = ''
        for classPeriodName in classPeriodNames:
            assignmentDir = os.path.join(rootDir,classPeriodName,assignmentGroup,"00PLAGIARISM",assignmentName)
            #print(f'DBG {assignmentDir =}')
            if os.path.isdir(assignmentDir):
                #assignmentDir = f'"{assignmentDir}"'
                if any(file.endswith('.py') for file in os.listdir(assignmentDir)):  # check to see if there are actually python files in the directory
                    compare50Files = compare50Files + f'"{assignmentDir}"/*.py '
                #print(f'DBG {compare50Files =}')
    else:   # custom assignment
        compare50Files = ''
        for customFiles in customAssignments[assignmentName]:
            compare50Files = compare50Files + f'{customFiles} '
    solutionsDir = os.path.join(rootDir,"ASSIGNMENT_GROUPS",assignmentGroup,assignmentName,"solutions")
    if os.path.isdir(solutionsDir):
        compare50Files = compare50Files + f'"{solutionsDir}"/*.py '        
    # run compare50    
    compare50FilesWsl = compare50Files.replace('\\','/')
    # replace 'C:' with '/mnt/c' for WSL use (do this for all drives specified in drives4WSL
    for drive in drives4WSL:
        compare50FilesWsl = compare50FilesWsl.replace(drive + ':','/mnt/' + drive.lower())
    outputDir = f'{compare50OutputDir}/{assignmentName}'
    outputDirWsl = outputDir.replace('C:','/mnt/c')
    idv = ' '
    if individual:
       idv = f' "{individual}" -a '
    distro = ' '
    distroFile = getDistroFile(assignment)
    if distroFile:
        distro = f' -d "{distroFile}"'
    compare50Cmd = f'wsl compare50 -n {MATCHES} -o {outputDirWsl}{idv}{compare50FilesWsl}{distro}'
    if os.path.isdir(outputDir):
        print(f'\nRemoving previous output directory {outputDir}')
        rmtree(outputDir) # remove compare50 output directory for assignment
    print('\nInvoking wsl to run compare50\n'+compare50Cmd)
    result = subprocess.run(compare50Cmd)
    # print out data from the top 10 match_*.html files
    # Open and read the local HTML file
    print('Top matches',datetime.today().strftime('%Y-%m-%d'))
    print('      structure   text        exact')
    topMatchFiles = []
    for num in range(1,TOP_MATCHES+1):
        fileName =  Path(f'{outputDir}\match_{num}.html')
        if not fileName.is_file():
            pass
            #print(f"Error!!! {fileName} not found")
        else:
            with open(fileName, 'r', encoding='utf-8') as file:
                # Read the content of the file
                html_content = file.read()

                # Parse the HTML content with BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')

                # Get period name from stuff at top of page
                topOfPageDiv = soup.find('div', id='structuresub_names')
                if topOfPageDiv:
                    pathNameDiv = topOfPageDiv.find('h5')
                    windowsPathNameLeft = pathNameDiv.get_text()
                    windowsPathNameLeft = windowsPathNameLeft[:windowsPathNameLeft.rfind(' ')]  # remove everything after last space
                    classPeriodLeft = pathNameDiv.get_text().split('/')[9]
                topOfPageDiv = soup.find('div', id='structuresub_names')
                if topOfPageDiv:
                    pathNameDivs = topOfPageDiv.find_all('h5')
                    pathNameDiv = pathNameDivs[1]
                    windowsPathNameRight = pathNameDiv.get_text()
                    windowsPathNameRight = windowsPathNameRight[:windowsPathNameRight.rfind(' ')]  # remove everything after last space
                    classPeriodRight = pathNameDivs[1].get_text().split('/')[9]
                    
                # Get percentages for structure, text, and exact matches as well as the file name (from which I extract the student name)
                percents = ''
                for structure in ['structureleft','structureright','textleft','textright','exactleft','exactright']:
                    divWithInfo = soup.find('div', id=f'{structure}')
                    
                    if divWithInfo:
                        # Find all <h4> elements with class="file_name" within the structureleft div
                        file_names = divWithInfo.find_all('h4', class_='file_name')
                        
                        # Print the contents of each <h4> element
                        for file_name in file_names:
                            name = file_name.get_text().split('_')[0]
                            fileName = file_name.get_text()[:file_name.get_text().find('(')].rstrip()
                            percent = file_name.get_text().split()[-1].replace('(','').replace(')','')
                            percents = percents + f'{percent:>5s} '
                            if structure == 'structureleft':
                                nameLeft = name
                                if HIDE_NAMES:
                                    nameLeft = f'student{num}a'
                                filePathLeft = windowsPathNameLeft + '/' + fileName
                            if structure == 'structureright':
                                nameRight = name
                                if HIDE_NAMES:
                                    nameRight = f'student{num}b'
                                filePathRight = windowsPathNameRight + '/' + fileName
                    else:
                        print('No div with id="structureleft" found.')
                topMatchFiles.append(((classPeriodLeft,nameLeft,filePathLeft),(classPeriodRight,nameRight,filePathRight)))
                print(f'  {num:2d} {percents} ({classPeriodLeft}) {nameLeft:20s}  ({classPeriodRight}) {nameRight:20s}')
    #print(topMatchFiles)
    response = input("#(a|b) run compare50 for individual, <Enter> to open results in browser, x=exit? ")
    if response.endswith('a'):
        num = int(response[:-1])-1
        compare50(assignment,compare50OutputDir,topMatchFiles[num][0][2])
    elif response.endswith('b'):
        num = int(response[:-1])-1
        compare50(assignment,compare50OutputDir,topMatchFiles[num][1][2])
    elif response != 'x':
        webbrowser.open(outputDir + '/index.html')

def moss(assignment):
    with open('CSAClogin.txt') as login:
        for line in login:
            if line.startswith('moss'):
                userid = int(line.split()[1])
    m = mosspy.Moss(userid, "python")

    assignmentName = assignment[1]
    assignmentGroup = assignment[2]    
    if assignmentName not in customAssignments:   # regular CSAC assignment
        for classPeriodName in classPeriodNames:
            assignmentDir = os.path.join(rootDir,classPeriodName,assignmentGroup,"00PLAGIARISM",assignmentName)
            if os.path.isdir(assignmentDir):
                #assignmentDir = f'"{assignmentDir}"'
                print(f'{assignmentDir=}')
                m.addFilesByWildcard(f'{assignmentDir}/*.py' )
    else:   # custom assignment
        for customFiles in customAssignments[assignmentName]:
            m.addFilesByWildcard(customFiles)
    print("Sending files to moss")        
    url = m.send(lambda file_path, display_name: print('*', end='', flush=True))
    print("Opening results in browser")
    webbrowser.open(url)
   
# https://plagcheck.readthedocs.io/en/latest/?badge=latest
# is this useful????
# def plagcheck(assignment):
#     with open('CSAClogin.txt') as login:
#         for line in login:
#             if line.startswith('moss'):
#                 userid = int(line.split()[1])
#     moss = check("python",userid)
# 
#     assignmentName = assignment[1]
#     assignmentGroup = assignment[2]    
#     if assignmentName not in customAssignments:   # regular CSAC assignment
#         for classPeriodName in classPeriodNames:
#             assignmentDir = os.path.join(rootDir,classPeriodName,assignmentGroup,"00PLAGIARISM",assignmentName)
#             if os.path.isdir(assignmentDir):
#                 #assignmentDir = f'"{assignmentDir}"'
#                 print(f'{assignmentDir=}')
#                 moss.addFilesByWildCard(f'{assignmentDir}/*.py' )
#     else:   # custom assignment
#         for customFiles in customAssignments[assignmentName]:
#             moss.addFilesByWildCard(customFiles)
#     print("Submitting files to moss")
#     moss.submit()
#     result = moss.getResults()
# 
#     response = input("print results (enter=y)? ")
#     if response == '':
#         pprint.pprint(result)
#         
#     # print potential distributor-culprit relationships
#     response = input("print potential distributor-culprit relationships (enter=y)? ")
#     if response == '':
#         pprint.pprint(insights(result))
# 
#     # print frequency of each shared solution
#     response = input("print frequency of each shared solution (enter=y)? ")
#     if response == '':
#         pprint.pprint(share_scores(result))
# 
#     response = input("Open moss results in browser (enter=y)? ")
#     if response == '':
#         webbrowser.open(moss.getHomePage()) 

def variableFrequency(assignment):
    variableNames = {}
    assignmentName = assignment[1]
    assignmentGroup = assignment[2]
    files = []
    if assignmentName not in customAssignments:   # regular CSAC assignment
        for classPeriodName in classPeriodNames:
            assignmentDir = os.path.join(rootDir,classPeriodName,assignmentGroup,"00PLAGIARISM",assignmentName)
            if os.path.isdir(assignmentDir):
                #checkFiles = os.listdir(f'{assignmentDir}/*.py')
                for file in glob.glob(f'{assignmentDir}/*.py'):
                    files.append(file)
    else:   # custom assignment
        for customFiles in customAssignments[assignmentName]:
            for file in glob.glob(customFiles):
                files.append(file)
    print(f'Processing {len(files)} files.')
    variables = {}
    for filePath in files:
        with open(filePath, 'r') as file:
            for line in file:
                pattern = r'\bdef\s+(\w+)\s*\((.*?)\)\s*:'    # function definition
                match = re.search(pattern, line)
                if match:
                    params = match.group(2)
                    # Split parameters by commas and strip whitespace
                    param_list = [param.strip() for param in params.split(',') if param.strip()]
                    for param in param_list:
                        if param not in variables:
                            variables[param] = []
                        if filePath not in variables[param]:
                            variables[param].append(filePath)
                        
                pattern = r'^\s*(\w+)\s*='    # assignment statement
                match = re.search(pattern, line)
                if match:
                    variable = match.group(1)
                    if variable not in variables:
                        variables[variable] = []
                    if filePath not in variables[variable]:
                        variables[variable].append(filePath)                    

    print("Variables used more than once but less than 10 times")
    variableList = []
    for variable in variables:
        if len(variables[variable]) > 1 and len(variables[variable]) < 10:
            variableList.append((len(variables[variable]),variable,str(len(variables[variable]))+ ' ' +variable))
    variableList.sort()
    while True:
        printInColumns(variableList,5,22,2)
        response = input("Enter number for more details ('x' to exit): ")
        if response == 'x':
            break
        key = variableList[int(response)-1][1]
        print(f'Details for variable "{key}"')
        pprint.pprint(variables[key], indent=4)
        response = input("Enter to 'd' to move on to diff, anything else to exit: ")
        if response == 'd':
            diffFiles(variables[key])

# MAIN PROGRAM

print(f'\nCurrently only works for Python files!!!!\n')

assignment = getAssignment()

while True:
    print(f'\nAssignment {assignment[1]}')
    print('  1 compare50')
    print('  2 moss')
    print('  3 variable frequency')
    print('  4 find string(s)')
    print('  5 find regex(s)')
    print('  6 predefined regex(s)')
    response = input("select ('x' to exit)? ")
    if response == '1':
        print('Assumes compare50 is setup in Windows Subsystem for Linux (WSL)')
        compare50(assignment,'C:/Users/E151509/Desktop/compare50')
    elif response == '2':
        moss(assignment)   
    elif response == '3':
        variableFrequency(assignment)
    elif response == '4':
        response = input('Enter string or a list of strings: ')
        findPatterns(response,assignment,False)
    if response == '5':
        response = input('Enter regex or a list of regexs: ')
        findPatterns(response,assignment,True)
    elif response == '6':
        options = [('join method or map function',r'\b(join|map)\s*\('),
                   ('list comprehension',r'\[.+\bfor\b.+\]'),
                   ('comments at end of line',r'^(?!\s*#).*(?=\s*#)')]
        for i, option in enumerate(options, 1):
           print(f"    {i} {option[0]}")
        choice = int(input("    Enter the number of your choice: "))
        if 1 <= choice <= len(options):
            findPatterns(options[choice-1][1],assignment,True)
    elif response == 'x':
        break


    


