gradesDir = r'C:\Users\E151509\My Drive\My LASA\misc\tools\Grades2Teams'
codingBatDir = r'C:\Users\E151509\My Drive (rainer.mueller@austinisd.org)\CSAC\StudentSubmissions\2024-25\scoreboard\CodingBat'

# maps the class name from the classPeriodNames list in CSACcustomize.py to the class name used in ASSIGNMENTS dictionary below
classPeriods = { 'P3' : 'Fundamentals',
                 'P5' : 'Fundamentals',
                 'P6' : 'Fundamentals',
                 'P8' : 'Fundamentals'
               }

latePenaltyPercentageDefault = 0.70   # programs flagged as late are worth this percentage of the points

# ASSIGNMENTS dictionary
# key = Grade Book name
# value = (class, assignment group, gradingTuple)
#    gradingTuple = (pointsPossible,assignmentTuple1,assignmentTuple2,...)
#       * points possible is a integer number for the total points of assignment group OR
#         a tuple representing the points for assignments where grading is based on how many assignments in the assignment group are completed: 1st tuple element is points for 0 completed, 2nd is for 1 completed, 3rd is for 2 completed, ...
#       * each assignmentTuple = assignmentName, percentOfAssignment (integer or float - see note about optional assignmetns below),[optional: percentDeductionForIncorrectSubmission]
#       * example 1  (10,('calculator',100))  a 10pt assignment called calculator
#       * example 2  (20,('pgm1a',80),('pgm1b',15),('pgm1c',5))    pgm1a correct is 80% (i.e. 16pts), pgm1a & pgm1b correct is 95%=80%+15%, pgm1a,pgm1b,pgm1c correct is 100%=80%+15%+5%
#       * example 3  (20,('pgm1a',80,10),('pgm1b',15),('pgm1c',5)) same as above except that 2pts (10% of 20pts) are deducted for every incorrect submission of pgm1a    
#       * example 4  ((0,7.5,9,10.5,12,13.5,15),('pgm1a',),('pgm1b',),('pgm1c',),('pgm1d',),('pgm1e',),('pgm1f',))   6 total programs 0 correct = 0 pts,  1 correct = 7.5pts, 2=9pts, 3=10.5pts, ...
#                                                       NOTE: A tuple with a single element requires a , after the element
# A note about optional assigments
#   Assignments can be optional and their points are counted if a later part of the assignment is correct.
#   Optional assignments are indicated by adding the string '(opt)' to the front of the assignment name.
ASSIGNMENTS = {
#graded with manual checkoff 'CodingBat Warmup'         : ('Fundamentals','CodingBat',(0,2,3,4,5)),
#'Introduction to Thonny'   : ('Fundamentals','PYTHON_01_FirstAssignments',(5,('introduction',100))),
#'Heat Index'               : ('Fundamentals','PYTHON_01_FirstAssignments',(10,('heat',100))),
#'CodingBat Logic'          : ('Fundamentals','CodingBat',(0,1,2,3)),
#'Calculator'               : ('Fundamentals','PYTHON_01_FirstAssignments',(10,('calculator',100))),
'Fuel Economy'             : ('Fundamentals','PYTHON_01_FirstAssignments',(5,('fuel',100))),
#'CodingBat Berlin Wall'    : ('Fundamentals','CodingBat',(0,1,2,3)),
'Using Functions'          : ('Fundamentals','PYTHON_01_FirstAssignments',(10,('heat2',100))),
'While loops'              : ('Fundamentals','PYTHON_01_FirstAssignments',(3,('while',100))),
'For loops'                : ('Fundamentals','PYTHON_01_FirstAssignments',(4,('for',100,12.5))),  # deduct 1/2 point (12.5%) for every incorrect submission
'Booleans decisions loops' : ('Fundamentals','PYTHON_01_FirstAssignments',(10,('bdl',100))),
'Lets get loopy'           : ('Fundamentals','PYTHON_02_Lets_Get_Loopy',((0,9,15,21,24,25.5,27,27.9,28.8,29.4,30,31.5,33,34.5),('01sal',),('02fib',),('03days',),('04agtb',),('05pi',),('06collatz',),('07power',),('08triplet',),('09polter',),('10champ',),('11area',),('12flip',),('13coin',))),
#'Strings'                  : ('Fundamentals','PYTHON_01_FirstAssignments',(5,('strings1',100,10),('strings2',40))),  # deduct 1/2 point (10%) for strings1, string2 is a bonus of 2 pts (or 40% of 5 points)
# 'Ciphers'                  : ('Fundamentals','PYTHON_03_SecondAssignments',(15,('caesar',90),('vigenere',10))), 
# 'Files'                    : ('Fundamentals','PYTHON_03_SecondAssignments',(4,('files1',70),('files2',10),('files3',10),('files4',10),('files5',25))), 
#'Register & Login'         : ('Fundamentals','PYTHON_03_SecondAssignments',(15,('pw0',70),('pw1',15),('pw2',15),('pwbonus0',6.7),('pwbonus1',6.7))), 
#'List Introduction'        : ('Fundamentals','PYTHON_03_SecondAssignments',(5,('list1',80,12.5),('musical',20))),   # deduct 1/2 point (12.5%) for every incorrect list1 submission
#'Student Grades'           : ('Fundamentals','PYTHON_04_ThirdAssignments',(10,('grades1',90),('grades2',10),('letters',20))),
#'First Challenges'         : ('Fundamentals','PYTHON_04_ThirdAssignments',((0,5,10,15,18,20,22),('aftest',),('artest',),('elevator',),('climb',),('microwave',),('tgencrypt',))),
#'Dictionary Introduction'  : ('Fundamentals','PYTHON_05_FourthAssignments',(5,('contacts',70),('dictionary1',30),('sharedBirthday',40))),
#'EV Analysis'              : ('Fundamentals','PYTHON_05_FourthAssignments',(15,('evanalysis0',50),('evanalysis1',20),('evanalysis2',10),('evanalysis3',10),('evanalysis4',10),('astronauts',20))),
#'More Student Grades'      : ('Fundamentals','PYTHON_05_FourthAssignments',(10,('grades3',100))),
#'Tuple labs'               : ('Fundamentals','PYTHON_05_FourthAssignments',(10,('(opt)states1',70),('states2',10),('baseball',20))),   #
#'More tuples'              : ('Fundamentals','PYTHON_05_FourthAssignments',(10,('prime',70),('picture1',10),('picture2',10),('picture3',10),('distances1',30),('distances2',10))),
#'Indeed 2024'              : ('Fundamentals','2024_Indeed',((0,5,10,14,16,18,19,20,20,22,22,23,23,24,25,26,27),('Aplusflex',),('Better',),('Buzz',),('Check',),('Coins',),('Compare',),('Determined',),('Encryption',),('Jewels',),('Lisp',),('Middle',),('Partitions',),('Pispeech',),('Postfix',),('Wall',),('Yahtzee',))),
#'Programming Quiz'         : ('Fundamentals','PYTHON_08_Programming_Quiz',(10,('(opt)quiz1',50),('(opt)quiz2',20),('(opt)quiz3',10),('(opt)quiz4',10),('(opt)quiz5',10),('(opt)quiz6',10))),
#'Python Final 2024'         : ('Fundamentals','PYTHON_09_ProgrammingFinal2024',(100,('helloSummer',70),('water',10),('tribonacci',10),('distinct',10))),
#'Second Challenges'        : ('Fundamentals','PYTHON_06_SecondChallenges',((0,10,14,16,17,18,19,20),('snap',),('fence',),('points',),('palinum',),('yoda',),('ocr',),('independence',))),
#'Three Bonus Problems'     : ('Fundamentals','PYTHON_07_ThreeProblems',((0,1,2,3),('supersum',),('summation',),('radical',))),
##########################################################################################################    
#'Hello World'            : ('AP','JAVA_00_FirstAssignments',(3,('Hello',100))),
#'Hello World Plus'       : ('AP','JAVA_00_FirstAssignments',(3,('HelloPlus',100))),
#'First Practice'             : ('AP','JAVA_00_FirstAssignments',(10,('FirstPractice',100))),
#'User Input'                 : ('AP','JAVA_00_FirstAssignments',(5,('UserInput',100,10.0))),   # -1/2 point (10%  of 5 points) for every incorrect submission
#'Methods Part 1'             : ('AP','JAVA_01_WritingAndCallingMethods',(10,('Rounding',50),('GallonsWasted',20),('BeanCount',20),('RandomStatement',10))),
#'Methods Part 2'             : ('AP','JAVA_01_WritingAndCallingMethods',(10,('Tasking',70),('Invocations',30))),
#'CodingBat String Exercises' : ('AP','CodingBat',(0,1,2,3,4,5,6,7,8,8.5,9.5,9.7,10)),
#'String Methods'             : ('AP','JAVA_01_WritingAndCallingMethods',(2,('StringMethods',100,25.0))),  # -1/2 point (25% of 2 points) 
#'Dice'                       : ('AP','JAVA_02_Objects1',(5,('Dice',100))),   
#'Book & StudentId'           : ('AP','JAVA_02_Objects1',(15,('Book',80),('StudentId',20))),
#'InOrderColors'              : ('AP','JAVA_02_Objects1',(10,('InOrderColors',100))),
#'CodingBat Logic Exercises'  : ('AP','CodingBat',(0,3,4,5,6,8,10,12,12.5,12.8,13.2,13.5,14.0,14.3,14.7,15,15)),
#'Calculator & Quadratic'      : ('AP','JAVA_02_Objects1',(10,('Calculator',90),('Quadratic',10))),
#'Robot Simulation & GCD'      : ('AP','JAVA_02_Objects1',(10,('Robot',90),('GCD',20))),
#'Deal'                     : ('AP','JAVA_03_Objects2',(15,('Deal',100))),
#'Phrase & Pictures'          : ('AP','JAVA_02_Objects1',(15,('Phrase',80,4.2),('Baboon',10),('Peppers',10),('Illusion1',6.67),('Illusion2',6.67),('Illusion3',6.67))),   # 4.2% of 80% of 15 = 0.5 pts, 6.67% of 15 = 1 pt
#'Collatz'                    : ('AP','JAVA_03_Objects2',(15,('Collatz',100,6.67))),   # 6.67% of 15 = 1 pt
#'UserAccess'                 : ('AP','JAVA_03_Objects2',(15,('(opt)UserAccess0',70),('(opt)UserAccess1',15),('UserAccess2',15),('UserEnglish',6.67),('UserPassword',6.67))),
#'WordSearch'               : ('AP','JAVA_03_Objects2',(15,('(opt)WordSearch80',80),('(opt)WordSearch90',10),('WordSearch100',10))),
#'CodingBat Array Exercises'  : ('AP','CodingBat',(0,4,6,7,8,9,10,11,12,13,14,15)),
#'Vigenere'                  : ('AP','JAVA_03_Objects2',(10,('(opt)Vigenere0',90),('Vigenere1',10))),
#'PlayList'                  : ('AP','JAVA_03_Objects2',(15,('PlayList',100))),
#'UIL 2018 Hands On'        : ('AP','2018_UIL_District',((0,8,9,10,11,12,13,14,15,16,17,18,19),('Alice',),('Bayani',),('Candela',),('Carla',),('Diya',),('Gleb',),('Jeremy',),('Kinga',),('Layla',),('Max',),('Nandita',),('Raymond',))),
#'UIL Hands On'              : ('AP','2022_UIL_District',((0,5,7,9,10,10.5,11,11.5,12,12.5,13,13.5,14),('Adrian',),('Arusha',),('Catherine',),('Diane',),('Facundo',),('Haru',),('Kristina',),('Lavanya',),('Manos',),('Michaela',),('Pankaj',),('Shirley',))),
#'ArrayLists'                : ('AP','JAVA_04_Semester2A',(15,('NumberJumble',70),('Library',30))),
#'Card'                      : ('AP','JAVA_04_Semester2A',(10,('Card',100))),
#'Deck'                      : ('AP','JAVA_04_Semester2A',(10,('Deck',100,5.0))),   # -1/2 point (5% of 10 points) for every incorrect submission
#'Players'                   : ('AP','JAVA_04_Semester2A',(15,('Player',50),('CardPlayer',50))),
#2024-25 'Players'                   : ('AP','JAVA_04_Semester2A',(15,('Player',50),('CardPlayer',50,6.67))),  # -1/2 point (6.67% of 7.5 points) for every incorrect submission
#'CardPlayerLevel1'          : ('AP','JAVA_04_Semester2A',(10,('CardPlayerLevel1',100))),
#2024-25  'CardPlayerLevel1'         : ('AP','JAVA_04_Semester2A',(10,('CardPlayerLevel1',100,5.0))),   # -1/2 point (5% of 10 points) for every incorrect submission
#'CardGame'                  : ('AP','JAVA_04_Semester2A',(15,('CardGame',100))),
#'CardShark'                 : ('AP','JAVA_04_Semester2A',(5,('(opt)CardPlayerLevel2',70),('CardPlayerLevel3',30),('CardPlayerBonus',40))),
#'CodingBat LASA Drills 01'  : ('AP','CodingBat',(0,1,2,3,4,5)),
# 'FR Practice 1'             : ('AP','JAVA_05_FR_Practice1',((0,6,8.4,9.6,10.8,11.4,12),('RandomStringChooser',),('RandomLetterChooser',),('LogMessage',),('SystemLog',),('Crossword',),('StringFormatter',))),
# 'CodingBat Recursion'       : ('AP','CodingBat',(0,7,8,10)),    # manually double check 10 grade to make sure they also have a 1 in AntClimb
# 'AntClimb'                  : ('AP','JAVA_06_Semester2B',(1,('AntClimb',100))),
# 'MergeSort and QuickSort'   : ('AP','JAVA_06_Semester2B',((0,7,10),('MergeSort',),('QuickSort',))),
# 'FR Practice 2'             : ('AP','JAVA_07_FR_Practice2',((0,5.6,6.8,8),('MusicDownloads',),('TokenPass',),('SkyView',))),
# 'FR Practice 3'             : ('AP','JAVA_08_FR_Practice3',((0,7,8.5,10),('Scramble',),('SeatingChart',),('Trio',)))
}