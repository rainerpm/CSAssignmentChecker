# programs
pythonIde = r'C:/Users/E151509/AppData/Local/Programs/Python/Python312/Lib/idlelib/idle.pyw'
javaIde = r'C:/Program Files (x86)/jGRASP/bin/jgrasp.exe'      
textEditor = r'C:/Program Files/Notepad++/notepad++.exe'
diffPgm = r'C:/Program Files/WinMerge/WinMergeU.exe'

# directories
rootDir = r'C:/Users/E151509/My Drive (rainer.mueller@austinisd.org)/CSAC/StudentSubmissions/2024-25'
#rootDir = r'C:/Users/E151509/Dropbox/Apps/StudentFiles'
#rootDir = r'C:/Users/E151509/Downloads/demo/demo'
#scoreboardDir = r'C:/Users/E151509/Google Drive/Course Materials/Introduction to Computer Science/10.Python/scoreboard'
#scoreboardDirAlt = r'C:/Users/E151509/My Drive/Course Materials/Introduction to Computer Science/10.Python/scoreboard'
scoreboardDir = r'C:/Users/E151509/My Drive/My LASA/scoreboard'
#scoreboardDir = r'C:/Users/E151509/Downloads/demo/demo/scoreboard_for_demo'
#mossDir = r'C:/Users/E151509/My Drive/My LASA/misc/tools/plagiarize checking'

# java and python class periods
classPeriodNames = ["P3","P5","P6","P8","Contests"]
classPeriodNamesForMenu = ["3","5","6","8","C"]  # list of class names (shortened to make them easier to pick from the menu)

javaAssignmentGroups = [#"JAVA_01_WritingAndCallingMethods",
                        #"JAVA_02_Objects1",
                        #"JAVA_03_Objects2",
                        #"JAVA_04_Semester2A",
                        #"JAVA_05_FR_Practice1",
                        #"JAVA_06_Semester2B",
                        #"JAVA_07_FR_Practice2",
                        #"JAVA_08_FR_Practice3",
                        #"JAVA_09_Post_AP"
                       ]
pythonAssignmentGroups = ["PYTHON_01_FirstAssignments",
                          "PYTHON_02_Lets_Get_Loopy",
                          #"PYTHON_03_SecondAssignments",
                          #"PYTHON_04_ThirdAssignments",
                          #"PYTHON_05_FourthAssignments",
                          #"PYTHON_06_SecondChallenges",
                          #"PYTHON_07_ThreeProblems",
                          #"PYTHON_08_Programming_Quiz",
                          #"PYTHON_09_ProgrammingFinal2024"
                         ]
contestAssignmentGroups = [# "2018_UIL_District",
                           # "2018_UIL_Regional",
                           # "2021_UIL_District",
                           # "2022_UIL_District",
                           # "2023_UIL_District",
                           # "2024_Indeed"
                          ]
classAssignmentGroups = {}
classAssignmentGroups["P3"] = pythonAssignmentGroups
classAssignmentGroups["P5"] = pythonAssignmentGroups
classAssignmentGroups["P6"] = pythonAssignmentGroups
classAssignmentGroups["P8"] = pythonAssignmentGroups
classAssignmentGroups["Contests"] = contestAssignmentGroups

# email (email login is in login.py)
emailSignature = "\nMr. Mueller\n"
emailAttachmentDir = r"C:/Users/E151509/Documents/"
# if set to False all sent email will end up in the Outlook 'Sent Items' folder
# Set to True only if you have created the folder 'CSAC' inside your 'Sent Items' folder
emailUseClassPeriodSentFolders = True  

# timeout (default time in seconds for student assignment to time out - protects against endless loops
TIMEOUT_DEFAULT = 5

# days not to count for assignment's days late calculation
schoolHolidays = []
schoolHolidays.append('2024-09-02')           # Holiday
schoolHolidays.append('2024-10-03')           # PD Day
schoolHolidays.append('2024-10-04')           # PLED Day
schoolHolidays.append('2024-10-14')           # PD Day
schoolHolidays.append('2024-11-01')           # Holiday
schoolHolidays.append('2024-11-05')           # PD Day
for i in range(25, 29+1):                     # Thanksgiving Week (+1 since range function goes up to but not including last one)
    schoolHolidays.append(f'2024-11-{i:02}')  # Thanksgiving Week
for i in range(23, 31+1):                     # ChristmasBreak
    schoolHolidays.append(f'2024-12-{i:02}')  # ChristmasBreak
for i in range(1, 3+1):                       # ChristmasBreak
    schoolHolidays.append(f'2024-01-{i:02}')  # ChristmasBreak
schoolHolidays.append('2024-01-06')           # PD Day
schoolHolidays.append('2024-01-20')           # Holiday
schoolHolidays.append('2024-01-29')           # PD Day
schoolHolidays.append('2024-02-17')           # PD Day
schoolHolidays.append('2024-03-14')           # PLED Day
for i in range(17, 21+1):                     # Spring Break Week
    schoolHolidays.append(f'2024-03-{i:02}')  # Spring Break Week
schoolHolidays.append('2024-03-31')           # Holiday
schoolHolidays.append('2024-04-18')           # PD Day
schoolHolidays.append('2024-05-26')           # Holiday
schoolHolidays.append('2024-05-30')           # PD Day

