# beginning of the year
#   * remove the class directories from the previous year
#     - also remove the (now empty) directories in the dropbox app/website.
#   * delete all directories/files in the scoreboard directory

import CSACscoreboard  # import the associated CSACscoreboard.py which creates the scoreboard files
from CSACscoreboard import assignmentResults    
from CSACcustomize import classPeriodNames,classPeriodNamesForMenu,classPeriodEmailYN,classAssignmentGroups,rootDir,scoreboardDir,pythonIde,javaIde,schoolHolidays,diffPgm,textEditor,emailSignature,emailAttachmentDir, emailUseClassPeriodSentFolders, TIMEOUT_DEFAULT

minimizeFilesCreated = True

# import python libraries
import os               # module is in python standard library 
import glob             # module is in python standard library
import subprocess       # module is in python standard library
import re               # module is in python standard library
import time             # module is in python standard library
import sys              # module is in python standard library
import signal           # module is in python standard library
import json             # module is in python standard libraryy

import zipfile
from   datetime import datetime  # module is in python standard library
from   datetime import date      # module is in python standard library
from   numpy    import busday_count   # pip install numpy (Thonny install numpy package)
from   pathlib  import Path      # module is in python standard library
from   shutil   import move  # module is in python standard library
from   shutil   import copyfile  # module is in python standard library
from   shutil   import copy      # module is in python standard library
from   shutil   import rmtree    # module is in python standard library
import ssl              # module is in python standard library
import smtplib          # module is in python standard library
from   email.mime.text      import MIMEText      # module is in python standard library
from   email.mime.multipart import MIMEMultipart # module is in python standard library
from   email.mime.base      import MIMEBase      # module is in python standard library
from   email                import encoders      # module is in python standard library
from   PIL      import ImageGrab                 # pip install pillow  (Thonny install pillow package)
import win32com.client  # pip install pywin32 (close and reopen Python after install) [for email using Outlook Windows 10 app (https://github.com/mhammond/pywin32)] (Thonny install pywin32 package)          
import pyperclip        # pip insall pyperclip (allows python to add things to the clipboard (so it can be quickly pasted)  (Thonny install pyperclip package)
#from icecream import ic
import webbrowser           # module is in python standard library
import os                   # module is in python standard library
# from twilio.rest import Client  # pip install twilio (Thonny install twilio)
# to get the line number of a Python statement
from inspect import currentframe, getframeinfo  # module is in python standard library
from math import ceil

if 'idlelib.run' in sys.modules:   # colors do not work in IDLE
    class bcolors:
        HEADER,BLUE,CYAN,GREEN,WARNING,RED,ENDC,BOLD,UNDERLINE,LIGHTGRAY,ORANGE,BLACK,BGGREEN,BGRED,BGYELLOW,BGCYAN = '','','','','','','','','','','','','','','',''
else:
    class bcolors:
        HEADER,BLUE,CYAN,GREEN,WARNING,RED,ENDC,BOLD,UNDERLINE,LIGHTGRAY,ORANGE,BLACK,BGGREEN,BGRED,BGYELLOW,BGCYAN = '\033[95m','\033[94m','\033[96m','\033[92m','\033[93m','\033[91m','\033[0m','\033[1m','\033[4m','\033[37m','\033[33m','\033[30m','\033[42m','\033[41m','\033[43m','\033[46m'

validFileExtensions = [".py",".java",".zip",".txt"] # .py for python, .java/.zip for java, .txt for counting submissions (i.e. *_CORRECT.txt)

# Check variables set in customize.py
initError = False

if not Path(rootDir).is_dir():
    initError = True
    print(f"{bcolors.RED}Error!!!{bcolors.ENDC} root directory does not exist (" + rootDir + ")")
else:
    if not Path(rootDir,"ASSIGNMENT_GROUPS").is_dir():
        initError = True
        print(f"{bcolors.RED}Error!!!{bcolors.ENDC} ASSIGNMENT_GROUPS directory does not exist in " + rootDir)

if not Path(scoreboardDir).is_dir():
    initError = True
    print(f"{bcolors.RED}Error!!!{bcolors.ENDC} scoreboard directory does not exist @" + scoreboardDir)
        
if not Path(emailAttachmentDir).is_dir():
    initError = True
    print(f"{bcolors.RED}Error!!!{bcolors.ENDC} email attachment directory does not exist @" + emailAttachmentDir)  

if pythonIde:
    if not Path(pythonIde).is_file(): 
        initError = True
        print(f"{bcolors.RED}Error!!!{bcolors.ENDC} Python IDE not found @ " + pythonIde)
else:
    print("WARNING!! No Python IDE was specified")

if javaIde:
    if not Path(javaIde).is_file():
        initWarning = True
        print(f"{bcolors.RED}Error!!!{bcolors.ENDC} JAVA IDE not found @ " + javaIde)
else:
    print("WARNING!! No JAVA IDE was specified")      

if not Path(diffPgm).is_file():
    initError = True
    print(f"{bcolors.RED}Error!!!{bcolors.ENDC} Diff program not found @ " + diffPgm)

if not Path(textEditor).is_file():
    initError = True
    print(f"{bcolors.RED}Error!!!{bcolors.ENDC} TextEditor not found @ " + textEditor)
textEditorCmdOpt1 = [textEditor,r'-nosession',r'-multiInst',r'-n1000000']

# customDirectoryForUILComp specifies a directory that students submit program competition files to.
# This program then moves the submitted programs to Period 9 and treats them like they are from a regular class at that point.
customDirectoryForUILComp = r'C:\Users\E151509\My Drive\Programming Competitions\LASA{CS} UIL Practice (CSAC)\UIL Practice (Spring 2024)'
classPeriodForCompetitions = 9
if not Path(customDirectoryForUILComp).is_dir():
    customDirectoryForUILComp = None   

### REGISTRATION
registrationRequired = True

# due dates
assignmentDueDateGlobal = {}
if os.path.exists(Path(rootDir,"dueDates.txt")):
    with open(Path(rootDir,"dueDates.txt"), "r") as dd:
        for line in dd:
            if line.lstrip().startswith("#"):
                continue
            fields = line.split()
            dateField = fields[0]
            assignmentFields = fields[1:]
            for assignmentField in assignmentFields:
                assignmentDueDateGlobal[assignmentField] = dateField

# Use Ctrl-C to stop waiting for new submissions
def signal_handler(signal, frame):
    # print("signal handler")
    global interrupted
    interrupted = True

signal.signal(signal.SIGINT, signal_handler)

def check4Activity():
    print(f'\n{bcolors.BOLD}{bcolors.BLUE}*** Checking for new submissions ***{bcolors.ENDC}')
    listOfDirectoriesInRootDir = [p.name for p in Path(rootDir).iterdir() if p.is_dir()]  # getting-a-list-of-all-subdirectories-in-the-current-directory
    validClassPeriodDirs = []
    for classPeriodName in classPeriodNames:
        if classPeriodName in listOfDirectoriesInRootDir:
            validClassPeriodDirs.append(classPeriodName)
    for classPeriodName in validClassPeriodDirs:
        files = []
        print(f'{bcolors.BOLD}({classPeriodNamesForMenu[classPeriodNames.index(classPeriodName)]}) Submissions for {classPeriodName}{bcolors.ENDC}')
        files =[p for p in Path(rootDir,classPeriodName).iterdir() if p.is_file()]
        for file in files:
           if file.name != "REGISTER.txt":
              if file.suffix not in validFileExtensions:
                 print(" ","File with incorrect extension",">" + file.name + "<")
              else:
                 print(" ", datetime.fromtimestamp(file.stat().st_mtime).strftime("%b%d %Hh%Mm"), ">"+file.name+"<")
        if os.path.isdir(Path(rootDir,classPeriodName,"00ManualCheck")):         
            files =[p for p in Path(rootDir,classPeriodName,"00ManualCheck").iterdir() if p.is_file()]
            for file in files:
               print("  ..", "manual check -> ", datetime.fromtimestamp(file.stat().st_mtime).strftime("%b%d %Hh%Mm"), ">"+file.name+"<")               
                
# return a dictionary of all registered students and create student directory
# if it does not yet exist
def loadRegisteredStudents(classRootDir,assignmentGroups):
    classRegistration = {}
    if Path(classRootDir,"REGISTER.txt").is_file():
        with open(Path(classRootDir,"REGISTER.txt"), "r") as freg:
            for line in freg:
                line = line.rstrip()
                if not line:
                    continue
                fields = line.split()
                email = ""
                studentId = ""
                if len(fields) == 4:  # if registration does not have email
                    code, name, classPeriod = fields
                elif len(fields) == 5:
                    code, nameLast, nameFirst, classPeriod, email = fields
                elif len(fields) == 6:
                    code, nameLast, nameFirst, classPeriod, email, studentId = fields
                name = nameLast + " " + nameFirst
                if code.isdigit():
                    if code not in classRegistration:
                        classRegistration[code] = (name, classPeriod, email)
                        # check if the student directory for each registered student exists in every assignment group of the class
                        aKeys = list(assignmentGroups.keys())
                        aKeys.sort()
                        for aGroupId in aKeys:
                            aDict = assignmentGroups[aGroupId]
                            aGroupDir = aDict["assignmentGroupDir"]
                            studentDir = Path(aGroupDir,name + "_" + code)
                            if not Path(studentDir).is_dir():
                                Path(studentDir).mkdir()
                                print("  created student dir", studentDir.parent.name + '/' + studentDir.name)
                    else:
                        print(f'{bcolors.RED}Error!!!{bcolors.ENDC} Student code >' + code + '< in REGISTER.txt exists more than one time.') 
                else:
                    print(f'{bcolors.RED}Error!!!{bcolors.ENDC} Student code >' + code + '< in REGISTER.txt does NOT contain only digits.')
    return classRegistration

def setup():
    allAssignmentGroups = {}
    allAssignments = {}
    # new in July 2024
    for classPeriodName in classPeriodNames:
        classPeriodsDir = os.path.join(rootDir,classPeriodName)
        if not os.path.isdir(classPeriodsDir):
            os.mkdir(classPeriodsDir)
            print("Created directory",classPeriodsDir)
        for classAssignmentGroup in classAssignmentGroups[classPeriodName]:
            globalAssignmentGroupDir = os.path.join(rootDir,"ASSIGNMENT_GROUPS",classAssignmentGroup)
            classAssignmentGroupDir = os.path.abspath(os.path.join(rootDir,classPeriodName,classAssignmentGroup))  # abspath necessary to open file explorer for main menu 'f' option
            if not os.path.isdir(classAssignmentGroupDir):
                os.mkdir(classAssignmentGroupDir)
                print("Created directory",classAssignmentGroupDir)
            latestResultsDir = os.path.join(rootDir,classPeriodName,"00LatestResults")
            if not os.path.isdir(latestResultsDir):
                os.mkdir(latestResultsDir)
                print("Created directory",latestResultsDir)
            autoJudgeManualCheckDir = os.path.join(rootDir,classPeriodName,"00ManualCheck")
            if not os.path.isdir(autoJudgeManualCheckDir):
                os.mkdir(autoJudgeManualCheckDir)                
                print("Created directory",autoJudgeManualCheckDir)
            plagiarismDir = os.path.join(classAssignmentGroupDir,"00PLAGIARISM")
            if not os.path.isdir(plagiarismDir):
                os.mkdir(plagiarismDir)                
                print("Created directory",plagiarismDir)
            assignmentGroup = {}  # create content dict, then add to it
            assignmentGroup["assignmentGroupDir"] = classAssignmentGroupDir
            assignmentGroup["goldenDir"] = globalAssignmentGroupDir   # this is in the GLOBAL assignment group directory
            assignmentGroup["plagiarismDir"] = plagiarismDir
            assignments = {}
            assignmentGroups = {}
            listOfAssignments = [f.name for f in os.scandir(globalAssignmentGroupDir) if f.is_dir()]  # https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
            # now using 'INACTIVE' folder for assignments in an assignment group that I am not currently using
            #listOfAssignments = [s for s in listOfAssignments if not s.startswith("IGNORE")]
            listOfAssignments.sort()
            assignmentGroup["listOfAssignments"] = listOfAssignments
            for assignment in listOfAssignments:
                assignments[assignment] = classAssignmentGroup
            assignmentGroups[classAssignmentGroup] = assignmentGroup
            if classPeriodName in allAssignmentGroups:
                allAssignmentGroups[classPeriodName].update(assignmentGroups)
            else:
                allAssignmentGroups[classPeriodName] = assignmentGroups
            if classPeriodName in allAssignments:
                allAssignments[classPeriodName].update(assignments)
            else:
                allAssignments[classPeriodName] = assignments
    return allAssignmentGroups, allAssignments

def emailStudent(submission, comment='',attach=True):
    emailCodes = []
    if submission["groupSubmission"]:
        print("  Group submission.  Choose student(s) to send email to.")
        choice = 1
        validResponses = ['']
        for code in submission["groupCodes"]:
            print("    (" + str(choice) + ") " + submission["classRegistration"][code][0])
            validResponses.append(str(choice))
            choice = choice + 1
        response = input("  Choose (1-"+str(choice-1)+") (" + bcolors.BLUE + '<ENTER>=all' + bcolors.ENDC + ")? ")
        while response not in validResponses:
           response = input("  Choose (1-"+str(choice-1)+") (" + bcolors.BLUE + '<ENTER>=all' + bcolors.ENDC + ")? ")
        if response == '':
            emailCodes = submission["groupCodes"]
        else:
            emailCodes = [submission["groupCodes"][int(response)-1]]
    else:
        if "studentCode" in submission:
           emailCodes = [submission["studentCode"]]
        else:
           print(f'{submission["classRegistration"]=}')
           classRegistrationInOrder = sorted(submission["classRegistration"], key=submission["classRegistration"].get, reverse=False)
           print(f'{classRegistrationInOrder=}')
           num = 0
           for student in classRegistrationInOrder:
               num = num + 1
               print(f'{num:2d} {submission["classRegistration"][student][0]}')
           userInput = input("Enter one or more students (separate with space): ").strip()
           emailCodes = []
           for studentSel in userInput.split():
               lstIdx = int(studentSel) - 1
               emailCodes.append(classRegistrationInOrder[lstIdx])
           print(f'{emailCodes=}')    
    receiverEmailAddress = ""
    subject = f'{submission["classPeriod"]} CSAC Submission ({submission["Assignment"]} - {submission["submissionDateTime"]})'
    if submission["invalidAssignment"]:
        comment = f'"{submission["Assignment"]}" is an incorrect assignment name. Please resubmit with the correct assignment name.'
        incorrectAssignmentName = True
    else:
        if not comment:
            comment = commentFromFile(submission)
        incorrectAssignmentName = False
    response = ""
    attachment = ""
    if comment!="cancelComment":
       if not incorrectAssignmentName:
           if attach and not comment.endswith("cancelAttachment"):
               response = input("  attach image from clipboard (y " + bcolors.BLUE + '<ENTER>=n' + bcolors.ENDC + ")? ")
               if response == "y":
                   while True:
                      image = ImageGrab.grabclipboard()
                      haveImage = True
                      if image == None:
                        haveImage = False
                        print("  No image found on top of clipboard.")
                        response = input("  (q)uit trying (" + bcolors.BLUE + '<ENTER>=try again' + bcolors.ENDC + ")? ")
                        if response == 'q':
                           break
                      else:
                         break
                   if haveImage:
                      imageJpg = image.convert('RGB')
                      imageJpg.save(os.path.join(emailAttachmentDir,'CSassignmentChecker.jpg'),'JPEG')
                      attachment = emailAttachmentDir + r'\CSassignmentChecker.jpg'
                      # print(f'{attachment = }')
                      comment = comment + "\nBe sure to look at the e-mail attachment.\n"
           else:
               comment = comment.rstrip("cancelAttachment")
       updateLogFile(submission, "  email msg -> " + comment)
       emailHeader = f'The {submission["Assignment"]} was submitted on {submission["submissionDateTime"]}.'
       dueDateMsg = getDueDateInfo(submission,submission["Assignment"],submission["submissionDateTimeObj"])[1]
       message = comment + '\n' + dueDateMsg + '\n'  + emailSignature
       for emailCode in emailCodes:
           emailSent = False
           if emailCode in submission["classRegistration"]:
             receiverEmailAddress = receiverEmailAddress + submission["classRegistration"][emailCode][2] + ";"
             emailSent = emailWithOutlook(receiverEmailAddress,subject,message,attachment)
           else: 
             print(f'  Do not have an email address to send to.')
             input(f'  <Enter> to continue and remove file {submission["FileName"]} from {submission["classPeriodDir"]}.')
       if emailSent:
         print(f'  {bcolors.BOLD}email sent{bcolors.ENDC} to {receiverEmailAddress}')
       return incorrectAssignmentName 

# https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development
# NOTE: DOES NOT CURRENTLY HANDLE ATTACHMENTS
def emailWithGmail(senderEmailAddress, senderPassword, receiverEmailAddress, subject, message):
    port = 465  # For SSL
    subjectStr = "Subject: " + subject + "\n\n"
    msgToSend = subjectStr + message
    context = ssl.create_default_context()  # Create a secure SSL context
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(senderEmailAddress, senderPassword)
        server.sendmail(senderEmailAddress, receiverEmailAddress, msgToSend)

# This function makes sure we wait until the sent email is in 'Sent Items' folder before moving it to 'Sent Items/CSAC'
def wait_for_email_in_sent_items(outlook, sent_email_subject, timeout_seconds=10, poll_interval=0.3):
    start_time = time.time()
    while time.time() - start_time < timeout_seconds:
        # Get the sent items folder
        sent_items_folder = outlook.GetNamespace("MAPI").GetDefaultFolder(5)  # 5 represents olFolderSentMail
        sent_items_folder.Items.Sort("[ReceivedTime]", True)
        # Check if the email with the specified subject is in the 'Sent Items' folder
        filter_str = f"[Subject]='{sent_email_subject}'"
        sent_email = sent_items_folder.Items.Restrict(filter_str).GetLast()
        if sent_email is not None:
            return True  # Email found in 'Sent Items'
        time.sleep(poll_interval)
    return False  # Timeout reached, email not found in 'Sent Items'

# send email using the Windows 10 Outlook App
def emailWithOutlook(email_recipient,email_subject,email_message,attachment_location=""):
    outlook=win32com.client.Dispatch("Outlook.Application")
    email=outlook.CreateItem(0)
    email.To = email_recipient
    email.Subject = email_subject
    email.Body = email_message
       
    if attachment_location != "":
        email.Attachments.Add(attachment_location)
    email.send      # SEND THE EMAIL
       
    if emailUseClassPeriodSentFolders:
        if wait_for_email_in_sent_items(outlook, email_subject):
            # MOVE THE SENT EMAIL FROM THE GENERAL 'Sent Items' Folder to the 'CSAC' folder within 'Sent Items'
            # Get the sent items folder
            sent_items_folder = outlook.GetNamespace("MAPI").GetDefaultFolder(5)  # 5 represents olFolderSentMail
            sent_items_folder.Items.Sort("[ReceivedTime]", True)

            # Retrieve the new email from the 'Sent Items' folder based on subject
            filter_str = f"[Subject]='{email_subject}'"
            new_email = sent_items_folder.Items.Restrict(filter_str).GetLast()

            # Move the new email to the desired folder
            target_folder = outlook.GetNamespace("MAPI").GetDefaultFolder(5).Folders['CSAC']
            new_email.Move(target_folder)

            return True
        else:
            print(f"   {bcolors.RED}Timeout reached. Email with subject '{email_subject}' not found in 'Sent Items'{bcolors.ENDC}.")
            return False                  
    return True

# send email via Outlook using SMTP (blocked by school district now)
# https://medium.com/@neonforge/how-to-send-emails-with-attachments-with-python-by-using-microsoft-outlook-or-office365-smtp-b20405c9e63a
def emailWithOutlookViaSMTP(email_sender,email_password,email_recipient,email_subject,email_message,attachment_location=""):
    success = True
    msg = MIMEMultipart()
    msg["From"] = email_sender
    msg["To"] = email_recipient
    msg["Subject"] = email_subject
    msg.attach(MIMEText(email_message, "plain"))
    if attachment_location != "":
        filename = os.path.basename(attachment_location)
        attachment = open(attachment_location, "rb")
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename= %s" % filename)
        msg.attach(part)
        attachment.close()
    try:
        TIMEOUT = 15   # 15 seconds
        server = smtplib.SMTP("smtp.office365.com", 587,None,TIMEOUT)  # for me times out at school (but does not timeout at home)
        response = server.ehlo()
        response = server.starttls()
        response = server.login(email_sender, email_password)
        text = msg.as_string()
        server.sendmail(email_sender, email_recipient, text)
        server.quit()
    except:
        print("  email SMPT server connection error (TIMEOUT=" + str(TIMEOUT) + ")")
        success = False
    return success

def sendTextMsg(msg,phoneNumber):
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
             body=msg,
             from_='+17572557696',
             to='+1'+ phoneNumber
         )
    print("Texted message to",phoneNumber)    

def commentFromFile(submission):
   askQuestion = True
   matchResponse = False
   commentsFile = ""
   while askQuestion:
      askQuestion = False
      while not matchResponse:
         response = input("  Comment (g[*], l[*], (o)ne-time comment, (n)o comment, (c)lipboard text (ca)lipboard&attachment e(x)it? ")
         if matchResponse := re.match(r'([gloncx])([.\w. \-]*)',response):
            commentTypeResponse = matchResponse.group(1)
            commentNameResponse  = matchResponse.group(2)
      if commentTypeResponse == 'g':
         commentsFile = os.path.join(rootDir,"ASSIGNMENT_GROUPS","comments"+submission["language"].upper()+".txt")
      elif commentTypeResponse == 'l':
         commentsFile = os.path.join(submission["goldenAssignmentDir"],"comments.txt")
      elif commentTypeResponse == 'o':
         commentsFileOneTime = os.path.join(rootDir,"ASSIGNMENT_GROUPS","comments_ONE_TIME.txt")
         with open(commentsFileOneTime, "w") as oneTimeFile:
            None
         #fh = open(commentsFileOneTime,"w")   # create the file
         #fh.close()
         textEditorCmd = textEditorCmdOpt1 + [commentsFileOneTime]
         process = subprocess.Popen(textEditorCmd, shell=True)
         submission["processes"].append(process)
         input("  ### press any key to continue once comments_ONE_TIME.txt has been saved.")
      comment = ''
      if commentTypeResponse == 'g' or commentTypeResponse == 'l':
         if not commentNameResponse:
            askQuestion = True
            matchResponse = False
            textEditorCmd = [textEditor,"-nosession",commentsFile]      
            process = subprocess.run(textEditorCmd, shell=True)
            submission["processes"].append(process)
         else:
            fname = commentsFile[commentsFile.find("ASSIGNMENT_GROUPS"):]
            print("    retrieving comment",commentNameResponse,"from",fname)
            commentsDict = {}
            firstComment = True
            commentName = ''
            commentCount = 1
            with open(commentsFile) as cFile:
               for line in cFile:
                  if matchResponse := re.match(r'comment ([.\w. \-]+)',line):
                     commentNamePrev = commentName
                     commentName = matchResponse.group(1)
                     if firstComment:
                        firstComment = False
                     else:
                        commentsDict[commentNamePrev] = comment
                        comment = ''
                        commentCount += 1
                  else:
                     if line[0:2] == "  ":   # remove first two spaces of the line (to account for idention in the comment file)
                        line = line[2:]
                     comment = comment + line      
               commentsDict[commentName] = comment  # put last comment from file into dictionary
            if commentNameResponse in commentsDict:
               comment = commentsDict[commentNameResponse]
            else:
               print('    comment' + bcolors.RED,commentNameResponse,bcolors.ENDC + "was not found.")
               askQuestion = True
               matchResponse = False               
      elif commentTypeResponse == 'o':
         with open(commentsFileOneTime) as cfile:
            for line in cfile:
               comment = comment + line
         os.remove(commentsFileOneTime)  # remove 
      elif commentTypeResponse == 'n':
         comment = ""
      elif commentTypeResponse == 'c':
         if not commentNameResponse == 'a':
             comment = pyperclip.paste() + '\n' + 'cancelAttachment'
      elif commentTypeResponse == 'x':
         comment = "cancelComment"
   print(f'  {bcolors.BOLD}  comment -> {bcolors.ENDC}{comment[:80].rstrip()} ...')
   return comment

def openErrorFile(submission,errorType):
   if errorType == "compile":
      errFile = submission["compileErrorFileName"] 
   else:
      errFile = submission["runTimeErrorFileName"]
   errorFileSize = Path(errFile).stat().st_size
   if errorFileSize != 0:  # had errors
     if not autoJudging:
         response = input("  " + errorType + f" {bcolors.RED}error!!!{bcolors.ENDC}  Open error file (y " + bcolors.BLUE + '<ENTER>=n' + bcolors.ENDC + ")? ")
         if response == "y":
            textEditorCmd = [textEditor,errFile]      
            process = subprocess.Popen(textEditorCmd, shell=True)
            submission["processes"].append(process)
     return True
   return False

def checkStudentRegistration(fname,nameLast,nameFirst,code,classRegistration):
   foundNameInRegistration = True
   name = nameLast + " " + nameFirst
   if name != "Test Test":
      if (code not in classRegistration):
         #print("  Code >" + code + "< is not registered " + "(" + fname +")")
         print('\n' + bcolors.RED + f'  Code >{code}< is not registered for {nameFirst} {nameLast}!!!' + bcolors.ENDC) 
         foundNameInRegistration = False
      elif classRegistration[code][0] != name:
         print('\n' + bcolors.RED + f'  Name mismatch!!! >{code}< code registered as {classRegistration[code][0]} and not {name}' + bcolors.ENDC)
         foundNameInRegistration = False
   return foundNameInRegistration

def processFileName(fname):
   nameLast = nameFirst = code = nameLastPartner = nameFirstPartner = codePartner = assignment = ""
   # File Submission:   LastName FirstName Code - assignmentName.ext
   # For group submissions LastName FirstNamae Code will contain a + sign between
   #   individual student's names/codes.
   validNameAndCode = re.search(r"^([-+\w]+) ([-+\w]+) ([+\d]+)",fname)
   if validNameAndCode:
      nameLast = validNameAndCode.group(1).strip()
      nameFirst = validNameAndCode.group(2).strip()
      code = validNameAndCode.group(3).strip()   
   validSubmittedFileName = re.search(r"^([-+\w]+) ([-+\w]+) ([+\d]+)(_)([-@.\w]+)( \(\d+\))?\.(\w+)$",fname) 
   concurrent = None
   if validSubmittedFileName:
      nameLast = validSubmittedFileName.group(1).strip()
      nameFirst = validSubmittedFileName.group(2).strip()
      code = validSubmittedFileName.group(3).strip()
      assignment = validSubmittedFileName.group(5).strip()
      # if a student submits an assignment a 2nd time before the 1st one has been processed
      # the filename will contain " (1)".
      concurrent = validSubmittedFileName.group(6)
      if concurrent:
          concurrent = concurrent.strip()   
      suffix = validSubmittedFileName.group(7).strip()
      ##print(f'DBG {getframeinfo(currentframe()).lineno}: {nameLast=} {nameFirst=} {code=} {assignment=} {suffix=} {concurrent=}')
   else:
      print('\n' + bcolors.RED + f'  Incorrect file name format >{fname}<' + bcolors.ENDC)
   return validNameAndCode,validSubmittedFileName,nameLast,nameFirst,code,assignment,concurrent
   
def getDueDateInfo(submission,assignment,submissionDateTimeObj):
   lateInfoStr = ''
   dueDateMsg = ''
   if assignment in assignmentDueDateGlobal:
       dueDateObj = datetime.strptime(assignmentDueDateGlobal[assignment],'%m/%d/%y').date()
       submittedDateObj = submissionDateTimeObj
       submittedDateString = submittedDateObj.strftime("%Y-%m-%d")
       submittedOnWeekendOrHoliday = (submittedDateObj.isoweekday() == 6) or (submittedDateObj.isoweekday() == 7) or (submittedDateString in schoolHolidays)
       lateMsg = 'this is the last day'
       if submittedOnWeekendOrHoliday:
           lateMsg = 'the next school day is the last day'
       calendarDaysLate = (submittedDateObj - dueDateObj).days
       schoolDaysLate = busday_count(dueDateObj,submittedDateObj,weekmask=[1,1,1,1,1,0,0],holidays=schoolHolidays)
       if schoolDaysLate > 0:
           if schoolDaysLate > 6:
               lateInfoStr = bcolors.BOLD + bcolors.RED + f'2late {schoolDaysLate-6} school day{"s"[:(schoolDaysLate-6)^1]} since last 70% day' + bcolors.ENDC + bcolors.RED + f' 0%' + bcolors.ENDC
           elif schoolDaysLate > 3:
               lateInfoStr = bcolors.BOLD + bcolors.RED + f'late {schoolDaysLate}' + bcolors.ENDC + f':{calendarDaysLate}' + bcolors.RED + f' 70%' + bcolors.ENDC
           elif schoolDaysLate > 0:
               lateInfoStr = bcolors.BLUE + f'{schoolDaysLate}' + bcolors.ENDC + f':{calendarDaysLate}' + bcolors.BLUE + f' grace day' + bcolors.ENDC
       else:
           lateInfoStr = bcolors.GREEN + f'{schoolDaysLate}' + bcolors.ENDC + f':{calendarDaysLate}'

       if schoolDaysLate < 0:
           dueDateMsg = f'The assignment is due on {assignmentDueDateGlobal[assignment]} which is in {-calendarDaysLate} calendar days ({-schoolDaysLate} school days). After that you still have 3 "grace" days to receive full credit.'
       elif schoolDaysLate == 0:
           dueDateMsg = f'You submitted on {submission["submissionDateTime"]} which is the assignments due date. You still have 3 "grace" school days to receive full credit.'
       elif schoolDaysLate <  3:
           dueDateMsg = f'The assignment was due on {assignmentDueDateGlobal[assignment]}. You submitted on {submission["submissionDateTime"]} (you still have {3-schoolDaysLate} school day{"s"[:(3-schoolDaysLate)^1]} left from this date to receive full credit).'
       elif schoolDaysLate == 3:
           dueDateMsg = f'The assignment was due on {assignmentDueDateGlobal[assignment]}. You submitted on {submission["submissionDateTime"]} ({lateMsg} to still receive full credit for the assignment).'
       elif schoolDaysLate < 6:
           dueDateMsg = f'The assignment was due on {assignmentDueDateGlobal[assignment]}. You submitted on {submission["submissionDateTime"]} (the assignment can still be submitted for partial credit for {6-schoolDaysLate} more school day{"s"[:(6-schoolDaysLate)^1]} from this date).'
       elif schoolDaysLate == 6:
           dueDateMsg = f'The assignment was due on {assignmentDueDateGlobal[assignment]}. You submitted on {submission["submissionDateTime"]} ({lateMsg} to still receive partial credit for the assignment).'
       elif schoolDaysLate > 6:
           dueDateMsg = f'You submitted on {submission["submissionDateTime"]}. It is now too late to submit this assignment for credit. The last partial credit day was {schoolDaysLate-6} school days ago. The assignment was due on {assignmentDueDateGlobal[assignment]} which was {schoolDaysLate} school days or {calendarDaysLate} calendar days ago.'
   else:
       lateInfoStr = "NoDueDate"
       
   return lateInfoStr,dueDateMsg
   
def processCurrentSubmission(currentSubmission, assignmentGroups, assignments,classRootDir):
   submission = {}
   submission["processes"] = []
   submission["valid"] = False
   submission["classPeriod"] = os.path.basename(os.getcwd())
   submission["classPeriodDir"] = Path(classRootDir)
   submission["FileName"] = currentSubmission
   submission["submissionDateTime"] = datetime.fromtimestamp(Path(submission["FileName"]).stat().st_mtime).strftime("%b_%d_%Hh%Mm%Ss")
   submission["submissionDateTimeObj"] = date.fromtimestamp(Path(submission["FileName"]).stat().st_mtime)
   submission["classDir"] = classRootDir;
   # check submission
   validNameAndCode,validSubmittedFileName, nameLast, nameFirst, code, assignment, concurrent = processFileName(submission["FileName"])                                                          # windows will name the file with a " (1)" in the filename      
   if concurrent:
       print("  Assignment was submitted while a previous submission was still waiting to be run")
   validFileSubmission = validNameAndCode and validSubmittedFileName
     
   submission["registration"] = '@' in assignment
   ##print(f'{validFileSubmission=} {nameLast=} {nameFirst=} {code=} {assignment=} {submission["registration"]=}')
   submission["groupSubmission"] = False
   if nameLast.find('+') != -1 or nameFirst.find('+') != -1 or code.find('+') != -1:
      submission["groupSubmission"] = True
      submission["groupLastNames"] = nameLast.split('+')
      submission["groupFirstNames"] = nameFirst.split('+')
      submission["groupCodes"] = code.split('+')
      if (len(submission["groupLastNames"])== len(submission["groupFirstNames"])) and (len(submission["groupLastNames"])== len(submission["groupCodes"])):
         submission["groupNumbersOK"] = True
      else:
         submission["groupNumbersOK"] = False
   submission["FileExtension"] = os.path.splitext(submission["FileName"])[1]
   if submission["FileExtension"] == ".py":
       submission["language"] = "python"
   else:
       submission["language"] = "java"
   submission["Assignment"]  = assignment
   if validSubmittedFileName:
       submission["lateInfo"] = getDueDateInfo(submission,assignment,submission["submissionDateTimeObj"])[0]
       if submission["FileExtension"] == ".zip":
         submission["assignmentFileName"] = submission["Assignment"] + ".java"
       else:
         submission["assignmentFileName"] = submission["Assignment"] + submission["FileExtension"]       
   if validNameAndCode: 
       if submission["groupSubmission"]:
          submission["studentName"] = submission["groupLastNames"][0] + " " + submission["groupFirstNames"][0]  # for a group submission the student run directory is in the 1st student of the groups student directory
          submission["studentCode"] = submission["groupCodes"][0]
       else:
          submission["studentName"] = nameLast + " " + nameFirst
          submission["studentCode"] = code
         
   submission["classRegistration"] = loadRegisteredStudents(submission["classPeriodDir"],assignmentGroups)

   if validFileSubmission:
       if submission["registration"]:
          registrationOK = True
       else:
          if submission["groupSubmission"]:
             registrationOK = True
             if (len(submission["groupLastNames"]) == len(submission["groupFirstNames"])) and (len(submission["groupLastNames"]) == len(submission["groupCodes"])):
                for i in range(len(submission["groupLastNames"])):
                    studentRegistered = checkStudentRegistration(submission["FileName"],submission["groupLastNames"][i],submission["groupFirstNames"][i],submission["groupCodes"][i],submission["classRegistration"])
                    registrationOK = registrationOK and studentRegistered
             else:
                registrationOK = False
                print('\n' + bcolors.RED + f'  Different number of last names, first names, and secret codes.' + bcolors.ENDC);
          else:
             registrationOK = checkStudentRegistration(submission["FileName"],nameLast,nameFirst,code,submission["classRegistration"])
   #print(f'DBG  {assignments=}')

   if (assignment in assignments):   
       submission["assignmentGroupId"] = assignments[assignment]  # assignment group assignment belongs to
       assignmentGroup = assignmentGroups[submission["assignmentGroupId"]]  # dictionary with info for this assignment group
       submission["assignmentGroup"] = assignmentGroup
       submission["listOfAssignments"] = assignmentGroup["listOfAssignments"]

       if validFileSubmission and not(assignment in submission["listOfAssignments"]):
          print("  Assignment >"+assignment+"< is not in group "+submission["listOfAssignments"])
   submission["invalidAssignment"] = validFileSubmission and not((assignment in assignments) or submission["registration"])
   if submission["invalidAssignment"]:
      print('\n' + bcolors.RED + f'  Invalid Assignment Name: >{assignment}< for submission: {submission["FileName"]}' + bcolors.ENDC)
      
   if validFileSubmission and ((assignment in assignments) or submission["registration"]) and registrationOK and (submission["registration"] or (assignment in submission["listOfAssignments"])):
      submission["nameForLatestDir"] = submission["studentName"]

      if submission["registration"]:   
         if submission["studentCode"] in submission["classRegistration"]:
             print("  Code >" + submission["studentCode"] + "< is already registered")
             print("    previous registration", submission["classRegistration"][submission["studentCode"]][0],submission["studentCode"],"("+submission["classRegistration"][submission["studentCode"]][2]+")")
             print("    current submission   ", submission["FileName"])
             input("  Incorrect registration. Press any key to delete current submission and continue ... ")
         else:
             foundName = False
             for k,v in submission["classRegistration"].items():                 
                 if v[0] == submission["studentName"]:
                    foundName = True
                    print("  Name >" + submission["studentName"] + "< is already registered")
                    print("    previous registration", v[0],k,v[2])
                    print("    current submission   ", submission["FileName"])
                    input("  Incorrect registration. Press any key to delete current submission and continue ... ")
                    break
             if not foundName:
                 with open("REGISTER.txt", "a") as freg:  # register the student in REGISTER.txt
                    freg.write(f'{submission["studentCode"]} {submission["studentName"]} {submission["classPeriod"]} {assignment}\n')
                    print('  ' + submission["studentName"] + ' was registered (' + submission["studentCode"] + ' ' + assignment + ')')
         print("  removing file -> ",submission["FileName"])
         os.remove(submission["FileName"])  # remove registration file (assignment name was register, file has served its purpose)
      else:   
         submission["valid"] = True
         submission["FileNameRoot"] = os.path.splitext(submission["FileName"])[0]
         submission["submittedFileNameWithDate"] = submission["FileNameRoot"] + "_" + submission["submissionDateTime"] + submission["FileExtension"]
         submission["outFileName"] = submission["Assignment"] + "_out.txt"
         submission["outCheckFileName"] = submission["Assignment"] + "_check.txt"
         submission["outFindFileName"] = submission["Assignment"] + "_find.txt"
         submission["outCorrectFileName"] = submission["Assignment"] + "_" + submission["submissionDateTime"] + "_out_CORRECT.txt"
         submission["outCorrectButLateFileName"] = submission["Assignment"] + "_" + submission["submissionDateTime"] + "_out_CORRECT_LATE.txt"
         submission["outCorrectBut2LateFileName"] = submission["Assignment"] + "_" + submission["submissionDateTime"] + "_out_CORRECT_2LATE.txt"
         submission["outGradeFileName"] = submission["Assignment"] + "_" + submission["submissionDateTime"] + "_out_GRADE_##.txt"
         submission["outLongFileName"] = submission["Assignment"] + "_" + submission["submissionDateTime"] + "_out.txt"
         submission["outFileNamePresentationErr"] = submission["Assignment"] + "_" + submission["submissionDateTime"] + "_presentationErr.txt"
         submission["outFileNameManualCheckAuto"] = submission["Assignment"] + "_" + submission["submissionDateTime"] + "_manualCheckAuto.txt"
         submission["compileErrFileName"] = submission["Assignment"] + "_" + submission["submissionDateTime"] + "_compileErr.txt"
         submission["runErrFileName"] = submission["Assignment"] + "_" + submission["submissionDateTime"] + "_runErr.txt"
         submission["runTimeErrorFileName"] = submission["Assignment"] + "_err.txt"
         submission["compileErrorFileName"] = "CompilerError.txt";
         # directories
         submission["assignmentGroupDir"] = assignmentGroup["assignmentGroupDir"]
         submission["goldenDir"] = assignmentGroup["goldenDir"]
         submission["goldenAssignmentDir"] = os.path.join(assignmentGroup["goldenDir"], submission["Assignment"])
         submission["goldFile"] = os.path.join(submission["goldenAssignmentDir"], "gold.txt")
         submission["findGoldFile"] = os.path.join(submission["goldenAssignmentDir"], "findGold.txt")
         submission["goldCheckFile"] = os.path.join(submission["goldenAssignmentDir"], "checker.txt")
         submission["stuffToFindFile"] = os.path.join(submission["goldenAssignmentDir"], "find.txt")
         submission["dataInputFileExists"] = os.path.exists(os.path.join(submission["goldenAssignmentDir"],submission["Assignment"]+".dat"))
         submission["dataInputFileName"] = os.path.join(submission["goldenAssignmentDir"],submission["Assignment"]+".dat")
         submission["timeoutFileName"] = os.path.join(submission["goldenAssignmentDir"],"timeout.txt")
         if os.path.exists(submission["timeoutFileName"]):
             with open(submission["timeoutFileName"]) as tfile:
                submission["timeout"] = float(tfile.readline().strip())
         else:
           submission["timeout"] = TIMEOUT_DEFAULT
         submission["plagiarismAssignmentDir"] = os.path.join(assignmentGroup["plagiarismDir"],submission["Assignment"])
         ##RPM FIX Creating a plagiarism directory for each assignment should be done when setting up the class
         if not os.path.isdir(submission["plagiarismAssignmentDir"]):
           os.mkdir(submission["plagiarismAssignmentDir"])
         # student directories
         submission["studentDir"] = os.path.join(submission["assignmentGroupDir"],submission["studentName"] + "_" + submission["studentCode"])
         if not os.path.isdir(submission["studentDir"]):
           os.mkdir(submission["studentDir"])
         submission["studentAssignmentDir"] = os.path.join(submission["studentDir"],submission["Assignment"])
         if not os.path.isdir(submission["studentAssignmentDir"]):
           os.mkdir(submission["studentAssignmentDir"])
         submission["studentPgmRunDir"] = os.path.join(submission["studentAssignmentDir"],submission["submissionDateTime"])
         if not os.path.isdir(submission["studentPgmRunDir"]):
              os.mkdir(submission["studentPgmRunDir"])
         submission["studentPgmRunSubmissionDir"] = os.path.join(submission["studentAssignmentDir"],submission["submissionDateTime"],"submission")     
         if not os.path.isdir(submission["studentPgmRunSubmissionDir"]):
              os.mkdir(submission["studentPgmRunSubmissionDir"])
         submission["outputFile"] = os.path.join(submission["studentPgmRunDir"],submission["outFileName"])
         if submission["groupSubmission"]:
           partnersDirs = []
           for i in range(len(submission["groupLastNames"])):
              partnerName = submission["groupLastNames"][i] + " " + submission["groupFirstNames"][i]
              partnerCode = submission["groupCodes"][i]
              #print(f'{getframeinfo(currentframe()).lineno}: {partnerName=} {partnerCode=}')
              partnerDir = os.path.join(submission["assignmentGroupDir"],partnerName + "_" + partnerCode)
              partnersDirs.append(partnerDir)
              if not os.path.isdir(partnerDir):
                 os.mkdir(partnerDir)                
           submission["partnersDirs"] = partnersDirs

   else:
      updateLogFile(submission, "  File submission error (" + submission["FileName"] + ")",True)
      pyperclip.copy(submission["FileName"])
      time.sleep(0.5)
      if not submission["invalidAssignment"]:    # if not invalid assignment
        response = input("  Print out class registration (y " + bcolors.BLUE + '<ENTER>=n' + bcolors.ENDC + ")? ")
        if response == 'y':
            classRegistrationList = list(submission["classRegistration"].items())
            cols = 4
            rows = ceil(len(classRegistrationList) / cols)     # divide into columns
            fullCols = len(classRegistrationList) % cols       # columns that are full (i.e. have data in every row)
            for r in range(rows):
                rowStr = ''
                for c in range(cols):
                    if (c*rows)+r < len(classRegistrationList):
                       key,value = classRegistrationList[(c*rows)+r]
                       rowStr += f'{value[0][:15]:16} {key:6}    '
                print('    ' + rowStr)                   
      incorrectAssignmentName = False
      while True:
         if incorrectAssignmentName:
             response = 'r'
         else:
             response = input("  New name (clipboard), (r)emove submission, (m)ove to manual check (e)mail? ")
         if response == 'r':
            if os.path.exists(submission["FileName"]):
                os.remove(submission["FileName"])
                updateLogFile(submission, "  removed "  + os.path.abspath(os.path.join(classRootDir,submission["FileName"])),True)
            break
         elif response == 'm':
            os.rename(os.path.join(classRootDir,submission["FileName"]),os.path.join(submission["classDir"],"00ManualCheck",submission["FileName"]))  #move to 00ManualCheck
            updateLogFile(submission, "  copied to " + os.path.abspath(os.path.join(submission["classDir"],"00ManualCheck",submission["FileName"])),True)
            break
         elif response == 'e':
            incorrectAssignmentName = emailStudent(submission)
         elif response != '':
            yesNo = input(f'  Rename {submission["FileName"]} to {response} ({bcolors.BLUE}<ENTER>=yes{bcolors.ENDC})? ')
            if yesNo == '':
                if not response in os.listdir():   # make sure file (with case sensitive name) is not already in directory used to use not os.path.exists(response) but it is case insensitive
                    os.rename(submission["FileName"], response)  # rename to new name
                else:
                    print("    File " + response + " already exists!")
                    print("    Looks like student already resubmitted with the correct name and you can remove this file.")
                break
   return submission

def moveFilesFromDirToDir(dirFrom,DirTo,extension):               
    if dirFrom:
        files = glob.iglob(os.path.join(dirFrom, "*"+extension))
        movedFiles = False
        for file in files:
            if os.path.isfile(file):
                move(file, DirTo)   
                movedFiles = True
    return movedFiles

def copyFilesToProgramRunDirectory(submission, classRootDir):
    goldenAssignmentDir = submission["goldenAssignmentDir"]
    copyfile(os.path.join(classRootDir,submission["FileName"]),os.path.join(submission["studentPgmRunSubmissionDir"],submission["FileName"]))  # copy originally submitted file
    if submission["FileExtension"] == ".java":
        copyfile(os.path.join(classRootDir,submission["FileName"]),os.path.join(submission["studentPgmRunDir"],submission["assignmentFileName"]))  # copy so filename matches assignment name for java
    else:  # .zip files or Python .py files
        copyfile(os.path.join(classRootDir,submission["FileName"]),os.path.join(submission["studentPgmRunDir"],submission["FileName"]))
    os.chdir(submission["studentPgmRunDir"])
    if submission["FileExtension"] == ".zip":
        
        
       with zipfile.ZipFile(submission["FileName"]) as zFile:
           fileList = []
           for filename in zFile.namelist():
               if not filename.startswith("__MACOSX"):    # zip files on MACOS have files in a __MACOSX folder that we do not want to unzip                   
                   fileList.append(filename)
           for file in fileList:
               if file != 'Archive/':             # zip files on MACOS have everything in an Archive folder, ignore the folder, but not the files in it
                   zFile.extract(file,'.')
                   if not os.path.exists('./'+os.path.basename(file)):
                      os.rename(file,'./'+os.path.basename(file))
       files = [p for p in Path('.').iterdir() if p.is_file()]
       javaFilesFound = False
       for file in files:
           if (file.suffix == ".java"):
               javaFilesFound = True
           if not(file.suffix == ".java" or file.suffix == ".zip" or file.suffix == ".txt"):
              print("  Warning!!! Student zip file contains something other than a .java, .zip, or .txt file (" + file.name + ")")
       if not javaFilesFound:
           print(f"{bcolors.RED}  Error!!!{bcolors.ENDC} The zip file did not contain any java files.")
    goldenDirFiles = os.listdir(goldenAssignmentDir)
    for goldenDirFile in goldenDirFiles:
        if goldenDirFile != "gold.txt" or goldenDirFile != "checker.txt":
            fullGoldenDirFile = os.path.join(goldenAssignmentDir, goldenDirFile)
            if os.path.isfile(fullGoldenDirFile):
                copy(fullGoldenDirFile, submission["studentPgmRunDir"])
    os.chdir(classRootDir)
    
# returns True if output file matches golden file EXACTLY (except for line ending spaces or extra spaces/newlines at beginning or end of file)
def filesMatch(outputFile,goldenFile):
    with open(outputFile) as ofile:
        output = ofile.read().strip().split("\n")
    if not os.path.exists(goldenFile):
        return False
    with open(goldenFile) as gfile:
        golden = gfile.read().strip().split("\n")
    match = True
    if len(output) != len(golden):
        match = False
    else:
        for i in range(len(golden)):
            if golden[i].rstrip() != output[i].rstrip():
                match = False
                break
    return match

def runChecker(submission, classRootDir):
    checkGood = True
    os.chdir(submission["studentPgmRunDir"])
    if os.path.exists(os.path.join(submission["Assignment"] + "Checker.java")):
       compileCmd = ["javac", "-parameters", submission["Assignment"] + "Checker.java"]
       with open("CompilerOutput.txt", "w") as fout:
           with open(submission["compileErrorFileName"], "w") as ferr:
               result = subprocess.run(compileCmd, stdout=fout, stderr=ferr)  #COMPILE CHECKER
       errorCompile = openErrorFile(submission,"compile")

       if errorCompile:
           checkGood = False
       else:
           runCmd = ["java", submission["Assignment"] + "Checker"]
           with open(submission["outCheckFileName"], 'w') as fout:
              result = subprocess.run(runCmd, stdin=None, stdout=fout, stderr=None)   # run Checker
           checkFilesMatches = filesMatch(submission["outCheckFileName"],submission["goldCheckFile"])
           if checkFilesMatches:
               print('  ' + bcolors.BOLD + bcolors.BGGREEN + f'>>> CHECK CORRECT <<<' + bcolors.ENDC)
           else:
               if Path(submission["goldCheckFile"]).is_file():   #rpmnew
                   print('  ' + bcolors.BOLD + bcolors.BGRED+ "### miscompare checker (opening diff) ###" + bcolors.ENDC,end=" ")
                   diffCmd = [diffPgm,submission["outCheckFileName"],submission["goldCheckFile"]]
                   process = subprocess.Popen(diffCmd, shell=True)     # run diff program
                   submission["processes"].append(process)
                   checkGood = False
    os.chdir(classRootDir)
    return checkGood

def getJavaCodeToSearch(javaFile, toSearch):   # used by findInProgram()
    """
    Extracts the code of a specified method from a Java file.
    - javaFile    The path to the Java file.
    - toSearch
      * the name of the method to extract
      * "canBeAnywhere" returns the whole java file
    """
    
    # Regular expression pattern to match the method definition and body    
    method_pattern = re.compile(r'\s*(public|private|protected|\s)*\s*\w+\s+' + re.escape(toSearch) + r'\s*\(.*\)\s*' + r'(\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\})', re.MULTILINE)  # Match method body with nested braces

    with open(javaFile, 'r') as java_file:
        java_code = java_file.read()
        
    if toSearch == "canBeAnywhere":
        return java_code
    else:
        method_match = method_pattern.search(java_code)
        if method_match:
            return method_match.group(0)  # Return the entire method definition and body
    #otherwise returns None by default
    
def getPythonCodeToSearch(pythonFile, toSearch): # used by findInProgram()
    """
    Extracts the specified code , all the code outside any functions, or all the code in the file
    toSearch can be
      * function/method name  if code for the specific function is to be extracted
      * "outsideAFunction"    if all the code outside any function is be extracted 
      * "canBeAnywhere"       if all the code in the file is to be extracted
    """
    inTheFunction = False
    outsideAFunction = False
    lineNum = 0
    with open(pythonFile, 'r') as file:
        lineNum += 1
        code = None
        for line in file:
            line = re.sub(r'\s*#.*', '', line)   # remove comments
            if toSearch != 'canBeAnywhere':
                functionStart = re.search(r'^def\s+(\w+)\s*\((.*?)\)\s*:', line)
                if functionStart:
                    outsideAFunction = False
                outSideAFunctionStart = re.search(r'^(?!def\b)[a-zA-Z]+.*$', line)   # line on the left margin, starts with any alphabetic string except def
                if toSearch != "outsideAFunction":
                    if functionStart:
                        outsideAFunction = False
                        if inTheFunction:   # already processed the function and now found the start of another function or the code outside any functions
                            break
                        functionName = functionStart.group(1)
                        if functionName == toSearch:   # found the specified function
                            inTheFunction = True
                else:
                    if outSideAFunctionStart:
                        outsideAFunction = True
            #print(inTheFunction,outsideAFunction)
            if inTheFunction or outsideAFunction or toSearch == 'canBeAnywhere':
                if code is None:
                    code = line
                else:
                    code += line
    return code

def findInProgram(submission, classRootDir):
    os.chdir(submission["studentPgmRunDir"])
    miscompare = False
    stuffToFindFile = submission["stuffToFindFile"]
    outFindFile = submission["outFindFileName"]
    findGoldFile = submission["findGoldFile"]
    if submission["language"] == "python":
        codeFile = submission["FileName"]
    elif submission["language"] == "java":
        codeFile = submission["assignmentFileName"]
    if os.path.exists(stuffToFindFile):
        ffind  = open(outFindFile,'w')

        with open(stuffToFindFile, 'r') as file:
            lines = file.readlines()
        
        for line in lines:   # go through all the lines of the find.txt file
            # Split the line into toSearch and pattern
            parts = line.strip().split(maxsplit=1)
            if len(parts) != 2:
                ffind.write(f"Skipping invalid line: {line.strip()}\n")
                continue
            toSearch, regex = parts
            pattern = re.compile(regex.replace('\\\\', '\\'),re.M)
            
            # Check the pattern in the program file
            if os.path.exists(codeFile):
                if codeFile.endswith(".py"):
                    code = getPythonCodeToSearch(codeFile, toSearch)
                elif codeFile.endswith(".java"):
                    code = getJavaCodeToSearch(codeFile, toSearch)
                else:
                    ffind.write("ERROR!!! Only .py and .java files are supported\n")
                if code is None:
                    ffind.write(f"'{toSearch}' NOT FOUND\n")
                else:
                    found = len(re.findall(pattern, code))                
                    if found:
                        ffind.write(f"{toSearch}: FOUND {found} times '{regex}'\n")
                    else:
                        ffind.write(f"{toSearch}: DID NOT FIND  '{regex}'\n")
            else:
                ffind.write(f"File '{codeFile}' does not exist.\n")
        ffind.close()

        # compare submission find output to gold find file
        checkFilesMatches = filesMatch(outFindFile,findGoldFile)
        if checkFilesMatches:
           print('  ' + bcolors.BOLD + bcolors.BGGREEN + f'### FIND CORRECT ###' + bcolors.ENDC)
           miscompare = False
        else:
           print('  ' + bcolors.BOLD + bcolors.BGRED+ "### miscompare find (opening diff) ###" + bcolors.ENDC)
           diffCmd = [diffPgm,outFindFile,findGoldFile]
           process = subprocess.Popen(diffCmd, shell=True)     # run diff program
           submission["processes"].append(process)
           miscompare = True
               
    os.chdir(classRootDir)
    return miscompare


def runProgram(submission, classRootDir):
    autoJudgingCorrect = False
    error = False
    errorCompile = False
    os.chdir(submission["studentPgmRunDir"])
    if submission["language"] == "python":
        # Nov 2024  This caused a problem with some pair programming submissions, but not sure why it is necessary and what it even does (Python does not have a compile step????)
        # compileCmd = ["python","-m","py_compile",submission["FileName"]]
        compileCmd = []
        runCmds = [["python", submission["FileName"]]]
    elif submission["language"] == "java":
        compileCmd = ["javac", "-parameters", "-g", "-Xlint:unchecked", "*.java"]
        runCmds = []
        tester = False
        runner = False
        if os.path.exists(os.path.join(submission["Assignment"] + "Tester.java")):
            runCmds.append(["java",submission["Assignment"] + "Tester"])
            tester = True
        if os.path.exists(os.path.join(submission["Assignment"] + "Runner.java")):
            runCmds.append(["java",submission["Assignment"] + "Runner"]);
            runner = True
        if not(tester or runner):
            #incorrect use of rstrip   runCmds.append(["java",submission["assignmentFileName"].rstrip(".java")]);
            runCmds.append(["java",submission["assignmentFileName"][:submission["assignmentFileName"].find(".java")]])
    else:
        print(f"{bcolors.RED}Error!!!{bcolors.ENDC} Unsupported language")
        sys.exit()
    # language independant code
    if compileCmd:
        with open("CompilerOutput.txt", "w") as fout:
            with open(submission["compileErrorFileName"], "w") as ferr:
                result = subprocess.run(compileCmd, stdout=fout, stderr=ferr)  #COMPILE PROGRAM
        errorCompile = openErrorFile(submission,"compile")
    ideCmds = generateIdeCommands(submission)
    bringUpIDEorDataFile = '\nset /P c=Bring up IDE [y]? \nif /I "%c%" EQU "Y" goto :ide\ngoto :next\n:ide\n'
    for ideCmd in ideCmds:
       bringUpIDEorDataFile = bringUpIDEorDataFile + '\nSTART /B "' + ideCmd[0] + '"' + ' ' + '"' + ideCmd[1] + '"'
    bringUpIDEorDataFile = bringUpIDEorDataFile + '\n:next'
    latestResultsDir = os.path.join(classRootDir,"00LatestResults")
    if submission["dataInputFileExists"]:
        bringUpIDEorDataFile += '\nset /P c=Bring up input data file [y]? \nif /I "%c%" EQU "Y" goto :idf\ngoto :end\n:idf\n' + '"' + textEditor + '"' + " -multiInst -nosession " + '"' + submission["dataInputFileName"] + '"' + '\n:end'
    # compile error
    if errorCompile:
        copyfile(submission["compileErrorFileName"], os.path.join(latestResultsDir,submission["nameForLatestDir"] + "_compileError.txt"))  # copy compile error file to class directory
        copyfile(submission["compileErrorFileName"], os.path.join(submission["studentDir"],submission["compileErrFileName"]))  # copy output file to data directory
        if submission["groupSubmission"]:
           for partnerDir in submission["partnersDirs"]:
              copyfile(submission["compileErrorFileName"],os.path.join(partnerDir,submission["compileErrFileName"]))  # copy output file to all partners data directories        
        updateLogFile(submission, f"{bcolors.RED}Error!!!{bcolors.ENDC} " + submission["FileName"] + " had a compile time error.",False)
    # no compile error
    else:   
        if os.path.exists(os.path.join(latestResultsDir,submission["nameForLatestDir"] + "_compileError.txt")):
            os.remove(os.path.join(latestResultsDir,submission["nameForLatestDir"] + "_compileError.txt"))
        writeOrAppend = "w"
        timedOut = False
        for runCmd in runCmds:
            runStdin = None
            if not runCmd[1].endswith("Tester"):
               if runCmd[1].endswith("Runner"):
                  inputFileList = glob.glob(r"runnerUserInput*.txt")
               else:
                  inputFileList = glob.glob(r"pgmUserInput*.txt")
               if len(inputFileList) > 0:
                  for inputFile in inputFileList:
                     with open(inputFile) as runStdin:
                        #runStdin = open(inputFile)
                        with open(submission["outFileName"], writeOrAppend) as fout:
                            with open(submission["runTimeErrorFileName"], writeOrAppend) as ferr:
                               #fout.write("\n" + runCmd[1] + " stdin=" + inputFile +"\n")
                               fout.write("\nstdin=" + inputFile +"\n")
                               fout.flush()
                               if not timedOut:
                                  try:
                                     result = subprocess.run(runCmd, stdin=runStdin, stdout=fout, stderr=ferr, timeout=submission["timeout"])   # run submitted RUNNER or student program with a user input file (i.e. program reads from stdin)
                                  except:
                                     print('  ' + bcolors.BOLD + bcolors.BGRED +  "Timed Out (>" + str(submission["timeout"]) + "sec)!!! " + str(runCmd)  + bcolors.ENDC)
                                     sys.stdin = sys.__stdin__  # restoring the terminal settings by resetting stdin back to sys.stdin in case the subprocess affected it
                                     timedOut = True
                               writeOrAppend = "a"
                     #runStdin.close()
               else:
                  with open(submission["outFileName"], writeOrAppend) as fout:
                      with open(submission["runTimeErrorFileName"], writeOrAppend) as ferr:
                            if not timedOut:
                               try:
                                  result = subprocess.run(runCmd, stdin=runStdin, stdout=fout, stderr=ferr, timeout=submission["timeout"])   # run submitted RUNNER or student program with a user input file (i.e. program reads from stdin)
                               except:
                                  print('  ' + bcolors.BOLD + bcolors.BGRED +  "Timed Out (>" + str(submission["timeout"]) + "sec)!!! " + str(runCmd)  + bcolors.ENDC)                                 
                                  sys.stdin = sys.__stdin__  # restoring the terminal settings by resetting stdin back to sys.stdin in case the subprocess affected it
                                  timedOut = True
                            writeOrAppend = "a"
            else:
               with open(submission["outFileName"], writeOrAppend) as fout:
                   with open(submission["runTimeErrorFileName"], writeOrAppend) as ferr:
                      if not timedOut:
                          try:
                             result = subprocess.run(runCmd, stdin=runStdin, stdout=fout, stderr=ferr, timeout=submission["timeout"])   # run Tester    
                          except:                         
                             print('  ' + bcolors.BOLD + bcolors.BGRED +  "Timed Out (>" + str(submission["timeout"]) + "sec)!!! " + str(runCmd)  + bcolors.ENDC)
                             sys.stdin = sys.__stdin__  # restoring the terminal settings by resetting stdin back to sys.stdin in case the subprocess affected it
                             timedOut = True                          
                      writeOrAppend = "a"
        errorRun = openErrorFile(submission,"runtime")
        if errorRun:
            if os.path.exists(submission["outFileName"]):
                try: 
                   os.remove(submission["outFileName"])
                except:
                   print(f'ERROR! Can not remove file {submission["outFileName"]} right now.')
            if os.path.exists(os.path.join(latestResultsDir,submission["nameForLatestDir"] + ".bat")):
                os.remove(os.path.join(latestResultsDir,submission["nameForLatestDir"] + ".bat"))
            with open(os.path.join(latestResultsDir,submission["nameForLatestDir"] + ".bat"), "w") as fbatch:
                fbatch.write('"' + textEditor + '"' + " -multiInst -nosession " + '"' + os.path.join(submission["studentDir"],submission["runErrFileName"]) + '"')
                fbatch.write(bringUpIDEorDataFile)
            copyfile(submission["runTimeErrorFileName"], os.path.join(latestResultsDir,submission["nameForLatestDir"] + "_runTimeError.txt"))  # copy compile error file to class directory
            copyfile(submission["runTimeErrorFileName"], os.path.join(submission["studentDir"],submission["runErrFileName"]))  # copy output file to data directory
            if submission["groupSubmission"]:
               for partnerDir in submission["partnersDirs"]:
                  copyfile(submission["runTimeErrorFileName"],os.path.join(partnerDir,submission["runErrFileName"]))  # copy output file to all partners data directories
            updateLogFile(submission, f"{bcolors.RED}Error!!!{bcolors.ENDC} " + submission["FileName"] + " had a run time error.",False)
        else:
            if os.path.exists(os.path.join(latestResultsDir,submission["nameForLatestDir"] + "_runTimeError.txt")):
                os.remove(os.path.join(latestResultsDir,submission["nameForLatestDir"] + "_runTimeError.txt"))
    error = errorCompile or errorRun
    if not error:
        goldFileMatches = filesMatch(submission["outputFile"],submission["goldFile"])
        if goldFileMatches:
            print('  ' + bcolors.BOLD + bcolors.BGGREEN + f'*** RUN CORRECT ***' + bcolors.ENDC)
            autoJudgingCorrect = True    
        else:
            if autoJudging:
                print("  INCORRECT (autojudged)")
            else:
                if Path(submission["goldFile"]).is_file():
                    print('  ' + bcolors.BOLD + bcolors.BGRED+ "### miscompare gold file (opening diff) ###" + bcolors.ENDC)
                    diffCmd = [diffPgm,submission["outputFile"],submission["goldFile"]]
                    process = subprocess.Popen(diffCmd, shell=True)     # run diff program
                    submission["processes"].append(process)
                else:
                    print("  ### no golden file, skipping diff")
            with open(os.path.join(submission["studentPgmRunDir"], "diff.bat"), "w") as fdiff:
                fdiff.write('"' + diffPgm + '"' + " " + submission["outFileName"] + ' "' + os.path.join(submission["goldenAssignmentDir"], 'gold.txt"'))
            # also write diff batch file to class directory (for quick access to each student's last run results)
            if os.path.exists(os.path.join(latestResultsDir,submission["nameForLatestDir"] + ".bat")):
                os.remove(os.path.join(latestResultsDir,submission["nameForLatestDir"] + ".bat"))
            with open(os.path.join(latestResultsDir,submission["nameForLatestDir"] + ".bat"), "w") as fbatch:
                fbatch.write('"' + diffPgm + '"' + ' "' + os.path.join(submission["studentPgmRunDir"],submission["outFileName"]) + '" "' + os.path.join(submission["goldenAssignmentDir"], "gold.txt") + '"')
                fbatch.write(bringUpIDEorDataFile)
    os.chdir(classRootDir)
    return autoJudgingCorrect

def getSubmissions(extensions):
    listOfSubmissions = []
    for extension in extensions:
        listOfSubmissions = listOfSubmissions + glob.glob(r"*" + extension)  
    allFiles = [f for f in glob.glob("*") if os.path.isfile(f)]
    notValidFiles = list(set(allFiles).difference(listOfSubmissions))
    if notValidFiles:
        print('Found invalid file(s)',notValidFiles)
    #if "REGISTER.txt" in listOfSubmissions:
    #  listOfSubmissions.remove("REGISTER.txt")
    listOfSubmissions.remove('REGISTER.txt')
    return listOfSubmissions

def updateLogFile(submission, logMessage, alsoPrint = False, indent=True):
    if not minimizeFilesCreated:
        if alsoPrint:
            print(logMessage)
        indentSpaces = ""
        if indent:
           indentSpaces = '  '
        # global log file in rootDir
        with open(os.path.join(rootDir,"logGlobal.txt"), "a") as fglog:
            fglog.write(indentSpaces + logMessage + "\n")
        # assignment log file in classRootDir
        if "assignmentGroupDir" in submission:
            with open(os.path.join(submission["assignmentGroupDir"],"logAssignment.txt"), "a") as falog:
                falog.write(indentSpaces+ logMessage + "\n")
        # student log file in student directory
        if "studentDir" in submission:  # "studentDir" will not be in dictionary for an invalid/unknown assignment name
            with open(os.path.join(submission["studentDir"],"log.txt"), "a") as fslog:
                fslog.write(indentSpaces + logMessage + "\n")

def gradeSubmission(submission):
    summary = "\n*** " + submission["Assignment"] + " (" + submission["result"] + ") " + submission["submissionDateTime"]
    gradesFileName = os.path.join(submission["studentAssignmentDir"],"grades.txt")
    with open(gradesFileName, "a") as gFile:
        gFile.write(summary + "\n  ")
    textEditorCmd = [textEditor,"-n1000000","-nosession",gradesFileName]      
    process = subprocess.Popen(textEditorCmd, shell=True)
    submission["processes"].append(process)

def submissionCorrect(submission,reason=""):
    # update CORRECT.txt file
    with open(os.path.join(rootDir,"CORRECT.txt"), "a") as fcorr:
       assignmentGroup = os.path.basename(os.path.normpath(submission["assignmentGroup"]["assignmentGroupDir"]))
       assignmentGroup = assignmentGroup[:27]+">" if len(assignmentGroup) > 27 else assignmentGroup
       assignment = submission["Assignment"]
       assignment = assignment[:11]+">" if len(assignment) > 11 else assignment
       fcorr.write(f'{submission["classPeriod"]} {reason} {assignmentGroup:<28} {submission["result"]} {assignment:<12} {submission["FileName"]} * {submission["submissionDateTime"]}\n')        
        #fcorr.write("(P" + submission["classPeriod"] + " " + os.path.basename(os.path.normpath(submission["assignmentGroup"]["assignmentGroupDir"])) +") " + submission["Assignment"] + " " + submission["FileName"] + " * " + submission["submissionDateTime"] + " *\n") 
    # move pgm to PLAGIARISM directory
    if not os.path.exists(os.path.join(submission["plagiarismAssignmentDir"],submission["submittedFileNameWithDate"])):
       os.rename(submission["FileName"], os.path.join(submission["plagiarismAssignmentDir"],submission["submittedFileNameWithDate"]))  
       #if submission["FileExtension"] == ".zip":
       #   combineFilesInZipFile(submission["plagiarismAssignmentDir"],submission["submittedFileNameWithDate"])
    else:
        os.remove(submission["FileName"])       # remove submission file (this only happens if the same file with the same time stamp is copied into class directory)
    correctFileName = submission["outCorrectFileName"]    # default correct case
    if Path(submission["studentPgmRunDir"],submission["outFileName"]).is_file():
       if reason == 'late':
           correctFileName = submission["outCorrectButLateFileName"]
       elif reason == '2late':    # submission is too late for any grade
           correctFileName = submission["outCorrectBut2LateFileName"]
       elif reason.startswith('grade'):
           actualGrade = reason[5:]
           correctFileName = submission["outGradeFileName"].replace('##',actualGrade)
       copyfile(os.path.join(submission["studentPgmRunDir"],submission["outFileName"]), os.path.join(submission["studentDir"],correctFileName))  # copy output file to data directory
       if submission["groupSubmission"]:
          for partnerDir in submission["partnersDirs"]:
             copyfile(os.path.join(submission["studentPgmRunDir"],submission["outFileName"]), os.path.join(partnerDir,correctFileName))  # copy output file to partner's data directory
    else:     # (outFileName file may not exist - maybe program was manually deemed to be correct)
       if reason == 'late':
           correctFileName = submission["outCorrectButLateFileName"]
       elif reason == '2late':    # submission is too late for any grade
           correctFileName = submission["outCorrectBut2LateFileName"]
       elif reason.startswith('grade'):
           actualGrade = reason[5:]
           correctFileName = submission["outGradeFileName"].replace('##',actualGrade)
       copyfile(os.path.join(submission["goldFile"]), os.path.join(submission["studentDir"],correctFileName))  # copy output file to data directory
       if submission["groupSubmission"]:
          for partnerDir in submission["partnersDirs"]:
             copyfile(os.path.join(submission["goldFile"]), os.path.join(partnerDir,correctFileName))  # copy output file to all partners data directories
    CSACscoreboard.updateScoreboard(scoreboardDir,submission["assignmentGroupDir"],submission["assignmentGroupId"],submission["classPeriod"],submission["listOfAssignments"])
    updateLogFile(submission, bcolors.BOLD + bcolors.GREEN + f'  *** CORRECT *** ' + bcolors.ENDC)

def submissionIncorrect(submission,reason=""):
    global autoJudging, moveTo00ManualCheck, classRootDir

    if autoJudging and moveTo00ManualCheck:
      copyfile(submission["FileName"], os.path.join(submission["classDir"],"00ManualCheck",submission["FileName"])) # move pgm to 00AutoManualCheck directory
      updateLogFile(submission, "  Copied to 00ManualCheck directory ", True)
    if reason == "presentationError":
       outFileName = submission["outFileNamePresentationErr"]
    elif reason == "manualCheck":
       outFileName = submission["outFileNameManualCheckAuto"]          
    else:
       outFileName = submission["outLongFileName"]
    if True or submission["valid"]:
        if os.path.exists(os.path.join(submission["studentPgmRunDir"],submission["outFileName"])):
            copyfile(os.path.join(submission["studentPgmRunDir"],submission["outFileName"]),os.path.join(submission["studentDir"],outFileName))  # copy output file to data directory
            if submission["groupSubmission"]:
              for partnerDir in submission["partnersDirs"]:
                 copyfile(os.path.join(submission["studentPgmRunDir"],submission["outFileName"]),os.path.join(partnerDir,outFileName))  # copy output file to all partners data directories
        CSACscoreboard.updateScoreboard(scoreboardDir,submission["assignmentGroupDir"],submission["assignmentGroupId"],submission["classPeriod"],submission["listOfAssignments"])
        updateLogFile(submission, "  >>> INCORRECT <<< ")
    else:
        updateLogFile(submission, "  >>> INVALID SUBMISSION <<< ")
    os.remove(submission["FileName"])

def generateIdeCommands(submission):
    global pythonIde,javaIde
    ideCmds = []
    ideCmd = ['none','none']
    if submission["language"] == "python":
       ideCmd = [pythonIde,os.path.join(submission["studentPgmRunDir"],submission["FileName"])]
       ideCmds.append(ideCmd)
    elif submission["language"] == "java":
        ideCmd = [javaIde,os.path.join(submission["studentPgmRunDir"],submission["Assignment"] + ".java")]
        ideCmds.append(ideCmd)
        if os.path.exists(os.path.join(submission["studentPgmRunDir"],submission["Assignment"] + "Tester.java")):
            ideCmd = [javaIde,os.path.join(submission["studentPgmRunDir"],submission["Assignment"] + "Tester.java")]
            ideCmds.append(ideCmd)

    return ideCmds

def setFileTimestampToNow(file):
    now = datetime.now()
    accessed_time = now
    modified_time = now
    accessed_time = int(time.mktime(accessed_time.timetuple()))
    modified_time = int(time.mktime(modified_time.timetuple()))
    os.utime(file, (accessed_time, modified_time))

def killProcesses(submission):
    for process in submission["processes"]:
        try:
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(process.pid)],stdout=devnull, stderr=devnull)
        except:
            pass
    submission["processes"] = []

### MAIN PROGRAM ###
def main():
    global interrupted, autoJudging, autoJudgingPeriods, autoJudgingSleepTime, moveTo00ManualCheck

    allAssignmentGroups, allAssignments = setup()
    autoJudging = False
    autoJudgingFirstTime = True
    autoJudgingSleepTime = 60  # in seconds
    while True:
        os.chdir(rootDir)
        inputContinue = False
        lCount = 0
        while not(inputContinue or not autoJudgingFirstTime):
            check4Activity()
            classPeriodNamesString = ""
            for classPeriod in classPeriodNamesForMenu:
                classPeriodNamesString = classPeriodNamesString + classPeriod + " "
            classPeriodNamesString = classPeriodNamesString.rstrip()
            response = input("\n" + "("+ classPeriodNamesString + ")judge (a)utojudge score(b)oard (l)og (f)iles e(x)it (" + bcolors.BLUE + "<ENTER>=check for new submissions" + bcolors.ENDC + ")? ")
            if response in classPeriodNamesForMenu:
                response = classPeriodNames[classPeriodNamesForMenu.index(response)]
            inputContinue = (response == 'x') or (response in classPeriodNames)
            if response in classPeriodNames:
                classPeriod = response
                manualCheckFiles = os.listdir(Path(rootDir,classPeriod,"00ManualCheck"))
                if len(manualCheckFiles) > 0:
                   response = input("  move " + str(len(manualCheckFiles)) + " files from 00ManualCheck to class directory to be judged (y " + bcolors.BLUE + '<ENTER>=n' + bcolors.ENDC + ")? ")
                   if response == 'y':
                      for file in manualCheckFiles:
                         os.rename(Path(rootDir,classPeriod,"00ManualCheck",file),Path(rootDir,classPeriod,file))
            elif response == "a":
                response2 = input("(" + classPeriodNamesString + ")autojudge (m)ultiple (" + bcolors.BLUE + '<ENTER>=all periods' + bcolors.ENDC + ")? ")
                autoJudging = True
                autoJudgingFirstTime = False
                if response2 in classPeriodNames:
                    classPeriod = response2
                    autoJudgingPeriods = [classPeriod]
                    autoJudgingSleepTime = 30
                elif response2 == "m":
                    response3 = input("Enter comma separated list of class periods (e.g. 1,4,5)? ")
                    autoJudgingPeriods = response3.split(",")
                    autoJudgingSleepTime = 30
                else:
                    autoJudgingPeriods = classPeriodNames
                moveTo00ManualCheck = False
                response3 = input("incorrect to 00ManualCheck directory instead of judging incorrect (y " + bcolors.BLUE + '<ENTER>=n' + bcolors.ENDC + ")? ")
                if response3 == 'y':
                   moveTo00ManualCheck = True
            elif response == "l":   # log
                print("  opening logGlobal.txt file")
                textEditorCmd = textEditorCmdOpt1 + ["logGlobal.txt"]      
                result = subprocess.run(textEditorCmd, shell=True)
            elif response == "f":   # file explorer
                print("  opening file explorer")
                process = subprocess.Popen('explorer "' + os.path.normpath(rootDir) + '"',creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
            elif len(response) > 0 and response[0] == "b":
               process = subprocess.Popen('explorer "' + scoreboardDir + r'\withNames"',creationflags=subprocess.CREATE_NEW_PROCESS_GROUP) # bring up file explorer of scoreboard directory
            elif response == "x":
                sys.exit()

        if autoJudging:
            classPeriod = autoJudgingPeriods[0]
            print(classPeriod,end="")


        classRootDir = os.path.join(rootDir,classPeriod)  # CLASSROOTDIRassignment (directory for submissions)
        os.chdir(classRootDir)
        
        if classPeriod == str(classPeriodForCompetitions):
            movedFilesJava   = moveFilesFromDirToDir(customDirectoryForUILComp,classRootDir,".java")
            movedFilesPython = moveFilesFromDirToDir(customDirectoryForUILComp,classRootDir,".py")
            if movedFilesJava or movedFilesPython:
                print(f'moved files to Period {classPeriod} from {customDirectoryForUILComp}')           
        

        # initialize the dictionaries for the class
        if classPeriod in allAssignmentGroups:
           assignmentGroups = allAssignmentGroups[classPeriod]
        else:
           print("No assignment group found for class period",classPeriod)
           break
        if classPeriod in allAssignments:
           assignments = allAssignments[classPeriod]
        else:
           print("No assignment found for class period",classPeriod)
           break

        # update scoreboard for every assignment group in the class
        aKeys = list(assignmentGroups.keys())
        aKeys.sort()
        for aGroupId in aKeys:
            aDict = assignmentGroups[aGroupId]
            aGroupDir = aDict["assignmentGroupDir"]
            listOfAssignments = aDict["listOfAssignments"]
            CSACscoreboard.updateScoreboard(scoreboardDir,aGroupDir,aGroupId,classPeriod,listOfAssignments)      
      
        doItAgain = False
        while True:  # loop over each program, run the oldest first
            interrupted = False
            correct = False          
            currentSubmissions = getSubmissions(validFileExtensions)
            if len(currentSubmissions) > 0:
                currentSubmission = min(currentSubmissions, key=os.path.getmtime)
                # when Dropbox first puts the file onto the PC it seperates file name components using space-space (ie. space dash space) but then quickly renames
                # the file using an _ (and no spaces) in the filename.  This program sometimes occasionally sees the space-space
                # name. The loop below wait until Dropbox has renamed the file in the folder.                
                while re.search(r"^([-+\w]+) ([-+\w]+) ([+\d]+)( - )([-@.\w]+)( \(\d+\))?\.(\w+)$",currentSubmission):   # same as regex in processFileName() function except ( - ) is replaced with (_)
                    print("Waiting for Dropbox rename")
                    time.sleep(1)
                    currentSubmissions = getSubmissions(validFileExtensions)
                    currentSubmission = min(currentSubmissions, key=os.path.getmtime)
                currentSubmission = min(currentSubmissions, key=os.path.getmtime)
                currentSubmissions.remove(currentSubmission)
                submission = processCurrentSubmission(currentSubmission, assignmentGroups, assignments,classRootDir)
                if submission["valid"]:
                   updateLogFile(submission,"(" + submission["classPeriod"] + " " + submission["Assignment"] + ")" + ' ' + submission["FileName"] + ' * ' + submission["submissionDateTime"] + ' *',False,False)
                   ####################################### 
                   ### COPY, CHECK, and RUN THE PROGRAM
                   #######################################
                   listOfStudentDataFiles = glob.glob(submission["studentDir"] + '/' + submission["Assignment"] + r'_*.txt')
                   result,points,correctFound = assignmentResults(listOfStudentDataFiles)
                   submission["result"] = result
                   timeoutStr = ""
                   if submission["timeout"] > TIMEOUT_DEFAULT:
                       timeoutStr = bcolors.RED + " timeout=" + str(submission["timeout"]) + bcolors.ENDC
                   print("\n"+ bcolors.BOLD + f'*** {submission["Assignment"]} {submission["classPeriod"]} ({result}) {submission["assignmentGroupId"]} *** {submission["FileName"]}' + timeoutStr + bcolors.ENDC + f' {submission["submissionDateTime"]}')
                   if doItAgain:
                      doItAgain = False
                   else:
                      copyFilesToProgramRunDirectory(submission, classRootDir)  ### copy files to student program run directory ###
                   miscompareInFind = findInProgram(submission, classRootDir)   ### if there is a find.txt file, find code in submission
                   goodToRunCheck = True
                   goodToRunProgram = True
                   if miscompareInFind:
                     response = input("  Find check failed. Continue with other checks & run program (y " + bcolors.BLUE + '<ENTER>=n' + bcolors.ENDC + ")? ")
                     if response != 'y':
                        goodToRunCheck = False
                        goodToRunProgram = False
                   checkGood = True
                   if goodToRunCheck:
                       checkGood = runChecker(submission, classRootDir)   ### check the program ###
                   if not checkGood:
                     response = input("  Checker failed. Run program anyways (y " + bcolors.BLUE + '<ENTER>=n' + bcolors.ENDC + ")? ")
                     if response != 'y':
                        goodToRunProgram = False
                   if goodToRunProgram:
                       autoJudgingCorrect = runProgram(submission, classRootDir)   ### run the program ###
                   lCount = 0
                   if autoJudging:
                       if autoJudgingCorrect:
                           submissionCorrect(submission)
                       else:
                           submissionIncorrect(submission,"manualCheck")
                   while not autoJudging:    # loop until a valid response
                       currentSubmissions = getSubmissions(validFileExtensions)
                       if submission["studentName"] != "TestTest":
                          answer = input("  " + bcolors.BOLD + bcolors.BGYELLOW + "y/late/2late/n/p/###" + bcolors.ENDC + " [s d a b h i o g e c m f k t ?](r){x}(" + str(len(currentSubmissions)-1) + ") " + submission["lateInfo"] + "? ")
                       elif submission["studentName"] == "TestTest":
                         print("   *** THIS WAS JUST A TEST RUN ***")
                         response = input("  Confirm removing of file submission & student directory (y " + bcolors.BLUE + '<ENTER>=n' + bcolors.ENDC + ")? ")
                         if response == "y":
                             os.remove(submission["FileName"])  # remove submitted file
                             print("  " + submission["FileName"] + " was removed")                       
                             if os.path.isdir(submission["studentDir"]):
                               rmtree(submission["studentDir"]) # remove student directory 
                         break
                       else:
                           answer = input("  Invalid submission [s rn e c m k](r){x}? ")
                       if answer == "y":  # submission correct. UPDATE scoreboard, CONTINUE to next submission.
                           submissionCorrect(submission)
                           killProcesses(submission)
                           if classPeriod in classPeriodEmailYN:
                               emailStudent(submission,"Your submission was judged to be CORRECT.",False)                           
                           break
                       elif answer == "late":  # submission correct but LATE. UPDATE scoreboard, CONTINUE to next submission.
                           submissionCorrect(submission,"late")
                           killProcesses(submission)
                           break
                       elif answer == "2late":  # submission correct but TOO LATE. UPDATE scoreboard, CONTINUE to next submission.
                           submissionCorrect(submission,"2late")
                           killProcesses(submission)
                           break
                       elif re.search(r"(\d+\.*\d*)",answer):    # submission gets grade. UPDATE scoreboard, CONTINUE to next submission.
                           submissionCorrect(submission,"grade"+answer)
                           killProcesses(submission)
                           break        
                       elif answer == "n":  # submission incorrect. UPDATE scoreboard, CONTINUE to next submission.
                           submissionIncorrect(submission)
                           killProcesses(submission)
                           if classPeriod in classPeriodEmailYN:
                               emailStudent(submission,"Your submission was judged to be INCORRECT.",False)                            
                           break
                       elif answer == "p":   # submission incorrect (presentation error). UPDATE scoreboard, CONTINUE to next submission.
                           submissionIncorrect(submission,"presentationError")
                           killProcesses(submission)
                           break                          
                       elif answer == "s":  # show program in IDE
                           ideCmds = generateIdeCommands(submission)
                           for ideCmd in ideCmds:
                              #print(ideCmd)
                              process = subprocess.Popen(ideCmd, shell=True)
                              time.sleep(0.5)
                              submission["processes"].append(process)
                       elif answer == "d":
                           if Path(os.path.join(submission["studentPgmRunDir"],submission["outputFile"]),os.path.join(submission["goldenAssignmentDir"], "gold.txt")).is_file():   #rpmnew
                               diffCmd = [diffPgm,os.path.join(submission["studentPgmRunDir"],submission["outputFile"]),os.path.join(submission["goldenAssignmentDir"], "gold.txt")]
                               process = subprocess.Popen(diffCmd, shell=True)     # run diff program
                               submission["processes"].append(process)
                           else:
                               print("  ### no golden file, skipping diff")      
                       elif answer == "a":  # run program again
                           print("  Running program again.")
                           doItAgain = True
                           break
                       elif answer == "b":  # bring up file explorer of scoreboard directory
                           process = subprocess.Popen('explorer "' + scoreboardDir + r'\withNames"',creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                           submission["processes"].append(process)  # for some reason the explorer process can not be killed                        
                       elif answer == "h":
                           listOfStudentDataFiles = glob.glob(submission["studentDir"] + '/' + submission["Assignment"] + r'_*.txt')
                           if len(listOfStudentDataFiles) == 0:
                              print("  This is the first submission.")
                           else:
                              listOfStudentDataFilesSorted = sorted(listOfStudentDataFiles,key = os.path.getmtime, reverse=True)
                              for studentDataFile in listOfStudentDataFilesSorted:
                                 print("   ",os.path.basename(studentDataFile))
                       elif answer == "i":
                           if submission["dataInputFileExists"]:
                              infile = os.path.join(submission["studentPgmRunDir"],submission["dataInputFileName"])
                              textEditorCmd = [textEditor,"-n1000000",infile]      
                              process = subprocess.Popen(textEditorCmd, shell=True)
                              submission["processes"].append(process)
                           else:
                              if "dataInputFile" in submission:
                                 print("  Assignment does not have a data input file named")
                                 print("  " + submission["dataInputFile"])
                              else:
                                 print("  Assignment does not have a data input file")
                       elif answer == "o":   # print program output (making newline character visible)
                           outfile = os.path.join(submission["studentPgmRunDir"],submission["outFileName"])                        
                           if os.path.exists(outfile):
                              textEditorCmd = [textEditor,"-n1000000",outfile]      
                              process = subprocess.Popen(textEditorCmd, shell=True)
                              submission["processes"].append(process)   
                           else:
                              print("  File does not exits (" + outfile + ")")
                       elif answer == "g":
                           gradeSubmission(submission)
                       elif answer == "e":  # email student
                           emailStudent(submission)
                       elif answer == "m":  # move submission to 00ManualCheck directory
                           os.rename(os.path.join(classRootDir,submission["FileName"]),os.path.join(submission["classDir"],"00ManualCheck",submission["FileName"]))  #move to 00ManualCheck
                           updateLogFile(submission, "  copied to " + os.path.join(submission["classDir"],"00ManualCheck",submission["FileName"]),True)
                           break
                       elif answer == "?":  # open notes.txt
                           notesFile = os.path.join(submission["studentPgmRunDir"],"notes.txt")
                           textEditorCmd = [textEditor,notesFile]      
                           process = subprocess.Popen(textEditorCmd, shell=True)
                           submission["processes"].append(process)                             
                       elif answer == "f":  # files (open Windows file explorer for student directory)
                           process = subprocess.Popen('explorer "' + submission["studentPgmRunDir"] + '"',creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                           submission["processes"].append(process)  # for some reason the explorer process can not be killed
                       elif answer == "k":
                           killProcesses(submission)
                       elif answer == "r":  # remove submitted file and CONTINUE to next submission
                         response = input("  Confirm remove (y " + bcolors.BLUE + '<ENTER>=n' + bcolors.ENDC + ")? ")
                         if response == "y":
                            if Path(submission["FileName"]).is_file():
                               os.remove(submission["FileName"])  # remove submitted
                               print("  " + submission["FileName"] + " was removed")
                            else:
                               print("  did not find file " + submission["FileName"])
                         updateLogFile(submission, "  removed "  + os.path.join(classRootDir,submission["FileName"]),True)
                         break
                       elif answer == "c":  # clipboard (put email, subject, in Windows-10 clipboard) to enable clipboard history see https://www.howtogeek.com/671222/how-to-enable-and-use-clipboard-history-on-windows-10/
                           comment = commentFromFile(submission)
                           if comment != "cancelComment":
                              if comment:
                                  pyperclip.copy(comment + emailSignature)
                                  time.sleep(0.5)
                              if "studentCode" in submission and submission.get("studentCode","NA") in submission["classRegistration"]:
                                  if len(submission["classRegistration"][submission["studentCode"]]) > 2:  # email address was manually added to REGISTER.txt
                                      receiverEmailAddress = submission["classRegistration"][submission["studentCode"]][2]
                              subject = "P"+ submission.get("classPeriod","???") + "Submission (" + submission.get("Assignment","????") + ")"
                              pyperclip.copy(subject)
                              time.sleep(0.5)
                              pyperclip.copy(receiverEmailAddress)
                              print("  ready to paste (subject & email address)!!!")
                       elif answer == "x":  # exit program
                           print("exiting program")
                           sys.exit()
                       elif answer == "h":
                           webbrowser.open("https://github.com/rainerpm/CSAssignmentChecker#assignment-menu")
                       elif answer == "t":
                           print("timestamp.  Set the submissions time stamp to right now (so other pending programs will be run/judged before this one).")
                           setFileTimestampToNow(submission["FileName"])
                           break
                       else:
                           print("  not a valid answer!!!")
            elif not autoJudging:  # no current submissions (wait for new ones)
                currentSubmissions = getSubmissions(validFileExtensions)
                print("\nPERIOD *",classPeriod,"* waiting for new submissions (<Ctrl-C> in Idle only to go back to main menu) ", end="",flush=True)
                interrupted = False 
                while len(currentSubmissions) == 0:  # wait for more submissions
                    print(".", end="",flush=True)
                    if classPeriod == str(classPeriodForCompetitions):
                        movedFilesJava   = moveFilesFromDirToDir(customDirectoryForUILComp,classRootDir,".java")
                        movedFilesPython = moveFilesFromDirToDir(customDirectoryForUILComp,classRootDir,".py")
                        if movedFilesJava or movedFilesPython:
                            print(f'moved files to Period {classPeriod} from {customDirectoryForUILComp}')                                       
                    time.sleep(2)
                    currentSubmissions = getSubmissions(validFileExtensions)
                    if interrupted:
                        # update scoreboard for every assignment group in the class
                        aKeys = list(assignmentGroups.keys())
                        aKeys.sort()
                        for aGroupId in aKeys:
                            aDict = assignmentGroups[aGroupId]
                            aGroupDir = aDict["assignmentGroupDir"]
                            listOfAssignments = aDict["listOfAssignments"]
                            CSACscoreboard.updateScoreboard(scoreboardDir,aGroupDir,aGroupId,classPeriod,listOfAssignments)
                        break
                print()
            else:   # autojudging and all test in directory have been processed
                autoJudgingPeriods = autoJudgingPeriods[1:] + list(autoJudgingPeriods[0])
                #print("sleep",autoJudgingSleepTime)
                time.sleep(autoJudgingSleepTime)
                break
            if interrupted:  # if there is an interrupt go back to asking for class
                interrupted = False
                print()
                break

main()