# java and python class periods
validClassPeriods = ["1","6","7","8","9"]

# days not to count for assignment's days late calculation
schoolHolidays = []
schoolHolidays.append('2023-09-04')           # Holiday
schoolHolidays.append('2023-09-25')           # PD Day
schoolHolidays.append('2023-10-02')           # PD Day
schoolHolidays.append('2023-11-13')           # PD Day
for i in range(20, 24+1):                     # Thanksgiving Week
    schoolHolidays.append(f'2023-11-{i:02}')  # Thanksgiving Week
for i in range(21, 31+1):                     # ChristmasBreak
    schoolHolidays.append(f'2023-12-{i:02}')  # ChristmasBreak
for i in range(1, 8+1):                       # ChristmasBreak
    schoolHolidays.append(f'2024-01-{i:02}')  # ChristmasBreak
schoolHolidays.append('2024-01-15')           # Holiday
schoolHolidays.append('2024-02-09')           # PD Day
schoolHolidays.append('2024-02-19')           # Holiday
for i in range(11, 15+1):                     # Spring Break Week
    schoolHolidays.append(f'2024-03-{i:02}')  # Spring Break Week
schoolHolidays.append('2024-03-29')           # Holiday
schoolHolidays.append('2024-04-10')           # PD Day
    
# programs
pythonIde = r'C:/Users/E151509/AppData/Local/Programs/Python/Python311/Lib/idlelib/idle.pyw'
javaIde = r'c:/Program Files (x86)/jGRASP/bin/jgrasp.exe'      
textEditor = r'c:/Program Files/Notepad++/notepad++.exe'
diffPgm = r'C:\Program Files (x86)\WinMerge\WinMergeU.exe'

# directories
rootDir = r'C:/Users/E151509/Dropbox/Apps/StudentFiles'
#rootDir = r'C:\Users\E151509\Downloads\demo\demo'
#scoreboardDir = r'C:/Users/E151509/Google Drive/Course Materials/Introduction to Computer Science/10.Python/scoreboard'
#scoreboardDirAlt = r'C:/Users/E151509/My Drive/Course Materials/Introduction to Computer Science/10.Python/scoreboard'
scoreboardDir = r'C:\Users\E151509\My Drive\My LASA\scoreboard'
#scoreboardDir = r'C:\Users\E151509\Downloads\demo\demo\scoreboard_for_demo'
mossDir = r'C:\Users\E151509\My Drive\My LASA\misc\tools\plagiarize checking'

# email (email login is in login.py)
emailSignature = "\nMr. Mueller\n"
emailAttachmentDir = r"C:/Users/E151509/Documents/"
# if set to False all sent email will end up in the Outlook 'Sent Items' folder
# Set to True only if you have created the folder 'CSAC' inside your 'Sent Items' folder
emailUseClassPeriodSentFolders = True  


# timeout (default time in seconds for student assignment to time out - protects against endless loops
TIMEOUT_DEFAULT = 5


##### For Demo (simply uncomment the below, leave above alone)
##validClassPeriods = ["1","4","5"]
##rootDir = r'C:/Users/E151509/Downloads/demo'
##scoreboardDir = r'C:/Users/E151509/Downloads/demo/scoreboard'
##emailSignature = "/nYour Teacher/n"
##emailAttachmentDir = r"C:/Users/E151509/Downloads"
