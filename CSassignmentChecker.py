# summer improvements
# 1) Deal with studnets submitting a file with a unsupported file extension(.py, .java, or .zip only no .txt or .java.java)
# 2) MABYE: Move scoreboards into a class directory so all the scoreboards for a class are in one directory
# 3) add a password to StudentDrop (maybe not necessary since a 6 digit secret code should be good enough)
# 4) Make a "contest" StudentDrop
# 5) Put a code in the scoreboard for manually moving a program to manual judging. This already
#    exists when autojudging, but not when chosing 'm' to move it manually.
# 6) Combine zip files into 1 file (alphabetically) for 00PLAGIARISM (see combineJAVAFilesFromZIPFile.py)

#DBG print(f'{getframeinfo(currentframe()).lineno}: {var=}')


import scoreboard  # import the associated scoreboard.py which creates the scoreboard files
from scoreboard import assignmentResults    
from login import emailSendFromAddress, emailSendFromPassword
from customize import validClassPeriods,rootDir,scoreboardDir,scoreboardDirAlt,mossDir,pythonIde,javaIde,diffPgm,textEditor,emailSignature,emailAttachmentFile, TIMEOUT_DEFAULT

# import python libraries (using Python 3.10 only ones that need to be installed
# using 'pip install' appear to be pyperclip and pillow).
import os
import glob
import subprocess
import re
import time
import sys
import signal  # for interrupting waiting for submissions with CTRL-C
import json   # for pretty printing dictionaries
from   datetime import datetime
from   pathlib  import Path
from   shutil   import copyfile
from   shutil   import copy
from   shutil   import rmtree
import ssl     # for gmail
import smtplib # for gmail & outlook
from   email.mime.text      import MIMEText      # for outlook
from   email.mime.multipart import MIMEMultipart # for outlook
from   email.mime.base      import MIMEBase      # for outlook
from   email                import encoders      # for outlook
from   PIL      import ImageGrab                 # pip install pillow
import pyperclip        # allows python to add things to the clipboard (so it can be quickly pasted)
#from icecream import ic
import webbrowser
import os
from twilio.rest import Client
# to get the line number of a Python statement
from inspect import currentframe, getframeinfo

validFileExtensions = [".py",".java",".zip",".txt"] # .py for python, .java/.zip for java, .txt for registration file

# Check variables set in customize.py
initError = False

if not Path(rootDir).is_dir():
    initError = True
    print("ERROR!!! root directory does not exist (" + rootDir + ")")
else:
    if not Path(rootDir,"ASSIGNMENT_GROUPS").is_dir():
        initError = True
        print("ERROR!!! ASSIGNMENT_GROUPS directory does not exist in " + rootDir)

if not Path(scoreboardDir).is_dir(): 
    if not Path(scoreboardDirAlt).is_dir():
        scoreboardDir = scoreboardDirAlt
    else:
        initError = True
        print("ERROR!!! scoreboard directory does not exist (" + scoreboardDir + ")")

if not Path(pythonIde).is_file(): 
    initError = True
    print("ERROR!!! Python IDE not found @ " + pythonIde)

if not Path(javaIde).is_file():
    initError = True
    print("ERROR!!! JAVA IDE not found @ " + javaIde)

if not Path(diffPgm).is_file():
    initError = True
    print("ERROR!!! Diff program not found @ " + diffPgm)

if not Path(textEditor).is_file():
    initError = True
    print("ERROR!!! TextEditor not found @ " + textEditor)
textEditorCmdOpt1 = [textEditor,r'-nosession',r'-multiInst',r'-n1000000']
#textEditorCmdOpt1 = [textEditor,r'-nosession',r'-n1000000']

if initError:
    exit()


### REGISTRATION
registrationRequired = True


# Use Ctrl-C to stop waiting for new submissions
def signal_handler(signal, frame):
    global interrupted
    interrupted = True

signal.signal(signal.SIGINT, signal_handler)

def check4Activity():
    print("*** Checking for new file submissions ***")
    listOfDirectoriesInRootDir = [p.name for p in Path(rootDir).iterdir() if p.is_dir()]  # getting-a-list-of-all-subdirectories-in-the-current-directory
    for classPeriod in listOfDirectoriesInRootDir:
        files = []
        if classPeriod in validClassPeriods:
            print("Class Period",classPeriod)
            files =[p for p in Path(rootDir,classPeriod).iterdir() if p.is_file()]
            for file in files:
               if file.name != "REGISTER.txt":
                  ##RPM1 if file.name.endswith("registerMe.txt"):
                  ##RPM1   print(" ", datetime.fromtimestamp(file.stat().st_mtime).strftime("%b%d %Hh%Mm"), "REGISTER",">"+file.name+"<")
                  if file.suffix not in validFileExtensions:
                     print(" ","File with incorrect extension",">" + file.name + "<")
                  else:
                     print(" ", datetime.fromtimestamp(file.stat().st_mtime).strftime("%b%d %Hh%Mm"), ">"+file.name+"<")
            files =[p for p in Path(rootDir,classPeriod,"00ManualCheck").iterdir() if p.is_file()]
            for file in files:
               print("  ..", "manual check -> ", datetime.fromtimestamp(file.stat().st_mtime).strftime("%b%d %Hh%Mm"), ">"+file.name+"<")
               
            #DEL for extension in validFileExtensions:
            #DEL     files = files + glob.glob(os.path.join(rootDir,classPeriod,r"*"+extension))
            #DEL if files:
            #DEL     files.sort(key=os.path.getmtime)
            #DEL     for file in files:
            #DEL         fname = Path(file)
            #DEL         print(" ", datetime.fromtimestamp(fname.stat().st_mtime).strftime("%b%d %Hh%Mm"), os.path.basename(file))


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
                if len(fields) < 5:  # if registration does not have email
                    code, name, classPeriod = fields
                    email = ""
                else:
                    code, nameLast, nameFirst, classPeriod, email = fields
                name = nameLast + " " + nameFirst
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
    return classRegistration

def setup():
    listOfGlobalAssignmentGroupDirectories = [f.name for f in os.scandir(os.path.join(rootDir,"ASSIGNMENT_GROUPS")) if f.is_dir()]  # https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
    allAssignmentGroups = {}
    allAssignments = {}
    for globalAssignmentGroupDirOnly in listOfGlobalAssignmentGroupDirectories:  # iterate over assignment group directories in ASSIGNMENT_GROUPS directory
        globalAssignmentGroupDir = os.path.join(rootDir,"ASSIGNMENT_GROUPS",globalAssignmentGroupDirOnly)
        classesFile = os.path.join(globalAssignmentGroupDir,"periods.txt")
        if os.path.exists(classesFile): 
           with open(classesFile, "r") as cfile:
               classPeriods = cfile.read().replace("\n"," ").split()
        else:
           #RPM sthorten to parent and basename
           print("Did not find file period.txt in",globalAssignmentGroupDir)
        for classPeriod in classPeriods:
            classPeriodsDir = os.path.join(rootDir,classPeriod)
            if not os.path.isdir(classPeriodsDir):
                os.mkdir(classPeriodsDir)
                print("Created directory",classPeriodsDir)
            classAssignmentGroupDir = os.path.abspath(os.path.join(rootDir,classPeriod,globalAssignmentGroupDirOnly))  # abspath necessary to open file explorer for main menu 'f' option
            if not os.path.isdir(classAssignmentGroupDir):
                os.mkdir(classAssignmentGroupDir)
                print("Created directory",classAssignmentGroupDir)
            latestResultsDir = os.path.join(rootDir,classPeriod,"latestResults")
            if not os.path.isdir(latestResultsDir):
                os.mkdir(latestResultsDir)
                print("Created directory",latestResultsDir)
            autoJudgeManualCheckDir = os.path.join(rootDir,classPeriod,"00ManualCheck")
            if not os.path.isdir(autoJudgeManualCheckDir):
                os.mkdir(autoJudgeManualCheckDir)                
                print("Created directory",autoJudgeManualCheckDir)
            plagiarismDir = os.path.join(classAssignmentGroupDir,"00PLAGIARISM")
            if not os.path.isdir(plagiarismDir):
                os.mkdir(plagiarismDir)
                copy(os.path.join(mossDir,"moss.pl"),plagiarismDir)  
                copy(os.path.join(mossDir,"moss_java.bat"),plagiarismDir)                
                copy(os.path.join(mossDir,"moss_python.bat"),plagiarismDir)                
                print("Created directory",plagiarismDir)
            assignmentGroup = {}  # create content dict, then add to it
            assignmentGroup["assignmentGroupDir"] = classAssignmentGroupDir
            assignmentGroup["goldenDir"] = globalAssignmentGroupDir   # this is in the GLOBAL assignment group directory
            assignmentGroup["plagiarismDir"] = plagiarismDir
            assignments = {}
            assignmentGroups = {}
            listOfAssignments = [f.name for f in os.scandir(globalAssignmentGroupDir) if f.is_dir()]  # https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
            listOfAssignments.sort()
            assignmentGroup["listOfAssignments"] = listOfAssignments
            for assignment in listOfAssignments:
                assignments[assignment] = globalAssignmentGroupDirOnly
            assignmentGroups[globalAssignmentGroupDirOnly] = assignmentGroup
            if classPeriod in allAssignmentGroups:
                allAssignmentGroups[classPeriod].update(assignmentGroups)
            else:
                allAssignmentGroups[classPeriod] = assignmentGroups
            if classPeriod in allAssignments:
                allAssignments[classPeriod].update(assignments)
            else:
                allAssignments[classPeriod] = assignments
    return allAssignmentGroups, allAssignments

def emailStudent(submission):
    receiverEmailAddress = ""
    if "studentCode" in submission and submission["studentCode"] in submission["classRegistration"]:
        if len(submission["classRegistration"][submission["studentCode"]]) > 2:  # email address was manually added to REGISTER.txt
            receiverEmailAddress = submission["classRegistration"][submission["studentCode"]][2]
    if not receiverEmailAddress:  # student is in classRegistration dictionary but email is blank OR student is not in dictionary
        receiverEmailAddress = input("  enter student's email address -> ")
    if "Assignment" in submission:
        subject = "P"+ submission["classPeriod"] + " StudentDrop (" + submission["Assignment"] + ")"
    else:
        subject = "StudentDrop Error"
    print("  Preparing to send", subject, "email to", receiverEmailAddress)
    comment = commentFromFile(submission)
    response = ""
    if comment != "cancelComment":
       response = input("  attach image from clipboard (y)? ")
       attachment = ""
       if response == "y":
           while True:
              image = ImageGrab.grabclipboard()
              haveImage = True
              if image == None:
                haveImage = False
                print("  No image found on top of clipboard.")
                response = input("  <enter> to try again or <q>uit trying? ")
                if response == 'q':
                   break
              else:
                 break
           if haveImage:
              imageJpg = image.convert('RGB')
              imageJpg.save(emailAttachmentFile,'JPEG')
              attachment = emailAttachmentFile
              comment = comment + "\nBe sure to look at the e-mail attachment."
       updateLogFile(submission, "  email msg -> " + comment)
       message = comment + emailSignature
       emailSent = emailWithOutlook(emailSendFromAddress,emailSendFromPassword,receiverEmailAddress,subject,message,attachment)
       if emailSent:
          print("  Email sent.")

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

# https://medium.com/@neonforge/how-to-send-emails-with-attachments-with-python-by-using-microsoft-outlook-or-office365-smtp-b20405c9e63a
def emailWithOutlook(email_sender,email_password,email_recipient,email_subject,email_message,attachment_location=""):
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
         response = input("  Comment (g[#], l[#], (o)ne-time comment, (n)o comment, (c)ancel? ")
         if matchResponse := re.match('([glonc])(\w*)',response):
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
         commentsLocalFile = os.path.join(submission["goldenAssignmentDir"],"comments.txt")
         if os.path.exists(commentsLocalFile):         
             textEditorCmd = [textEditor,commentsLocalFile]      
             process = subprocess.Popen(textEditorCmd, shell=True)
             submission["processes"].append(process)
         commentsGlobalFile = os.path.join(rootDir,"ASSIGNMENT_GROUPS","comments"+submission["language"].upper()+".txt")
         if os.path.exists(commentsGlobalFile):         
             textEditorCmd = [textEditor,commentsGlobalFile]      
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
                  if matchResponse := re.match('comment (\w+)',line):
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
               print("    comment",commentNameResponse,"was not found.")
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
         comment = "cancelComment"
   print("  comment -> " + comment[:40].rstrip() + " ...")
   return comment

def openErrorFile(submission,errorType):
   if errorType == "compile":
      errFile = submission["compileErrorFileName"] 
   else:
      errFile = submission["runTimeErrorFileName"]
   errorFileSize = Path(errFile).stat().st_size
   if errorFileSize != 0:  # had errors
     if not autoJudging:
         response = input("  " + errorType + " error!!!  Open error file (y)? ")
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
         print(f'  Code >{code}< is not registered for {nameFirst} {nameLast}!!!') 
         foundNameInRegistration = False
      elif classRegistration[code][0] != name:
         print("  Name mismatch!!! >" + code + "< code registered as",classRegistration[code][0],"and not",name)
         foundNameInRegistration = False
   return foundNameInRegistration

def processFileName(fname):
   nameLast = nameFirst = code = nameLastPartner = nameFirstPartner = codePartner = assignment = ""
   # File Submission:   LastName FirstName Code - assignmentName.ext
   # For group submissions LastName FirstNamae Code will contain a + sign between
   #   individual student's names/codes.
   validFname = re.search("^([-+\w]+) ([-+\w]+) ([+\d]+) - (\w+)\.(\w+)$",fname)
   if validFname:
      nameLast = validFname.group(1).strip()
      nameFirst = validFname.group(2).strip()
      code = validFname.group(3).strip()
      assignment = validFname.group(4).strip()
      suffix = validFname.group(5).strip()
      #DBG print(f'{getframeinfo(currentframe()).lineno}: {nameLast=} {nameFirst=} {code=} {assignment=} {suffix=}')
   return validFname,nameLast,nameFirst,code,assignment
   
def processCurrentSubmission(currentSubmission, assignmentGroups, assignments,classRootDir):
   submission = {}
   submission["valid"] = False
   submission["classPeriod"] = os.path.basename(os.getcwd())
   submission["classPeriodDir"] = Path(classRootDir)
   submission["FileName"] = currentSubmission
   submission["submissionDateTime"] = datetime.fromtimestamp(Path(submission["FileName"]).stat().st_mtime).strftime("%b_%d_%Hh%Mm%Ss")
   submission["classDir"] = classRootDir;
   # check submission
   validFileName, nameLast, nameFirst, code, assignment = processFileName(submission["FileName"])

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
         
   submission["classRegistration"] = loadRegisteredStudents(submission["classPeriodDir"],assignmentGroups)

   if assignment == "registerMe":
      registrationOK = True
   else:
      if submission["groupSubmission"]:
         registrationOK = True
         for i in range(len(submission["groupLastNames"])):
            studentRegistered = checkStudentRegistration(submission["FileName"],submission["groupLastNames"][i],submission["groupFirstNames"][i],submission["groupCodes"][i],submission["classRegistration"])
            registrationOK = registrationOK and studentRegistered
      else:
         registrationOK = checkStudentRegistration(submission["FileName"],nameLast,nameFirst,code,submission["classRegistration"])

   if (assignment in assignments):   
       submission["assignmentGroupId"] = assignments[assignment]  # assignment group assignment belongs to
       assignmentGroup = assignmentGroups[submission["assignmentGroupId"]]  # dictionary with info for this assignment group
       submission["assignmentGroup"] = assignmentGroup
       submission["listOfAssignments"] = assignmentGroup["listOfAssignments"]

       if validFileName and not(assignment in submission["listOfAssignments"]):
          print("  Assignment >"+assignment+"< is not in group "+submission["listOfAssignments"])   

   if validFileName and not((assignment in assignments) or (assignment == "registerMe")):
      print("  Invalid Assignment Name: >"+assignment+"<")
      
   if validFileName and ((assignment in assignments) or (assignment == "registerMe")) and registrationOK and (assignment == "registerMe" or (assignment in submission["listOfAssignments"])):
      submission["Assignment"]  = assignment
      submission["registration"] = submission["Assignment"] == "registerMe"  # student submitted a registration request
      if submission["groupSubmission"]:
         submission["studentName"] = submission["groupLastNames"][0] + " " + submission["groupFirstNames"][0]  # for a group submission the student run directory is in the 1st student of the groups student directory
         submission["studentCode"] = submission["groupCodes"][0]
      else:
         submission["studentName"] = nameLast + " " + nameFirst
         submission["studentCode"] = code
      submission["nameForLatestDir"] = submission["studentName"]

      if submission["registration"]:   
         if submission["studentCode"] in submission["classRegistration"]:
             print(" ",submission["studentCode"], "is already registered")
             print("    previous registration", submission["classRegistration"][submission["studentCode"]])
             print("    current submission   ", submission["FileName"])
             input("Incorrect registration. Press any key to delete current submission and continue ... ") 
         else:
             with open("REGISTER.txt", "a") as freg:
                 registrationCode = ""
                 email = ""
                 with open(submission["FileName"],"r") as sreg:
                    registrationCode = sreg.readline().strip()
                    email = sreg.readline().strip()
                 if registrationCode and email: 
                    if registrationCode == submission["studentCode"]:    
                       freg.write(f'{submission["studentCode"]} {submission["studentName"]} {submission["classPeriod"]} {email}\n')
                       print('  ' + submission["studentName"] + ' was registered (' + submission["studentCode"] + ' ' + email + ')')
                    else:
                       print("  " + registrationCode + "code in the REGISTER.txt file does not match one in submission (" + submission["studentCode"] + ")")
                       input("Incorrect registration. Press any key to delete current submission and continue ... ") 
                 else:
                    print("  Registration code and email not found on first two lines of " + submission["FileName"])
                    input("Incorrect registration. Press any key to delete current submission and continue ... ") 
             #submission["classRegistration"] = loadRegisteredStudents(submission["classPeriod"],assignmentGroups)
         os.remove(submission["FileName"])  # remove registration file (assignment name was register, file has served its purpose)
      else:   
         submission["valid"] = True
         submission["processes"] = []
         submission["FileNameRoot"] = os.path.splitext(submission["FileName"])[0]
         submission["FileExtension"] = os.path.splitext(submission["FileName"])[1]
         if submission["FileExtension"] == ".py":
           submission["language"] = "python"
         else:
           submission["language"] = "java"
         if submission["FileExtension"] == ".zip":
           submission["assignmentFileName"] = submission["Assignment"] + ".java"
         else:
           submission["assignmentFileName"] = submission["Assignment"] + submission["FileExtension"]
         submission["submittedFileNameWithDate"] = submission["FileNameRoot"] + "_" + submission["submissionDateTime"] + submission["FileExtension"]
         submission["outFileName"] = submission["Assignment"] + "_out.txt"
         submission["outCheckFileName"] = submission["Assignment"] + "_check.txt"
         submission["outCorrectFileName"] = submission["Assignment"] + "_" + submission["submissionDateTime"] + "_out_CORRECT.txt"
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
         submission["goldCheckFile"] = os.path.join(submission["goldenAssignmentDir"], "checker.txt")
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
         submission["outputFile"] = os.path.join(submission["studentPgmRunDir"],submission["outFileName"])
         if submission["groupSubmission"]:
           partnersDirs = []
           for i in range(len(submission["groupLastNames"])):
              partnerName = submission["groupLastNames"][i] + " " + submission["groupFirstNames"][i]
              partnerCode = submission["groupCodes"][i]
              print(f'{getframeinfo(currentframe()).lineno}: {partnerName=} {partnerCode=}')
              partnerDir = os.path.join(submission["assignmentGroupDir"],partnerName + "_" + partnerCode)
              partnersDirs.append(partnerDir)
              if not os.path.isdir(partnerDir):
                 os.mkdir(partnerDir)                
           submission["partnersDirs"] = partnersDirs

   else:
      updateLogFile(submission, "  File submission error (" + submission["FileName"] + ")",True)
      pyperclip.copy(submission["FileName"])
      time.sleep(0.5)
      for key,value in submission["classRegistration"].items():
         print(f'    {key} {value[0]}')
      while True:
         response = input("  New name (clipboard), (r)emove submission (m)ove to manual check? ")
         if response == 'r':
            os.remove(submission["FileName"])
            updateLogFile(submission, "  removed "  + os.path.join(classRootDir,submission["FileName"]),True)
            break
         elif response == 'm':
            os.rename(os.path.join(classRootDir,submission["FileName"]),os.path.join(submission["classDir"],"00ManualCheck",submission["FileName"]))  #move to 00ManualCheck
            updateLogFile(submission, "  copied to " + os.path.join(submission["classDir"],"00ManualCheck",submission["FileName"]),True)
            break
         elif response != '':
            os.rename(submission["FileName"], response)  # rename to new name
            break
         
   return submission

def copyFilesToProgramRunDirectory(submission, classRootDir):
    goldenAssignmentDir = submission["goldenAssignmentDir"]
    if submission["FileExtension"] == ".java":
        # DOESN'T WORK CURRENTLY, since this will get a compile error that class name does not match file name
        #       I will have to fix how (and how many) files get compiled.
        # copyfile(os.path.join(classRootDir,submission["FileName"]),os.path.join(submission["studentPgmRunDir"],submission["FileName"]))  # copy submitted file 
        copyfile(os.path.join(classRootDir,submission["FileName"]),os.path.join(submission["studentPgmRunDir"],submission["assignmentFileName"]))  # copy so filename matches assignment name for java
    else:  # .zip files or Python .py files
        copyfile(os.path.join(classRootDir,submission["FileName"]),os.path.join(submission["studentPgmRunDir"],submission["FileName"]))
    os.chdir(submission["studentPgmRunDir"])
    if submission["FileExtension"] == ".zip":
       result = subprocess.run(["tar", "-xf", submission["FileName"]])  # EXTRACT zip file
       files =[p for p in Path('.').iterdir() if p.is_file()]
       for file in files:
           if file.suffix != ".java" and file.suffix != ".zip":
              print("  Error!!! Student zip file contains something other than a .java file (" + file.name + ")")
              break
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

def checkProgram(submission, classRootDir):
    checked = True
    os.chdir(submission["studentPgmRunDir"])
    if os.path.exists(os.path.join(submission["Assignment"] + "Checker.java")):
       compileCmd = ["javac", "-parameters", submission["Assignment"] + "Checker.java"]
       with open("CompilerOutput.txt", "w") as fout:
           with open(submission["compileErrorFileName"], "w") as ferr:
               result = subprocess.run(compileCmd, stdout=fout, stderr=ferr)  #COMPILE CHECKER
       errorCompile = openErrorFile(submission,"compile")

       if errorCompile:
           checked = False
       else:
           runCmd = ["java", submission["Assignment"] + "Checker"]
           with open(submission["outCheckFileName"], 'w') as fout:
              result = subprocess.run(runCmd, stdin=None, stdout=fout, stderr=None)   # run Checker
           checkFilesMatches = filesMatch(submission["outCheckFileName"],submission["goldCheckFile"])
           if checkFilesMatches:
               print("  >>> CHECK CORRECT <<<")
           else:
               print("  ### miscompare (opening diff) ###")
               diffCmd = [diffPgm,submission["outCheckFileName"],submission["goldCheckFile"]]
               process = subprocess.Popen(diffCmd, shell=True)     # run diff program
               submission["processes"].append(process)
               checked = False
    os.chdir(classRootDir)
    return checked

def runProgram(submission, classRootDir):
    autoJudgingCorrect = False
    error = False
    os.chdir(submission["studentPgmRunDir"])
    if submission["language"] == "python":
        compileCmd = ["python","-m","py_compile",submission["FileName"]]
        runCmds = [["python", submission["FileName"]]]
    elif submission["language"] == "java":
        compileCmd = ["javac", "-parameters", "*.java"]
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
        print("ERROR!!! Unsupported language")
        sys.exit()
    # language independant code
    with open("CompilerOutput.txt", "w") as fout:
        with open(submission["compileErrorFileName"], "w") as ferr:
            result = subprocess.run(compileCmd, stdout=fout, stderr=ferr)  #COMPILE PROGRAM
    errorCompile = openErrorFile(submission,"compile")
    ideCmds = generateIdeCommands(submission)
    bringUpIDEorDataFile = '\nset /P c=Bring up IDE [y]? \nif /I "%c%" EQU "Y" goto :ide\ngoto :next\n:ide\n'
    for ideCmd in ideCmds:
       bringUpIDEorDataFile = bringUpIDEorDataFile + '\nSTART /B "' + ideCmd[0] + '"' + ' ' + '"' + ideCmd[1] + '"'
    bringUpIDEorDataFile = bringUpIDEorDataFile + '\n:next'
    latestResultsDir = os.path.join(classRootDir,"latestResults")
    if submission["dataInputFileExists"]:
        bringUpIDEorDataFile += '\nset /P c=Bring up input data file [y]? \nif /I "%c%" EQU "Y" goto :idf\ngoto :end\n:idf\n' + '"' + textEditor + '"' + " -multiInst -nosession " + '"' + submission["dataInputFileName"] + '"' + '\n:end'
    if errorCompile:
        copyfile(submission["compileErrorFileName"], os.path.join(latestResultsDir,submission["nameForLatestDir"] + "_compileError.txt"))  # copy compile error file to class directory
        copyfile(submission["compileErrorFileName"], os.path.join(submission["studentDir"],submission["compileErrFileName"]))  # copy output file to data directory
        if submission["groupSubmission"]:
           for partnerDir in submission["partnersDirs"]:
              copyfile(submission["compileErrorFileName"],os.path.join(partnerDir,submission["compileErrFileName"]))  # copy output file to all partners data directories        
        updateLogFile(submission, "  ERROR!!! " + submission["FileName"] + " had a compile time error.",False)
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
                                     print("  Timed Out (>" + str(submission["timeout"]) + "sec)!!! " + str(runCmd))
                                     timedOut = True
                               writeOrAppend = "a"
                     #runStdin.close()
               else:
                  with open(submission["outFileName"], writeOrAppend) as fout:
                      with open(submission["runTimeErrorFileName"], writeOrAppend) as ferr:
                            if not timedOut:
                               try:
                                  result = subprocess.run(runCmd, stdin=runStdin, stdout=fout, stderr=ferr, timeout=submission["timeout"])   # run submitted RUNNER or student program without a user input file      
                               except:                         
                                  print("  Timed Out (>" + str(submission["timeout"]) + "sec)!!! " + str(runCmd))
                                  timedOut = True
                            writeOrAppend = "a"
            else:
               with open(submission["outFileName"], writeOrAppend) as fout:
                   with open(submission["runTimeErrorFileName"], writeOrAppend) as ferr: 
                      result = subprocess.run(runCmd, stdin=runStdin, stdout=fout, stderr=ferr)   # run Tester
                      writeOrAppend = "a"
        errorRun = openErrorFile(submission,"runtime")
        if errorRun:
            if os.path.exists(submission["outFileName"]):
                os.remove(submission["outFileName"])
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
            updateLogFile(submission, "  ERROR!!! " + submission["FileName"] + " had a run time error.",False)
        else:
            if os.path.exists(os.path.join(latestResultsDir,submission["nameForLatestDir"] + "_runTimeError.txt")):
                os.remove(os.path.join(latestResultsDir,submission["nameForLatestDir"] + "_runTimeError.txt"))
    error = errorCompile or errorRun
    if not error:
        goldFileMatches = filesMatch(submission["outputFile"],submission["goldFile"])
        if goldFileMatches:
            print("  *** RUN CORRECT ***")
            autoJudgingCorrect = True    
        else:
            if autoJudging:
                print("  INCORRECT (autojudged)")
            else:
                print("  ### miscompare (opening diff) ###")
                diffCmd = [diffPgm,submission["outputFile"],submission["goldFile"]]
                process = subprocess.Popen(diffCmd, shell=True)     # run diff program
                submission["processes"].append(process)
            with open(os.path.join(submission["studentPgmRunDir"], "diff.bat"), "w") as fdiff:
                fdiff.write('"' + diffPgm + '"' + " " + submission["outFileName"] + " " + os.path.join(submission["goldenAssignmentDir"], "gold.txt"))
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
    listOfSubmissions.remove("REGISTER.txt")
    return listOfSubmissions

def updateLogFile(submission, logMessage, alsoPrint = False, indent=True):
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

### using this program instead C:\Users\E151509\Google Drive\My LASA\misc\tools\moss plagiarize checking\prepZipFilesForMoss.py
##def combineFilesInZipFile(directory,mergedFile):
##    zipfile = os.path.join(directory,mergedFile)
##    print("NEW1a",os.getcwd())
##    if os.path.exists("tempZipDir"):
##       rmtree("tempZipDir")
##    os.mkdir("tempZipDir")
##    result = subprocess.run(["tar", "-xf", zipfile,"-C","tempZipDir"])  # EXTRACT zip file
##    os.chdir("tempZipDir")
##    javaFiles = glob.glob(r"*.java")
##    print("NEW1b",javaFiles)
##    data = data2 = ""
##    # Reading data from file1
##    with open(javaFiles[0]) as fp:
##       data = fp.read()
##    for javaFile in javaFiles[1:]:
##      # Reading data from file2
##      with open(javaFile) as fp:
##          data2 = fp.read()
##      # Adding next file to data
##      data += "\n\n\n"
##      data += data2     
##    with open ("temp" + ".java", 'w') as fp:
##       fp.write(data)
##    # move file and remove white space from filename for moss to work
##    print("NEW1c",os.getcwd())
##    os.rename(os.path.join(os.getcwd(),"temp.java"), os.path.join(directory,mergedFile + ".java"))  # move file
##    print("NEW1d",mergedFile + ".java")
##    os.chdir("..")
##    time.sleep(0.5)
##    rmtree("tempZipDir")

def submissionCorrect(submission):
    with open(os.path.join(rootDir,"CORRECT.txt"), "a") as fcorr:
       assignmentGroup = os.path.basename(os.path.normpath(submission["assignmentGroup"]["assignmentGroupDir"]))
       assignmentGroup = assignmentGroup[:27]+">" if len(assignmentGroup) > 27 else assignmentGroup
       assignment = submission["Assignment"]
       assignment = assignment[:11]+">" if len(assignment) > 11 else assignment
       fcorr.write(f'P{submission["classPeriod"]}  {assignmentGroup:<28} {submission["result"]} {assignment:<12} {submission["FileName"]} * {submission["submissionDateTime"]}\n')        
        #fcorr.write("(P" + submission["classPeriod"] + " " + os.path.basename(os.path.normpath(submission["assignmentGroup"]["assignmentGroupDir"])) +") " + submission["Assignment"] + " " + submission["FileName"] + " * " + submission["submissionDateTime"] + " *\n") 
    if not os.path.exists(os.path.join(submission["plagiarismAssignmentDir"],submission["submittedFileNameWithDate"])):
       os.rename(submission["FileName"], os.path.join(submission["plagiarismAssignmentDir"],submission["submittedFileNameWithDate"]))  # move pgm to PLAGIARISM directory
       #if submission["FileExtension"] == ".zip":
       #   combineFilesInZipFile(submission["plagiarismAssignmentDir"],submission["submittedFileNameWithDate"])
    else:
        os.remove(submission["FileName"])       # remove submission file (this only happens if the same file with the same time stamp is copied into class directory)
    if Path(submission["studentPgmRunDir"],submission["outFileName"]).is_file():  
       copyfile(os.path.join(submission["studentPgmRunDir"],submission["outFileName"]), os.path.join(submission["studentDir"],submission["outCorrectFileName"]))  # copy output file to data directory
       if submission["groupSubmission"]:
          for partnerDir in submission["partnersDirs"]:
             copyfile(os.path.join(submission["studentPgmRunDir"],submission["outFileName"]), os.path.join(partnerDir,submission["outCorrectFileName"]))  # copy output file to partner's data directory
    else:     # (outFileName file may not exist (maybe program was manually deemed to be correct)
       copyfile(os.path.join(submission["goldFile"]), os.path.join(submission["studentDir"],submission["outCorrectFileName"]))  # copy output file to data directory
       if submission["groupSubmission"]:
          for partnerDir in submission["partnersDirs"]:
             copyfile(os.path.join(submission["goldFile"]), os.path.join(partnerDir,submission["outCorrectFileName"]))  # copy output file to all partners data directories
    scoreboard.updateScoreboard(scoreboardDir,submission["assignmentGroupDir"],submission["assignmentGroupId"],submission["classPeriod"],submission["listOfAssignments"])
    updateLogFile(submission, "  *** CORRECT *** ")

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
        scoreboard.updateScoreboard(scoreboardDir,submission["assignmentGroupDir"],submission["assignmentGroupId"],submission["classPeriod"],submission["listOfAssignments"])
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
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(process.pid)])
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
            validClassPeriodsString = ""
            for classPeriod in validClassPeriods:
                validClassPeriodsString = validClassPeriodsString + classPeriod + " "
            validClassPeriodsString = validClassPeriodsString.rstrip()
            response = input("\n" + "("+ validClassPeriodsString + ")judge (a)utojudge score(b)oard (l)og (f)iles e(x)it (<ENTER>=check)? ")
            inputContinue = (response == 'x') or (response in validClassPeriods)
            if response in validClassPeriods:
                classPeriod = response
                manualCheckFiles = os.listdir(Path(rootDir,classPeriod,"00ManualCheck"))
                if len(manualCheckFiles) > 0:
                   response = input("Move " + str(len(manualCheckFiles)) + " files from 00ManualCheck to class directory to be judged (y)? ")
                   if response == 'y':
                      for file in manualCheckFiles:
                         os.rename(Path(rootDir,classPeriod,"00ManualCheck",file),Path(rootDir,classPeriod,file))
            elif response == "a":
                response2 = input("(" + validClassPeriodsString + ")autojudge (m)ultiple (<ENTER>=all periods)? ")
                autoJudging = True
                autoJudgingFirstTime = False
                if response2 in validClassPeriods:
                    classPeriod = response2
                    autoJudgingPeriods = [classPeriod]
                    autoJudgingSleepTime = 30
                elif response2 == "m":
                    response3 = input("Enter comma separated list of class periods (e.g. 1,4,5)? ")
                    autoJudgingPeriods = response3.split(",")
                    autoJudgingSleepTime = 30
                else:
                    autoJudgingPeriods = validClassPeriods
                moveTo00ManualCheck = False
                response3 = input("incorrect to 00ManualCheck directory (instead of judging incorrect)(y)? ")
                if response3 == 'y':
                   moveTo00ManualCheck = True
            elif response == "l":   # log
                textEditorCmd = textEditorCmdOpt1 + ["logGlobal.txt"]      
                result = subprocess.run(textEditorCmd, shell=True)
            elif response == "f":   # file explorer
                process = subprocess.Popen('explorer "' + os.path.normpath(rootDir) + '"',creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
            elif len(response) > 0 and response[0] == "b":
               process = subprocess.Popen('explorer "' + scoreboardDir + '\withNames"',creationflags=subprocess.CREATE_NEW_PROCESS_GROUP) # bring up file explorer of scoreboard directory
            elif response == "x":
                sys.exit()

        if autoJudging:
            classPeriod = autoJudgingPeriods[0]
            print(classPeriod,end="")


        classRootDir = os.path.join(rootDir,classPeriod)  # CLASSROOTDIRassignment (directory for submissions)
        os.chdir(classRootDir)

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
        # get dictionary of all registered students and create student directory
        # NOW part of submission["classRegistration"] dictionary
        # classRegistration = loadRegisteredStudents(classRootDir,assignmentGroups)
      
        doItAgain = False
        while True:  # loop over each program, run the oldest first
            interrupted = False
            correct = False
            currentSubmissions = getSubmissions(validFileExtensions)
            if len(currentSubmissions) > 0:
                currentSubmission = min(currentSubmissions, key=os.path.getmtime)
                currentSubmissions.remove(currentSubmission)
                submission = processCurrentSubmission(currentSubmission, assignmentGroups, assignments,classRootDir)
                if submission["valid"]:
                   updateLogFile(submission,"(P" + submission["classPeriod"] + " " + submission["Assignment"] + ")" + ' ' + submission["FileName"] + ' * ' + submission["submissionDateTime"] + ' *',False,False)
                   ####################################### 
                   ### COPY, CHECK, and RUN THE PROGRAM
                   #######################################
                   listOfStudentDataFiles = glob.glob(submission["studentDir"] + '/' + submission["Assignment"] + r'_*.txt')
                   result,points,correctFound = assignmentResults(listOfStudentDataFiles)
                   submission["result"] = result
                   print("\n"+ "*** " + submission["Assignment"] + " P" + submission["classPeriod"] + " (" + result + ") *** " + submission["FileName"] + ") " + submission["submissionDateTime"] + " [" + str(submission["timeout"]) + "sec]")
                   if doItAgain:
                      doitAgain = False
                   else:
                      copyFilesToProgramRunDirectory(submission, classRootDir)  ### copy files to student program run directory ###
                   checked = checkProgram(submission, classRootDir)   ### check the program ###
                   goodToRun = True
                   if not checked:
                     response = input("  Check failed. Run program anyways (y)? ")
                     if response != 'y':
                        goodToRun = False
                   if goodToRun:
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
                          answer = input("  y/n/p [s d a b h i o g e c m f l ls k w ?](r){x}" + str(len(currentSubmissions)-1) + "? ")
                       elif submission["studentName"] == "TestTest":
                         print("   *** THIS WAS JUST A TEST RUN ***")
                         response = input("  Confirm removing of file submission & student directory (y)? ")
                         if response == "y":
                             os.remove(submission["FileName"])  # remove submitted file
                             print("  " + submission["FileName"] + " was removed")                       
                             if os.path.isdir(submission["studentDir"]):
                               rmtree(submission["studentDir"]) # remove student directory 
                         break
                       else:
                           answer = input("  Invalid submission [s rn e c m l ll k](r){x}? ")
                       if answer == "y":  # submission correct. UPDATE scoreboard, CONTINUE to next submission.
                           submissionCorrect(submission)
                           killProcesses(submission)
                           break
                       elif answer == "n":  # submission incorrect. UPDATE scoreboard, CONTINUE to next submission.
                           submissionIncorrect(submission)
                           killProcesses(submission)
                           break
                       elif answer == "p":   # submission incorrect (presentation error). UPDATE scoreboard, CONTINUE to next submission.
                           submissionIncorrect(submission,"presentationError")
                           killProcesses(submission)
                           break                          
                       elif answer == "s":  # show program in IDE
                           ideCmds = generateIdeCommands(submission)
                           for ideCmd in ideCmds:
                              process = subprocess.Popen(ideCmd, shell=True)
                              time.sleep(0.5)
                              submission["processes"].append(process)
                       elif answer == "d":
                           diffCmd = [diffPgm,os.path.join(submission["studentPgmRunDir"],submission["outputFile"]),os.path.join(submission["goldenAssignmentDir"], "gold.txt")]
                           process = subprocess.Popen(diffCmd, shell=True)     # run diff program
                           submission["processes"].append(process)
                       elif answer == "a":  # run program again                     
                           doItAgain = True
                           break
                       elif answer == "b":  # bring up file explorer of scoreboard directory
                           process = subprocess.Popen('explorer "' + scoreboardDir + '\withNames"',creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
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
                       elif answer == "l" or answer == 'll':  # log, show the last lines of global (l) or local (ll) log file
                           if answer == "l":
                              logfile2Show = os.path.join(rootDir,"logGlobal.txt")
                           else:
                              logfile2Show = os.path.join(submission["studentDir"],"log.txt")
                           textEditorCmd = [textEditor,"-n1000000",logfile2Show]      
                           process = subprocess.Popen(textEditorCmd, shell=True)
                           submission["processes"].append(process)
                       elif answer == "r":  # remove submitted file and CONTINUE to next submission
                         response = input("  Confirm remove (y)? ")
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
                              subject = "P"+ submission.get("classPeriod","???") + "StudentDrop (" + submission.get("Assignment","????") + ")"
                              pyperclip.copy(subject)
                              time.sleep(0.5)
                              pyperclip.copy(receiverEmailAddress)
                              print("  ready to paste (subject & email address)!!!")
                       elif answer == "x":  # exit program
                           print("exiting program")
                           sys.exit()
                       elif answer == "h":
                           webbrowser.open("https://github.com/rainerpm/CSAssignmentChecker#assignment-menu")
                       elif answer == "w":
                           setFileTimestampToNow(submission["FileName"])
                           break
                       else:
                           print("  not a valid answer!!!")

            elif not autoJudging:  # no current submissions (wait for new ones)
                currentSubmissions = getSubmissions(validFileExtensions)
                print("\nPERIOD *",classPeriod,"* waiting for new submissions (<Ctrl-C> back to main menu) ", end="",flush=True)
                interrupted = False
                while len(currentSubmissions) == 0:  # wait for more submissions
                    print(".", end="",flush=True)
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
                            scoreboard.updateScoreboard(scoreboardDir,aGroupDir,aGroupId,classPeriod,listOfAssignments)
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
