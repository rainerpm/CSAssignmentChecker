import scoreboard  # import the associated scoreboard.py which creates the scoreboard files
from scoreboard import assignmentResults    
from login import emailSendFromAddress, emailSendFromPassword
from customize import validClassPeriods,rootDir,scoreboardDir,scoreboardDirAlt,pythonIdeLoc,javaIdeLoc,diffLoc,textEditorLoc,emailSignature,emailAttachmentFile

# import standard python libraries (might need to be installed on your computer using 'pip install')
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

validFileExtensions = [".py",".java",".zip","registerMe.txt"]  # .py for python, .java/.zip for java

# Check variables set in customize.py
initError = False

if not os.path.exists(os.path.join(rootDir)):
    initError = True
    print("ERROR!!! root directory does not exist (" + rootDir + ")")
else:
    if not os.path.exists(os.path.join(rootDir,"ASSIGNMENT_GROUPS")):
        initError = True
        print("ERROR!!! ASSIGNMENT_GROUPS directory does not exist in " + rootDir)

if not os.path.exists(os.path.join(scoreboardDir)):
    if os.path.exists(os.path.join(scoreboardDirAlt)):
        scoreboardDir = scoreboardDirAlt
    else:
        initError = True
        print("ERROR!!! scoreboard directory does not exist (" + scoreboardDir + ")")

if not os.path.exists(os.path.join(pythonIdeLoc)):
    initError = True
    print("ERROR!!! Python IDE not found @ " + pythonIdeLoc)

if not os.path.exists(os.path.join(javaIdeLoc)):
    initError = True
    print("ERROR!!! JAVA IDE not found @ " + javaIdeLoc)

if not os.path.exists(os.path.join(textEditorLoc)):
    initError = True
    print("ERROR!!! TextEditor not found @ " + textEditorLoc)

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
    listOfDirectoriesInRootDir = [f.name for f in os.scandir(rootDir) if f.is_dir()]  # https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
    for classPeriod in listOfDirectoriesInRootDir:
        files = []
        if classPeriod in validClassPeriods:
            print("Class Period",classPeriod)
            for extension in validFileExtensions:
                files = files + glob.glob(os.path.join(rootDir,classPeriod,r"*"+extension))
            if files:
                files.sort(key=os.path.getmtime)
                for file in files:
                    fname = Path(file)
                    print(" ", datetime.fromtimestamp(fname.stat().st_mtime).strftime("%b%d %Hh%Mm"), os.path.basename(file))

# return a dictionary of all registered students and create student directory
# if it does not yet exist
def loadRegisteredStudents(assignmentGroups):
    classRegistration = {}
    if os.path.isfile("REGISTER.txt"):
        with open("REGISTER.txt", "r") as freg:
            for line in freg:
                line = line.rstrip()
                if not line:
                    continue
                fields = line.split()
                if len(fields) < 4:  # if registration does not have email yet
                    code, name, classPeriod = fields
                    email = ""
                else:
                    code, name, classPeriod, email = fields
                classRegistration[code] = (name, classPeriod, email)
                # check if the student directory for each registered student exists in every assignment group of the class
                aKeys = list(assignmentGroups.keys())
                aKeys.sort()
                for aGroupId in aKeys:
                    aDict = assignmentGroups[aGroupId]
                    aGroupDir = aDict["assignmentGroupDir"]
                    studentDir = os.path.join(aGroupDir,name + "_" + code)
                    if not os.path.isdir(studentDir):
                        os.mkdir(studentDir)
                        print("  Created student dir", studentDir)
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
           print("Did not find file period.txt in",globalAssignmentGroupDir)
        for classPeriod in classPeriods:
            classPeriodsDir = os.path.join(rootDir,classPeriod)
            if not os.path.isdir(classPeriodsDir):
                os.mkdir(classPeriodsDir)
                print("Created directory",classPeriodsDir)
            classAssignmentGroupDir = os.path.join(rootDir,classPeriod,globalAssignmentGroupDirOnly)
            if not os.path.isdir(classAssignmentGroupDir):
                os.mkdir(classAssignmentGroupDir)
                print("Created directory",classAssignmentGroupDir)
            latestResultsDir = os.path.join(rootDir,classPeriod,"latestResults")
            if not os.path.isdir(latestResultsDir):
                os.mkdir(latestResultsDir)
                print("Created directory",latestResultsDir)
            saveDir = os.path.join(classAssignmentGroupDir,"00SAVE")
            if not os.path.isdir(saveDir):
                os.mkdir(saveDir)
                print("Created directory",saveDir)
            plagiarismDir = os.path.join(classAssignmentGroupDir,"00PLAGIARISM")
            if not os.path.isdir(plagiarismDir):
                os.mkdir(plagiarismDir)
                print("Created directory",plagiarismDir)
            assignmentGroup = {}  # create content dict, then add to it
            assignmentGroup["assignmentGroupDir"] = classAssignmentGroupDir
            assignmentGroup["goldenDir"] = globalAssignmentGroupDir   # this is in the GLOBAL assignment group directory
            assignmentGroup["saveDir"] = saveDir
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

def emailStudent(submission, classRegistration):
    receiverEmailAddress = ""
    if "studentCode" in submission and submission["studentCode"] in classRegistration:
        if len(classRegistration[submission["studentCode"]]) > 2:  # email address was manually added to REGISTER.txt
            receiverEmailAddress = classRegistration[submission["studentCode"]][2]
    if not receiverEmailAddress:  # student is in classRegistration dictionary but email is blank OR student is not in dictionary
        receiverEmailAddress = input("  enter student's email address -> ")
    if "Assignment" in submission:
        subject = "P"+ submission["classPeriod"] + "StudentDrop (" + submission["Assignment"] + ")"
    else:
        subject = "StudentDrop Error"
    print("  Preparing to send", subject, "email to", receiverEmailAddress)
    comment = commentFromFile(submission)
    response = ""
    if comment:
        response = input("  attach image from clipboard (y)? ")
    attachment = ""
    if response == "y":
        while True:
           image = ImageGrab.grabclipboard()
           if image == None:
             print("No image found on top of clipboard.")
             response = input("<enter> to try again or <q>uit trying? ")
             if response == 'q':
                break
           else:
              break
        imageJpg = image.convert('RGB')
        imageJpg.save(emailAttachmentFile,'JPEG')
        attachment = emailAttachmentFile
        comment = comment + "\nBe sure to look at the e-mail attachment."
    updateLogFile(submission, "  email msg -> " + comment)
    message = comment + emailSignature
    print("SENDING EMAIL")
    emailWithOutlook(emailSendFromAddress,emailSendFromPassword,receiverEmailAddress,subject,message,attachment)
    #emailWithGmail("lasacsAutomated@gmail.com", "lasa{cs}ozarka", "rainer.mueller@austinisd.org", "test", "test message")
    print("SENT EMAIL")

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
    try:
        server = smtplib.SMTP("smtp.office365.com", 587)
        response = server.ehlo()
        response = server.starttls()
        response = server.login(email_sender, email_password)
        text = msg.as_string()
        server.sendmail(email_sender, email_recipient, text)
        server.quit()
    except:
        print("SMPT server connection error")
    return True

def commentFromFile(submission):
   askQuestion = True
   matchResponse = False
   commentsFile = ""
   while askQuestion:
      askQuestion = False
      while not matchResponse:
         response = input("  Comment (g[#], l[#], o=one-time comment, n=no comment)? ")
         if matchResponse := re.match('([glon])(\d*)',response):
            commentTypeResponse = matchResponse.group(1)
            commentNumResponse  = matchResponse.group(2)
      if commentTypeResponse == 'g':
         commentsFile = os.path.join(rootDir,"ASSIGNMENT_GROUPS","comments"+submission["language"].upper()+".txt")
      elif commentTypeResponse == 'l':
         commentsFile = os.path.join(submission["goldenAssignmentDir"],"comments.txt")
      if commentTypeResponse == 'g' or commentTypeResponse == 'l':
         if not commentNumResponse:
            askQuestion = True
            matchResponse = False
            txtEditorCmd = [textEditorLoc,commentsFile]      
            result = subprocess.run(txtEditorCmd, shell=True)
         else:
            print("    retrieving comment",commentNumResponse,"from",commentsFile)
            commentsDict = {}
            firstComment = True
            comment = ''
            commentNum = 0
            commentCount = 1
            with open(commentsFile) as cFile:
               for line in cFile:
                  if matchResponse := re.match('comment (\d+)',line):
                     commentNumPrev = commentNum
                     commentNum = matchResponse.group(1)
                     if firstComment:
                        firstComment = False
                     else:
                        commentsDict[commentNumPrev] = comment
                        comment = ''
                        commentCount += 1
                  else:
                     if line.strip() != "":    # left strip non empty lines
                        line = line.lstrip()
                     comment = comment + line
               commentsDict[commentNum] = comment  # put last comment from file into dictionary
            if commentNumResponse in commentsDict:
               comment = commentsDict[commentNumResponse]
            else:
               print("    comment",commentNumResponse,"was not found.")
               askQuestion = True
               matchResponse = False               
      elif commentTypeResponse == 'o':
         comment = input("    enter a online, one-time comment that will not be saved for next time (use \\n if you want a newline) \n    -> ").replace(r'\n', '\n')
      elif commentTypeResponse == 'n':
         comment = ""
   return comment

def checkErrorFileForErrors(errFile, errorType):
    errorFileSize = Path(errFile).stat().st_size
    if errorFileSize != 0:  # had errors
        if not autoJudging:
            response = input(errorType + "!!!  Print error file (y)? ")
            if response == "y":
                with open(errFile) as javaErrFile:
                    lines = javaErrFile.readlines()
                    for line in lines[: min(12, len(lines))]:
                        print(line.rstrip())
                    if len(lines) > 12:
                        print("     ^^^ first 12 ^^^        vvv last 4 vvv")
                        for line in lines[-min(4, len(lines)) :]:
                            print(line.rstrip())
        return True
    return False

def checkStudentRegistration(fname,name,code,classRegistration):
   foundNameInRegistration = True
   if name != "TestTest":
      if (code not in classRegistration):
         print("  Code >" + code + "< is not registered " + "(" + fname +")") 
         foundNameInRegistration = False
      elif classRegistration[code][0] != name:
         print("  Name mismatch!!! >" + code + "< code registered as",classRegistration[code][0],"and not",name)
         foundNameInRegistration = False
   return foundNameInRegistration

def processFileName(fname):
   nameLast = nameFirst = code = nameLastPartner = nameFirstPartner = codePartner = assignment = ""
   # One Person Submission:   LastName FirstName Code - assignmentName.ext
   match1 = re.search("^([-\w]+) ([-\w]+) (\d+) - (\w+)\.(\w+)$",fname)
   if match1:
      nameLast = match1.group(1).strip()
      nameFirst = match1.group(2).strip()
      code = match1.group(3).strip()
      namePartner = ""
      codePartner = ""
      assignment = match1.group(4).strip()

   # Pair Programming Submission:  LastName LastNamePartner FirstName FirstNamePartner Code CodePartner - assignmentName.ext
   match2 = re.search("^(\w+) (\w+) (\w+) (\w+) (\d+) (\d+) - (\w+)\.(\w+)$",fname)
   if match2:
      nameLast = match2.group(1).strip()
      nameFirst = match2.group(3).strip()
      code = match2.group(5).strip()
      nameLastPartner = match2.group(2).strip()
      nameFirstPartner = match2.group(4).strip()
      codePartner = match2.group(6).strip()
      assignment = match2.group(7).strip()

   valid = match1 or match2

   return valid,nameLast,nameFirst,nameLastPartner,nameFirstPartner,code,codePartner,assignment
   

def processCurrentSubmission(currentSubmission, assignmentGroups, assignments,classRootDir,classRegistration):
   submission = {}
   submission["classPeriod"] = os.path.basename(os.getcwd())
   submission["FileName"] = currentSubmission
   submission["submissionDateTime"] = datetime.fromtimestamp(Path(submission["FileName"]).stat().st_mtime).strftime("%b_%d_%Hh%Mm%Ss")
   # check submission
   validFileName, nameLast, nameFirst, nameLastPartner, nameFirstPartner, code, codePartner, assignment = processFileName(submission["FileName"])
   name = nameLast + nameFirst
   submission["Assignment"]  = assignment.strip()
   submission["registration"] = submission["Assignment"] == "registerMe"  # student submitted a registration request
   submission["studentName"] = name.strip()
   submission["studentFirstNameL"] = nameFirst + nameLast[0]   # RPM this also needs to exist for the partner somewhere
   submission["studentCode"] = code.strip()
   namePartner = nameLastPartner + nameFirstPartner   # will be an empty string if this is not a pair programming submission
   submission["hasPartner"] = (namePartner != "")
   submission["partnerName"] = namePartner.strip() 
   submission["partnerCode"] = codePartner.strip()
   submission["valid"] = False
   
   if submission["registration"]:   
      classRegistration = loadRegisteredStudents(assignmentGroups)
      if submission["studentCode"] in classRegistration:
          print(submission["studentCode"], "is already registered")
          print("  current submission   ", submission["FileName"])
          print("  previous registration", classRegistration[submission["studentCode"]])
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
                    print("  student code in file (" + registrationCode + ") does not match one in submission (" + submission["studentCode"] + ")")
                 # classRegistration[submission["studentCode"]] = (submission["studentName"],submission["classPeriod"])
                 # updateLogFile(submission,"registered " + submission["studentCode"] + " " + submission["studentName"] + " " + submission["classPeriod"],True)
              else:
                 print("  Registration code and email not found on first two lines of " + submission["FileName"])
      os.remove(submission["FileName"])  # remove registration file (assignment name was register, file has served its purpose)
   else:   
      studentRegistered = checkStudentRegistration(submission["FileName"],submission["studentName"],submission["studentCode"],classRegistration)
      partnerRegistered = True    
      if namePartner:
         partnerRegistered = checkStudentRegistration(submission["FileName"],submission["partnerName"],submission["partnerCode"],classRegistration)
      submission["fileNameFormatValid"] = validFileName and (studentRegistered and partnerRegistered)
      if submission["fileNameFormatValid"]:     
         submission["validAssignment"] = submission["Assignment"] in assignments
         submission["assignmentGroupValid"] = True
         if not submission["validAssignment"]:
            print("  Invalid Assignment Name: >"+submission["Assignment"]+"<")
         else:
            submission["assignmentGroupId"] = assignments[submission["Assignment"]]  # assignment group assignment belongs to
            assignmentGroup = assignmentGroups[submission["assignmentGroupId"]]  # dictionary with info for this assignment group
            submission["saveDir"] = assignmentGroup["saveDir"]
            submission["listOfAssignments"] = assignmentGroup["listOfAssignments"]
            submission["assignmentGroupValid"] = submission["Assignment"] in submission["listOfAssignments"]
            if not submission["assignmentGroupValid"]:
               print("  Assignment >"+submission["Assignment"]+"< is not in group "+submission["listOfAssignments"])     
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
         # caps = []
         # caps = [idx for idx in range(len(name)) if name[idx].isupper()]  # indexes of all uppercase characters

         submission["outFileName"] = submission["Assignment"] + "_out.txt"
         submission["outCheckFileName"] = submission["Assignment"] + "_check.txt"
         submission["outCorrectFileName"] = submission["Assignment"] + "_" + submission["submissionDateTime"] + "_out_CORRECT.txt"
         submission["outLongFileName"] = submission["Assignment"] + "_" + submission["submissionDateTime"] + "_out.txt"
         submission["compileErrFileName"] = submission["Assignment"] + "_" + submission["submissionDateTime"] + "_compileErr.txt"
         submission["runErrFileName"] = submission["Assignment"] + "_" + submission["submissionDateTime"] + "_runErr.txt"
         submission["errorFileName"] = submission["Assignment"] + "_err.txt"

      if submission["fileNameFormatValid"] and submission["validAssignment"] and submission["assignmentGroupValid"]:
         submission["valid"] = True
         # directories
         submission["classDir"] = classRootDir;
         submission["assignmentGroupDir"] = assignmentGroup["assignmentGroupDir"]
         submission["goldenDir"] = assignmentGroup["goldenDir"]
         submission["goldenAssignmentDir"] = os.path.join(assignmentGroup["goldenDir"], submission["Assignment"])
         submission["goldFile"] = os.path.join(submission["goldenAssignmentDir"], "gold.txt")
         submission["goldCheckFile"] = os.path.join(submission["goldenAssignmentDir"], "checker.txt")
         submission["dataInputFileExists"] = os.path.exists(os.path.join(submission["goldenAssignmentDir"],submission["Assignment"]+".dat"))
         submission["dataInputFileName"] = os.path.join(submission["goldenAssignmentDir"],submission["Assignment"]+".dat")
         submission["plagiarismAssignmentDir"] = os.path.join(assignmentGroup["plagiarismDir"],submission["Assignment"])
         ## FIX Creating a plagiarism directory for each assignment should be done when setting up the class
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
         submission["outputFile"] = os.path.join(submission["studentPgmRunDir"],submission["outFileName"])
         if not os.path.isdir(submission["studentPgmRunDir"]):
           os.mkdir(submission["studentPgmRunDir"])
         if submission["hasPartner"]:
           submission["partnerDir"] = os.path.join(submission["assignmentGroupDir"],submission["partnerName"] + "_" + submission["partnerCode"])
           if not os.path.isdir(submission["partnerDir"]):
               os.mkdir(submission["partnerDir"])
      else:
         updateLogFile(submission, "  File submission error (" + submission["FileName"] + ")",True)
         pyperclip.copy(submission["FileName"])
         time.sleep(0.5)
         response = input("  New name (clipboard) or remove submission (r)? ")
         if response == 'r':
            response = input("  Save in directory" + submission["saveDir"] + " before removing (y)? ")
            if response == "y":
              os.replace(os.path.join(classRootDir,submission["FileName"]),os.path.join(submission["saveDir"],submission["FileName"]))  # move (replace if already there) pgm to 00SAVE directory
            os.remove(submission["FileName"])
            updateLogFile(submission, "  removed "  + os.path.join(classRootDir,submission["FileName"]),True)
         else:
            os.rename(submission["FileName"], response)  # rename to new name
            submission = processCurrentSubmission(response, assignmentGroups, assignments,classRootDir,classRegistration)
         
   return submission

def copyFilesToProgramRunDirectory(submission, classRootDir):
    goldenAssignmentDir = submission["goldenAssignmentDir"]
    pgmRunDir = submission["studentPgmRunDir"] 
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
    goldenDirFiles = os.listdir(goldenAssignmentDir)
    for goldenDirFile in goldenDirFiles:
        if goldenDirFile != "gold.txt" or goldenDirFile != "checker.txt":
            fullGoldenDirFile = os.path.join(goldenAssignmentDir, goldenDirFile)
            if os.path.isfile(fullGoldenDirFile):
                copy(fullGoldenDirFile, pgmRunDir)
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
           with open("CompilerError.txt", "w") as ferr:
               result = subprocess.run(compileCmd, stdout=fout, stderr=ferr)  #COMPILE CHECKER
       runCmd = ["java", submission["Assignment"] + "Checker"]
       with open(submission["outCheckFileName"], 'w') as fout:
          result = subprocess.run(runCmd, stdin=None, stdout=fout, stderr=None)   # run Checker
       checkFilesMatches = filesMatch(submission["outCheckFileName"],submission["goldCheckFile"])
       if checkFilesMatches:
           print("  >>> CHECK CORRECT <<<")
       else:
           diffCmd = [diffLoc,submission["outCheckFileName"],submission["goldCheckFile"]]
           result = subprocess.run(diffCmd, shell=True)     # run diff program                      
           checked = False
    os.chdir(classRootDir)
    return checked

def runProgram(submission, classRootDir):
    correct = False
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
            runCmds.append(["java",submission["assignmentFileName"].rstrip(".java")]);
    else:
        print("ERROR!!! Unsupported language")
        sys.exit()
    # language independant code
    with open("CompilerOutput.txt", "w") as fout:
        with open("CompilerError.txt", "w") as ferr:
            result = subprocess.run(compileCmd, stdout=fout, stderr=ferr)  #COMPILE PROGRAM
    errorCompile = checkErrorFileForErrors("CompilerError.txt", "  COMPILE ERROR")
    bringUpIDEorDataFile = '\nset /P c=Bring up IDE [y]? \nif /I "%c%" EQU "Y" goto :ide\ngoto :next\n:ide\n' + bringUpProgramInIDE(submission,False) + '\n:next'
    latestResultsDir = os.path.join(classRootDir,"latestResults")
    if submission["dataInputFileExists"]:
        bringUpIDEorDataFile += '\nset /P c=Bring up input data file [y]? \nif /I "%c%" EQU "Y" goto :idf\ngoto :end\n:idf\n' + '"' + textEditorLoc + '"' + " -multiInst -nosession " + '"' + submission["dataInputFileName"] + '"' + '\n:end'
    if errorCompile:
        copyfile("CompilerError.txt", os.path.join(latestResultsDir,submission["studentFirstNameL"] + "_compileError.txt"))  # copy compile error file to class directory
        copyfile("CompilerError.txt", os.path.join(submission["studentDir"],submission["compileErrFileName"]))  # copy output file to data directory
        if submission["hasPartner"]:
            copyfile("CompilerError.txt",os.path.join(submission["partnerDir"],submission["compileErrFileName"]))  # copy output file to partner's data directory
        updateLogFile(submission, "  ERROR!!! " + submission["FileName"] + " had a compile time error.",False)
    else:
        if os.path.exists(os.path.join(latestResultsDir,submission["studentFirstNameL"] + "_compileError.txt")):
            os.remove(os.path.join(latestResultsDir,submission["studentFirstNameL"] + "_compileError.txt"))
        writeOrAppend = "w"
        for runCmd in runCmds:
            runStdin = None
            if not runCmd[1].endswith("Tester"):
               if runCmd[1].endswith("Runner"):
                  inputFileList = glob.glob(r"runnerUserInput*.txt")
               else:
                  inputFileList = glob.glob(r"pgmUserInput*.txt")
               if len(inputFileList) > 0:
                  for inputFile in inputFileList:
                     runStdin = open(inputFile)
                     with open(submission["outFileName"], writeOrAppend) as fout:
                         with open(submission["errorFileName"], writeOrAppend) as ferr:
                            #fout.write("\n" + runCmd[1] + " stdin=" + inputFile +"\n")
                            fout.write("\nstdin=" + inputFile +"\n")
                            fout.flush()
                            result = subprocess.run(runCmd, stdin=runStdin, stdout=fout, stderr=ferr)   # run submitted RUNNER or student program with a user input file (i.e. program reads from stdin)
                            writeOrAppend = "a"
                     runStdin.close()
               else:
                  with open(submission["outFileName"], writeOrAppend) as fout:
                      with open(submission["errorFileName"], writeOrAppend) as ferr:
                           result = subprocess.run(runCmd, stdin=runStdin, stdout=fout, stderr=ferr)   # run submitted RUNNER or student program without a user input file      
                           writeOrAppend = "a"
            else:
               with open(submission["outFileName"], writeOrAppend) as fout:
                   with open(submission["errorFileName"], writeOrAppend) as ferr: 
                      result = subprocess.run(runCmd, stdin=runStdin, stdout=fout, stderr=ferr)   # run Tester
                      writeOrAppend = "a"
        errorRun = checkErrorFileForErrors(submission["errorFileName"], "  RUNTIME ERROR")
        if errorRun:
            if os.path.exists(submission["outFileName"]):
                os.remove(submission["outFileName"])
            if os.path.exists(os.path.join(latestResultsDir,submission["studentFirstNameL"] + ".bat")):
                os.remove(os.path.join(latestResultsDir,submission["studentFirstNameL"] + ".bat"))
            with open(os.path.join(latestResultsDir,submission["studentFirstNameL"] + ".bat"), "w") as fbatch:
                fbatch.write('"' + textEditorLoc + '"' + " -multiInst -nosession " + '"' + os.path.join(submission["studentDir"],submission["runErrFileName"]) + '"')
                fbatch.write(bringUpIDEorDataFile)
            copyfile(submission["errorFileName"], os.path.join(latestResultsDir,submission["studentFirstNameL"] + "_runTimeError.txt"))  # copy compile error file to class directory
            copyfile(submission["errorFileName"], os.path.join(submission["studentDir"],submission["runErrFileName"]))  # copy output file to data directory
            if submission["hasPartner"]:
                copyfile(submission["errorFileName"],os.path.join(submission["partnerDir"],submission["runErrFileName"]))  # copy output file to partner's data directory
            updateLogFile(submission, "  ERROR!!! " + submission["FileName"] + " had a run time error.",False)
        else:
            if os.path.exists(os.path.join(latestResultsDir,submission["studentFirstNameL"] + "_runTimeError.txt")):
                os.remove(os.path.join(latestResultsDir,submission["studentFirstNameL"] + "_runTimeError.txt"))
    error = errorCompile or errorRun
    if not error:
        goldFileMatches = filesMatch(submission["outputFile"],submission["goldFile"])
        if goldFileMatches:
            print("  *** RUN CORRECT ***")
        else:
            if autoJudging:
                print("  INCORRECT (autojudged)")
            else:
                diffCmd = [diffLoc,submission["outputFile"],submission["goldFile"]]
                result = subprocess.run(diffCmd, shell=True)     # run diff program
            with open(os.path.join(submission["studentPgmRunDir"], "diff.bat"), "w") as fdiff:
                fdiff.write('"' + diffLoc + '"' + " " + submission["outFileName"] + " " + os.path.join(submission["goldenAssignmentDir"], "gold.txt"))
            # also write diff batch file to class directory (for quick access to each student's last run results)
            if os.path.exists(os.path.join(latestResultsDir,submission["studentFirstNameL"] + ".bat")):
                os.remove(os.path.join(latestResultsDir,submission["studentFirstNameL"] + ".bat"))
            with open(os.path.join(latestResultsDir,submission["studentFirstNameL"] + ".bat"), "w") as fbatch:
                fbatch.write('"' + diffLoc + '"' + " " + os.path.join(submission["studentPgmRunDir"],submission["outFileName"]) + " " + os.path.join(submission["goldenAssignmentDir"], "gold.txt"))
                fbatch.write(bringUpIDEorDataFile)
    os.chdir(classRootDir)
    return correct

def getSubmissions(extensions):
    listOfSubmissions = []
    for extension in extensions:
        listOfSubmissions = listOfSubmissions + glob.glob(r"*" + extension)
    return listOfSubmissions

def updateLogFile(submission, logMessage, alsoPrint = False):
    if alsoPrint:
        print(logMessage)
    # global log file in rootDir
    with open(os.path.join(rootDir,"logGlobal.txt"), "a") as fglog:
        fglog.write(submission["submissionDateTime"] + ' ' + submission["FileName"] + ' ' + logMessage + "\n")
    # assignment log file in classRootDir
    if "assignmentGroupDir" in submission:
        with open(os.path.join(submission["assignmentGroupDir"],"logAssignment.txt"), "a") as falog:
            falog.write(submission["submissionDateTime"] + ' ' + submission["FileName"] + ' ' + logMessage + "\n")
    # student log file in student directory
    if "studentDir" in submission:  # "studentDir" will not be in dictionary for an invalid/unknown assignment name
        with open(os.path.join(submission["studentDir"],"log.txt"), "a") as fslog:
            fslog.write(submission["submissionDateTime"] + ' ' + submission["FileName"] + ' ' + logMessage + "\n")

def gradeSubmission(submission):
    gradeFileName = os.path.join(submission["studentAssignmentDir"],"grades.txt")
    if os.path.exists(gradeFileName): 
        with open(gradeFileName) as gradeFile:
            for line in gradeFile:
                print("  " + line.rstrip())
    grade = input("  enter Grade ")
    note  = input("  enter Note  ")
    with open(gradeFileName, "a") as gradeFile:
        line2write = f'{grade.strip():<5s}' + " : " + submission["submissionDateTime"] + " : " + note.strip() + "\n"
        gradeFile.write(line2write)

def submissionCorrect(submission):
    if not os.path.exists(os.path.join(submission["plagiarismAssignmentDir"],submission["submittedFileNameWithDate"])):
       os.rename(submission["FileName"], os.path.join(submission["plagiarismAssignmentDir"],submission["submittedFileNameWithDate"]))  # move pgm to PLAGIARISM directory
    else:
        os.remove(submission["FileName"])       # remove submission file (this only happens if the same file with the same time stamp is copied into class directory)
    copyfile(os.path.join(submission["studentPgmRunDir"],submission["outFileName"]), os.path.join(submission["studentDir"],submission["outCorrectFileName"]))  # copy output file to data directory
    if submission["hasPartner"]:
        copyfile(os.path.join(submission["studentPgmRunDir"],submission["outFileName"]), os.path.join(submission["partnerDir"],submission["outCorrectFileName"]))  # copy output file to partner's data directory
    scoreboard.updateScoreboard(scoreboardDir,submission["assignmentGroupDir"],submission["assignmentGroupId"],submission["classPeriod"],submission["listOfAssignments"])
    updateLogFile(submission, "  *** CORRECT *** ")

def submissionIncorrect(submission):
    if submission["valid"]:
        if os.path.exists(os.path.join(submission["studentPgmRunDir"],submission["outFileName"])):
            copyfile(os.path.join(submission["studentPgmRunDir"],submission["outFileName"]),os.path.join(submission["studentDir"],submission["outLongFileName"]))  # copy output file to data directory
            if submission["hasPartner"]:
                copyfile(os.path.join(submission["studentPgmRunDir"],submission["outFileName"]),os.path.join(submission["partnerDir"],submission["outLongFileName"]))  # copy output file to partner's data directory
        scoreboard.updateScoreboard(scoreboardDir,submission["assignmentGroupDir"],submission["assignmentGroupId"],submission["classPeriod"],submission["listOfAssignments"])
        updateLogFile(submission, "  >>> INCORRECT <<< ")
    else:
        updateLogFile(submission, "  >>> INVALID SUBMISSION <<< ")
    os.remove(submission["FileName"])

def bringUpProgramInIDE(submission, run=True):
    global pythonIdeLoc,palreadyythonIdeCmd,javaIdeLoc,javaIdeCmd
    ideCmd = ['none','none']
    if submission["language"] == "python":
        if os.path.exists(pythonIdeLoc):
            ideCmd = [pythonIdeLoc,os.path.join(submission["studentPgmRunDir"],submission["FileName"])]
        else:
            print("Error!!! Did not find IDE executable at " + pythonIdeLoc + "\nSet pythonIdeLoc variable in program to correct IDE location")
    elif submission["language"] == "java":
        if os.path.exists(javaIdeLoc):
            ideCmd = [javaIdeLoc,os.path.join(submission["studentPgmRunDir"],submission["Assignment"] + ".java")]
        else:
            print("Error!!! Did not find IDE executable at " + javaIdeLoc + "\nSet javaIdeLoc variable in program to correct IDE location")
    if run:
        result = subprocess.run(ideCmd, shell=True)
    ideCmdString = '"' + ideCmd[0] + '"' + ' ' + ideCmd[1]
    return ideCmdString

### MAIN PROGRAM ###
def main():
    global interrupted, autoJudging, autoJudgingPeriods, autoJudgingSleepTime

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
            response = input("\n" + "("+ validClassPeriodsString + ")manual (a)utojudge (l)og e(x)it (<ENTER>=check)? ")
            inputContinue = (response == 'x') or (response in validClassPeriods)
            if response in validClassPeriods:
                classPeriod = response
            elif response == "a":
                response2 = input("(" + validClassPeriodsString + ")autojudge (m)ultiple (<ENTER>=all periods)? ")
                autoJudging = True
                autoJudgingFirstTime = False
                if response2 in validClassPeriods:
                    classPeriod = response2
                    autoJudgingPeriods = [classPeriod]
                    autoJudgingSleepTime = 2
                elif response2 == "m":
                    response3 = input("Enter comma separated list of class periods (e.g. 1,4,5)? ")
                    autoJudgingPeriods = response3.split(",")
                    autoJudgingSleepTime = 2
                else:
                    autoJudgingPeriods = validClassPeriods
            elif response == "l":   # log
                with open(os.path.join(rootDir,"logGlobal.txt")) as logfile:
                    lines = logfile.readlines()
                    fromLine = -min((lCount+1)*20,len(lines))
                    if lCount > 0:
                        for line in lines[fromLine:-(lCount*20)]:
                            print(" ",line.rstrip())
                    else:
                        for line in lines[fromLine:]:
                            print(" ",line.rstrip())
                lCount += 1
            elif response == "x":
                sys.exit()

        if autoJudging:
            classPeriod = autoJudgingPeriods[0]
            print(classPeriod,end="")


        classRootDir = os.path.join(rootDir,classPeriod)  # CLASSROOTDIRassignment (directory for submissions)
        os.chdir(classRootDir)

        # initialize the dictionaries for the class
        assignmentGroups = allAssignmentGroups[classPeriod]
        assignments = allAssignments[classPeriod]
        # get dictionary of all registered students and create student directory
        classRegistration = loadRegisteredStudents(assignmentGroups)

        # check for files in 00SAVE directories
        for key in assignmentGroups:
            saveDir = assignmentGroups[key]["saveDir"]
            savedFiles = len([name for name in os.listdir(saveDir) if os.path.isfile(os.path.join(saveDir, name))])
            if savedFiles != 0:
                print(" ", savedFiles, "submissions found in /00SAVE for", key)

        while True:  # loop over each program, run the oldest first
            interrupted = False
            correct = False
            currentSubmissions = getSubmissions(validFileExtensions)
            if len(currentSubmissions) > 0:
                currentSubmission = min(currentSubmissions, key=os.path.getmtime)
                currentSubmissions.remove(currentSubmission)
                submission = processCurrentSubmission(currentSubmission, assignmentGroups, assignments,classRootDir,classRegistration)
                updateLogFile(submission,"\nRECEIVED " + submission["FileName"] + " (P" + submission["classPeriod"] + ")")
                if submission["valid"]:
                   ####################################### 
                   ### COPY, CHECK, and RUN THE PROGRAM
                   ####################################### 
                   listOfStudentDataFiles = glob.glob(submission["studentDir"] + '/' + submission["Assignment"] + r'_*.txt')
                   result,points,correctFound = assignmentResults(listOfStudentDataFiles)
                   print("\n"+ "*** " + submission["Assignment"] + " P" + submission["classPeriod"] + " (" + result + ") *** " + submission["FileName"] + ") " + submission["submissionDateTime"])
                   copyFilesToProgramRunDirectory(submission, classRootDir)  ### copy file to student program run directory ###
                   checked = checkProgram(submission, classRootDir)   ### check the program ###
                   goodToRun = True
                   if not checked:
                     response = input("Check failed. Run program anyways (y)? ")
                     if response != 'y':
                        goodToRun = False
                   if goodToRun:
                     correct = runProgram(submission, classRootDir)   ### run the program ###

                   lCount = 0
                   if autoJudging:
                       if correct:
                           submissionCorrect(submission)
                       else:
                           submissionIncorrect(submission)
                   while not autoJudging:    # loop until a valid response
                       if submission["studentName"] != "TestTest":
                          answer = input("  y/n [s d a h i o g e c m f l ls](r){x} h=help? ")
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
                           answer = input("  Invalid submission [s rn e c m l ls](r){x} h=help? ")
                       if answer == "y":  # submission correct. UPDATE scoreboard, CONTINUE to next submission.
                           submissionCorrect(submission)
                           break
                       elif answer == "n":  # submission incorrect. UPDATE scoreboard, CONTINUE to next submission.
                           submissionIncorrect(submission)
                           break
                       elif answer == "s":  # show program in IDE
                           bringUpProgramInIDE(submission)
                       elif answer == "d":
                           diffCmd = [diffLoc,os.path.join(submission["studentPgmRunDir"],submission["outputFile"]),os.path.join(submission["goldenAssignmentDir"], "gold.txt")]
                           result = subprocess.run(diffCmd, shell=True)     # run diff program
                       elif answer == "a":  # run program again
                           runProgram(submission, classRootDir)
                       elif answer == "h":
                           listOfStudentDataFiles = glob.glob(submission["studentDir"] + '/' + submission["Assignment"] + r'_*.txt')
                           if len(listOfStudentDataFiles) == 0:
                              print("  This is the first submission.")
                           else:
                              listOfStudentDataFilesSorted = sorted(listOfStudentDataFiles,key = os.path.getmtime, reverse=True)
                              for studentDataFile in listOfStudentDataFilesSorted:
                                 print("  ",studentDataFile)
                       elif answer == "i":
                           if submission["dataInputFileExists"]:
                              infile = os.path.join(submission["studentPgmRunDir"],submission["dataInputFileName"])
                              with open(infile,'r') as inf:
                                  for line in inf:
                                      line = line.replace("\n","↵")
                                      print(line)
                           else:
                              if "dataInputFile" in submission:
                                 print("  Assignment does not have a data input file named")
                                 print("  " + submission["dataInputFile"])
                              else:
                                 print("  Assignment does not have a data input file")
                       elif answer == "o":   # print program output (making newline character visible)
                           outfile = os.path.join(submission["studentPgmRunDir"],submission["outFileName"])
                           with open(outfile,'r') as outf:
                               for line in outf:
                                   line = line.replace("\n","↵")
                                   print(line)
                       elif answer == "g":
                           gradeSubmission(submission)
                       elif answer == "e":  # email student
                           emailStudent(submission, classRegistration)
                       elif answer == "m":  # move submission to 00SAVE directory
                           os.rename(os.path.join(classRootDir,submission["FileName"]),os.path.join(submission["saveDir"],submission["FileName"]))  # copy (replace if already there) pgm to 00SAVE directory
                           updateLogFile(submission, "  copied to " + os.path.join(submission["saveDir"],submission["FileName"]),True)
                           break
                       elif answer == "f":  # files (show files in student directory)
                           print("    " + submission["studentPgmRunDir"])
                           # print("    " + '/'.join(submission["studentPgmRunDir"].split('/')[-3:]))   # print the last 3 folders in path
                           for file in glob.glob(os.path.join(submission["studentPgmRunDir"],"*")):
                               print("    " + os.path.basename(file))
                       elif answer == "l" or answer == 'ls':  # log, show the last lines of global log file (chosing l again will get the next earlier set of lines)
                           if answer == "l":
                              logfile2Show = os.path.join(rootDir,"logGlobal.txt")
                           else:
                              logfile2Show = os.path.join(submission["studentDir"],"log.txt")
                           with open(logfile2Show) as logfile:
                               lines = logfile.readlines()
                               fromLine = -min((lCount+1)*20,len(lines))
                               if lCount > 0:
                                   for line in lines[fromLine:-(lCount*20)]:
                                       print(line.rstrip())
                               else:
                                   for line in lines[fromLine:]:
                                       print(line.rstrip())
                           lCount += 1
                       elif answer == "r":  # remove submitted file and CONTINUE to next submission
                          response = input("  Save in directory" + submission["saveDir"] + " before removing (y)? ")
                          if response == "y":
                             os.replace(os.path.join(classRootDir,submission["FileName"]),os.path.join(submission["saveDir"],submission["FileName"]))  # move (replace if already there) pgm to 00SAVE directory
                          response = input("  Confirm remove (y)? ")
                          if response == "y":
                             os.remove(submission["FileName"])  # remove submitted
                             print("  " + submission["FileName"] + "was removed")
                          updateLogFile(submission, "  removed "  + os.path.join(classRootDir,submission["FileName"]),True)
                          break
                       elif answer == "c":  # clipboard (put email, subject, in Windows-10 clipboard)
                           comment = commentFromFile(submission)
                           if comment:
                               pyperclip.copy(comment)
                               time.sleep(0.5)
                           if "studentCode" in submission and submission.get("studentCode","NA") in classRegistration:
                               if len(classRegistration[submission["studentCode"]]) > 2:  # email address was manually added to REGISTER.txt
                                   receiverEmailAddress = classRegistration[submission["studentCode"]][2]
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
                       else:
                           print("  Please answer with y/n [s d r i o g e c m f l ls](r){x} h=help?")

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
