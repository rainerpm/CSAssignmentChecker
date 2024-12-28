# This program checks all the files for an assignment to see if students cheated.
# For each assignment user can select to run these cheating detection tools
#   1) compare50 (https://cs50.readthedocs.io/projects/compare50/en/latest/)
#         assumption is that compare50 has been setup in the Windows Subsystem for Linux
#   2) moss      (https://theory.stanford.edu/~aiken/moss/)
#         requires the CSAClogin.txt file which has a line that has the word 'moss' followed
#         by 1 or more spaces followed by your moss id.
#   3) plagcheck (https://plagcheck.readthedocs.io/en/latest/?badge=latest)
#         runs and analysis moss results (haven't checked how useful this analysis is)
#   4) variable frequency
#         function in this program that checks (python programs only for now) how often the same
#         variable name is used by different student's programs.
#   5) find regex(s)
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


from bs4 import BeautifulSoup   # Thonny (import beautifulsoup4)


# Assignments that are not in CSAC
#    name : list of files
customAssignments = {'FunMidterm' : ['C:/Users/E151509/Desktop/Midterm/submissions/*.jsc']}

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
    for key in customAssignments:
        assignmentNames.append((key,"Custom"))
    for i in range(len(assignmentNames)):
        assignmentNames[i] = (i+1,assignmentNames[i][0],assignmentNames[i][1])
    printInColumns(assignmentNames,5,10,1)
    response = input(f'Select an assignment 1-{len(assignmentNames)}: ')

    assignment = assignmentNames[int(response)-1]
    return assignment

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


def findPatterns(assignment):
    response = input('Enter string or a list of regex patterns to search for: ')
    if response.startswith('['):
        initialList = eval(response)
        patterns = []
        for item in InitialList:
            patterns.append(re.escape(item))
    else:
        patterns = [re.escape(response)]
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
def compare50(assignment,compare50OutputDir,custom=False):
    assignmentName = assignment[1]
    assignmentGroup = assignment[2]    
    if assignmentName not in customAssignments:   # regular CSAC assignment
        compare50Files = ''
        for classPeriodName in classPeriodNames:
            assignmentDir = os.path.join(rootDir,classPeriodName,assignmentGroup,"00PLAGIARISM",assignmentName)
            #print(f'DBG {assignmentDir =}')
            if os.path.isdir(assignmentDir):
                #assignmentDir = f'"{assignmentDir}"'
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
    compare50FilesWsl = compare50Files.replace('\\','/').replace('C:','/mnt/c')
    outputDir = f'{compare50OutputDir}/{assignmentName}'
    outputDirWsl = outputDir.replace('C:','/mnt/c')
    compare50Cmd = f'compare50 -n 100 -o {outputDirWsl} {compare50FilesWsl}'
    if os.path.isdir(outputDir):
        print(f'\nRemoving previous output directory {outputDir}')
        rmtree(outputDir) # remove compare50 output directory for assignment
    print('\nRunning compare50 command from within Python program\n'+compare50Cmd)
    result = subprocess.run('wsl ' + compare50Cmd)
    # print out data from the top 10 match_*.html files
    # Open and read the local HTML file
    print('Top matches')
    print('      structure   text        exact')
    for num in range(1,31):
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

                # Find the div with id="structureleft"
                percents = ''
                for structure in ['structureleft','structureright','textleft','textright','exactleft','exactright']:
                    structureDiv = soup.find('div', id=f'{structure}')
                    
                    if structureDiv:
                        # Find all <h4> elements with class="file_name" within the structureleft div
                        file_names = structureDiv.find_all('h4', class_='file_name')
                        
                        # Print the contents of each <h4> element
                        for file_name in file_names:
                            name = file_name.get_text().split('_')[0]
                            percent = file_name.get_text().split()[-1].replace('(','').replace(')','')
                            percents = percents + f'{percent:>5s} '
                            if structure == 'structureleft':
                                nameLeft = name
                            if structure == 'structureright':
                                nameRight = name
                    else:
                        print('No div with id="structureleft" found.')
                print(f'  {num:2d} {percents} {nameLeft:20s} {nameRight:20s}')
               
    response = input("Open results in browser (x=exit)? ")
    if response != 'x':
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
def plagcheck(assignment):
    with open('CSAClogin.txt') as login:
        for line in login:
            if line.startswith('moss'):
                userid = int(line.split()[1])
    moss = check("python",userid)

    assignmentName = assignment[1]
    assignmentGroup = assignment[2]    
    if assignmentName not in customAssignments:   # regular CSAC assignment
        for classPeriodName in classPeriodNames:
            assignmentDir = os.path.join(rootDir,classPeriodName,assignmentGroup,"00PLAGIARISM",assignmentName)
            if os.path.isdir(assignmentDir):
                #assignmentDir = f'"{assignmentDir}"'
                print(f'{assignmentDir=}')
                moss.addFilesByWildCard(f'{assignmentDir}/*.py' )
    else:   # custom assignment
        for customFiles in customAssignments[assignmentName]:
            moss.addFilesByWildCard(customFiles)
    print("Submitting files to moss")
    moss.submit()
    result = moss.getResults()

    response = input("print results (enter=y)? ")
    if response == '':
        pprint.pprint(result)
        
    # print potential distributor-culprit relationships
    response = input("print potential distributor-culprit relationships (enter=y)? ")
    if response == '':
        pprint.pprint(insights(result))

    # print frequency of each shared solution
    response = input("print frequency of each shared solution (enter=y)? ")
    if response == '':
        pprint.pprint(share_scores(result))

    response = input("Open moss results in browser (enter=y)? ")
    if response == '':
        webbrowser.open(moss.getHomePage()) 

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
    print('  3 moss (plagcheck) useful???')
    print('  4 variable frequency')
    print('  5 find regex(s)')
    response = input("select ('x' to exit)? ")
    if response == '1':
        print('Assumes compare50 is setup in Windows Subsystem for Linux (WSL)')
        compare50(assignment,'C:/Users/E151509/Desktop/compare50')
    elif response == '2':
        moss(assignment)
    elif response == '3':
        plagcheck(assignment)    
    elif response == '4':
        variableFrequency(assignment)
    if response == '5':
        findPatterns(assignment)
    elif response == 'x':
        break


    

