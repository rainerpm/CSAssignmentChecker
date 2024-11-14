# This program reads the student results from the scoreboard file generated by the CSAssignmentChecker
# and writes out a file with a grade for each student.
# It will likely have to be customized but should be a good starting point.

from   pathlib  import Path
from datetime import datetime
from CSACgradesData import ASSIGNMENTS,codingBatDir,gradesDir,classPeriods,latePenaltyPercentageDefault
from CSACcustomize import rootDir,scoreboardDir,classPeriodNames,classPeriodNamesForMenu
from math import ceil

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    LIGHTGRAY = '\033[37m'
    ORANGE = '\033[33m'
    BLACK = '\033[30m'
    
def calcPointsForStudent(gradingTuple,results):
    #print(f'{gradingTuple = }')
    #print(f'{results = }')
    # ['0x', 'C', 'C1']
    pointsPossible = gradingTuple[0]
    poinstForHowManyCorrect = type(pointsPossible) is tuple
    if poinstForHowManyCorrect:
        pointsPossibleTuple = gradingTuple[0]
        pointsPossible = pointsPossibleTuple[0]
    assignmentTuples = gradingTuple[1:]
    idx = 0
    points4grade = 0
    points4gradeOptionalAssignments = 0
    if not poinstForHowManyCorrect: # grade is based on the specific assignments in an assignment group that were completed.
        skippedOptionalParts = False
        for result in results:
            assignmentTuple = assignmentTuples[idx]
            idx = idx + 1
            assignmentName = assignmentTuple[0]
            assignmentPercentage = assignmentTuple[1]
            #print(f'  {result=} {assignmentTuple=} {assignmentPercentage=}')
            # possible deduction for incorrect attempts (only happens if percentDeductionForIncorrectSubmission is specified in assignmentTuple)
            pointDeductionForIncorrectAttemts = 0
            if len(assignmentTuple) == 3 and len(result) >= 2:
                percentDeductionForEachIncorrectSubmission = assignmentTuple[2]
                incorrectAttempts = 0
                if result.startswith('C') or result.startswith('L'):
                    incorrectAttempts = int(result[1:])
                pointDeductionForIncorrectAttemts = round(pointsPossible * assignmentPercentage/100 * percentDeductionForEachIncorrectSubmission/100,1) * incorrectAttempts
            # Point percentage for being late
            latePenaltyPercentage = 1.00  # assignments start at a 100%
            if result.startswith('L'):
                latePenaltyPercentage = latePenaltyPercentageDefault   # late assignments are worth this percentage
            points4assignment = ((pointsPossible * assignmentPercentage/100) - pointDeductionForIncorrectAttemts) * latePenaltyPercentage          

            if result.startswith('C') or result.startswith('L'):
                if result.startswith('L') and skippedOptionalParts:
                    points4gradeOptionalAssignments = points4gradeOptionalAssignments * 0.70
                #print(f'DBG2 {points4grade = } {points4assignment = } {points4gradeOptionalAssignments = }')
                points4grade = points4grade + points4assignment + points4gradeOptionalAssignments
                points4gradeOptionalAssignments = 0  # reset to 0 so if student completes multiple optional parts a previous optional part's points is not added multiple times
            else:    
                if assignmentName.startswith('(opt)'):
                    skippedOptionalParts = True
                    #print(f'DBG2 {points4gradeOptionalAssignments = } {points4assignment = }')
                    points4gradeOptionalAssignments = points4gradeOptionalAssignments + points4assignment
    else:    # grade is based on how MANY assignments in an assignment group are done (not which specific ones)
        numCorrect = 0
        numLate = 0
        for result in results:
            if result.startswith('C') or result.startswith('L'):
                numCorrect = numCorrect + 1
            if result.startswith('L'):
                numLate += 1
        # points4grade = float(pointsPossibleTuple[numCorrect]) + (numLate * pointsPossibleTuple[-1])
        points4grade = float(pointsPossibleTuple[numCorrect-numLate]) + float(pointsPossibleTuple[numCorrect] - pointsPossibleTuple[numCorrect-numLate]) * latePenaltyPercentageDefault
    points4grade = round(points4grade,1)
    if points4grade == 0:
        pointsStr = 'MSG'
        pointsStrColor = bcolors.BOLD + bcolors.RED + ' MSG' + bcolors.ENDC
    elif points4grade <= pointsPossible * 0.70:
        pointsStr = str(points4grade)
        pointsStrColor = bcolors.BOLD + bcolors.RED + f'{str(points4grade):>4s}' + bcolors.ENDC
    elif points4grade <= pointsPossible * 0.80:
        pointsStr = str(points4grade)
        pointsStrColor = bcolors.BOLD + bcolors.CYAN + f'{str(points4grade):>4s}' + bcolors.ENDC
    elif points4grade <= pointsPossible * 0.90:
        pointsStr = str(points4grade)
        pointsStrColor = bcolors.BOLD + bcolors.BLACK + f'{str(points4grade):>4s}' + bcolors.ENDC
    else:
        pointsStr = str(points4grade)
        pointsStrColor = bcolors.BOLD + bcolors.GREEN + f'{str(points4grade):>4s}' + bcolors.ENDC
    return pointsStr, pointsStrColor
            
    

dateTime = datetime.now().strftime("%b_%d_%Hh%Mm%Ss")

while True:
    print('\nChoose 1 or more class periods')
    
    listOfDirectoriesInRootDir = [p.name for p in Path(rootDir).iterdir() if p.is_dir()]  # getting-a-list-of-all-subdirectories-in-the-current-directory

    for classPeriodName in listOfDirectoriesInRootDir:
        files = []
        if classPeriodName in classPeriodNames:
            print(f'  {bcolors.BOLD}({classPeriodNamesForMenu[classPeriodNames.index(classPeriodName)]}) class {classPeriodName}{bcolors.ENDC}')
    print(f'{bcolors.BOLD}  (x) EXIT{bcolors.ENDC}')
    
#     # pick class period(s()
#     num = 0
#     for period in classPeriods.keys():
#         print(f'  {period:2s} {classPeriods[period]}')
#     print('  x  to exit')
    userInput = input('Enter one or more period numbers (separate with space): ').strip()
    if userInput == 'x':
        exit() 
    elif not userInput == "":   # 2nd time through if user just hits enter use the same class period(s)
        periodsEntered = userInput.split()
    
    periodsPicked = []
    for period in periodsEntered:
        if period in classPeriodNamesForMenu:
            periodsPicked.append(classPeriodNames[classPeriodNamesForMenu.index(period)])        
    # print("DBG",periodsPicked)

    # pick assignment(s)
    print('Choose 0 or 1 or more assignments')
    num = 0
    print('  0 all the below assignments for a single student')
    assignmentsList = []
    for assignment in ASSIGNMENTS:    # ASSIGNMENTS is dictionary defined in grades4ACdata.py 
        value = ASSIGNMENTS[assignment]
        assignmentGroup = value[1]
        gradingTuple = value[2]
        assignmentTuples = gradingTuple[1:]
        assignmentNames = ''
        if assignmentGroup == 'CodingBat':
            assignmentNames = 'various'
        else:
            for assignmentTuple in assignmentTuples:
                assignmentNames += assignmentTuple[0] + ' '
            assignmentNames = assignmentNames.rstrip()       
        for period in periodsPicked:
#            print(f'DBG {ASSIGNMENTS=}')
#            print(f'DBG {assignment=} {ASSIGNMENTS[assignment][0]=}')
#            print(f'DBG {period=} {classPeriodNames=}')
           if ASSIGNMENTS[assignment][0] == classPeriods[period]:
               if assignment not in assignmentsList:
                   num = num + 1
                   print(f' {num:2d} {assignment:<20} ({assignmentNames})')
                   assignmentsList.append(assignment)
    userInput = input(f'Choose 0 or one or more 1-{num} (separate with space): ').strip()
    pickSingleStudent = False
    if userInput == '0':
        pickSingleStudent = True
        assignmentsPickedList = assignmentsList[:]                  
    else:
        assignmentsPicked = userInput.split(' ')
        assignmentsPickedList = []
        for pick in assignmentsPicked:
            assignmentsPickedList.append(assignmentsList[int(pick)-1])

    writeToGradesDir = True
    if not pickSingleStudent:    
        userInput = input('Write grade files to ' + gradesDir + ' (Enter=y)? ').strip();
        if not(userInput == '' or userInput.lower() == 'y'):
            writeToGradesDir = False

    printedStudents = False
                        
    foundWarnings = False
    for assignmentName in assignmentsPickedList:
        value = ASSIGNMENTS[assignmentName]
        assignmentGroup = value[1]
        gradingTuple = value[2]
        assignmentTuples = gradingTuple[1:]
        assignmentNames = ''
        if assignmentGroup != 'CodingBat':
            for assignmentTuple in assignmentTuples:
                assignmentNames += assignmentTuple[0] + ' '
            assignmentNames = assignmentNames.rstrip()
        singleStudentNames = []
        for period in periodsPicked:
            code2ID = {}
            registrationOrder = []
            numStudents = 0
            with open(Path(rootDir,period,'REGISTER.txt'), 'r') as reg:
                for line in reg:
                    if line.rstrip():
                        fields = line.strip().split()
                        if pickSingleStudent and not printedStudents:
                            numStudents = numStudents + 1
                            print(f'{numStudents:2d} {fields[1]} {fields[2]} {fields[0]}')
                            singleStudentNames.append(fields[1] + ' ' + fields[2]) 
                        if len(fields) == 6:
                            code2ID[fields[0]] = fields[5]
                        registrationOrder.append((fields[0], fields[1], fields[2],fields[5])) 
                if pickSingleStudent and not printedStudents:
                    userInput = input('Enter number of student: ').strip()
                    singleStudentName = singleStudentNames[int(userInput)-1]
            if (assignmentGroup == "CodingBat"):
                with open(Path(gradesDir,period + ' - ' + assignmentName + '_' + dateTime + '.txt'), "w") as gf:
                    gf.write("ID,"+assignmentName+'\n')
                # CODINGBAT
                with open(Path(codingBatDir,period + ' - ' + assignmentName + '.txt'), "r") as cb:
                    lineNum = 0
                    for line in cb:
                        correct = int(line.split()[2])
                        name = line.split()[-3:-1]
                        grade = gradingTuple[correct]
                        studentId = line.split()[-1]
                        with open(Path(gradesDir,period + ' - ' + assignmentName + '_' + dateTime + '.txt'), "a") as gf:
                            print(f' {grade} {name[0]} {name[1]} [{studentId}]')
                            #gf.write(str(registrationOrder[lineNum][3]) + ',' + str(gradingTuple[correct])+'\n')
                            gf.write(f'{studentId},{grade}\n')
                        lineNum += 1
            else:
                with open(Path(scoreboardDir,'annonymous',period,assignmentGroup + '.txt'), "r") as sb:
                    firstLine = sb.readline()
                    secondLine = sb.readline()
                    assignmentsFromScoreboard = secondLine.split()
                    assignmentsOnly = []
                    for assignment in assignmentsFromScoreboard:
                        assignmentsOnly.append(assignment[assignment.find(')')+1:])
                    assignmentNums = []
                    for assignmentTuple in assignmentTuples:
                        num = 1
                        for assignment in assignmentsOnly:
                            assignmentNameFromTuple = assignmentTuple[0]
                            if assignmentNameFromTuple.startswith('(opt)'):
                                assignmentNameFromTuple = assignmentNameFromTuple[5:]   # remove '(opt)' from beginning of the name, '(opt)' is only used in calcPointsForStudent()
                            if assignment == assignmentNameFromTuple:
                                assignmentNums.append(num)
                            num = num + 1
                    thirdline = sb.readline()
                    fourthline = sb.readline()
                    gradesDic = {}
                    for line in sb:
                        if line.startswith('TOTALS'):
                            break
                        student = line.split()
                        studentCode = student[0]
                        studentResult = []
                        for assignmentNum in assignmentNums:
                            studentResult.append(student[assignmentNum])
                        gradeStr,gradeStrColor = calcPointsForStudent(gradingTuple,studentResult)
                        #print(f'{studentResult=}')
                        if studentCode in code2ID:
                            gradesDic[studentCode] = (code2ID[studentCode],gradeStr,gradeStrColor,studentResult)
                        else:
                            foundWarnings = True
                            print(bcolors.BOLD + bcolors.RED + f'WARNING!!! Student code {studentCode} in scoreboard file not found in REGISTER.txt.' + bcolors.ENDC)
                            

                    if writeToGradesDir:
                        with open(Path(gradesDir,period + ' - ' + assignmentName + '_' + dateTime + '.txt'), "w") as gf:
                            gf.write("ID,"+assignmentName+'\n')
                            for registration in registrationOrder:
                                code = registration[0]
                                if code in gradesDic:
                                   gf.write(gradesDic[code][0] + ',' + gradesDic[code][1]+'\n')
                    #print(gradesDic)
                    print("\n******* Period " + period + ' ' + assignmentName + " (" + assignmentNames + ") *******")
                    #print(f'DBG {registrationOrder = }')
                    for registration in registrationOrder:
                        code = registration[0]
                        name = registration[1] + ' ' + registration[2]
                        #print(f'DBG {gradesDic = }')
                        if code in gradesDic:
                            attempts = ''
                            for attempt in gradesDic[code][3]:
                                attempts += f'{attempt:<3s}'                            
                            if pickSingleStudent:
                                if singleStudentName == name:
                                    print(f'{gradesDic[code][2]} ({attempts[:-1]}) {name}')
                            else:
                                print(f'{gradesDic[code][2]} ({attempts[:-1]}) {name}')
                        else:
                            print(f'WARNING!!! No result found in scoreboard for {code} in REGISTER.txt ({name = })')
                    print("^^^^^^^ Period " + period + ' ' + assignmentName + " (" + assignmentNames + ") ^^^^^^^")


        printedStudents = True
    if foundWarnings:
         print(bcolors.BOLD + bcolors.RED + f'WARNINGS found above (have a look)' + bcolors.ENDC)                
    foundWarnings = False
                

