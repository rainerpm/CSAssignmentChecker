# prerequisite
#   > pip install pyperclip
#   > download & install tkdiff (https://sourceforge.net/projects/tkdiff/)
#
# Demo
#  * unzip demo.zip in a folder on your hard drive
#    - ASSIGNMENT_GROUPS folder
#      > assignment Group folders
#          assignment folders
#             gold.txt
#             ?????Tester.java (optional)  ???? = assignment name
#          periods.txt
#      > comments.txt  (global comments)
#    - 1,4,5 a folder for each class period
#  * set the rootDir variable to the location of the unzipped demo folder
#  * set the validClassPeriods & validClassPeriodsString variables to indicate the class periods
#    you will use this program for (for the demo the class periods are 1,4,5)
#  * run CSassignmentChecker.py
#    - since this is the first time running, the program creates some required directories
#  * You should now see the main menu
#      (1 4 5) manual (a)utojudge (l)og e(x)it (<ENTER>=check)?
#    Enter 1 to have the program enter a mode in which it continually checks for activity for class Period 1
#    (as there is no activity currently, the program will print a . every 2 seconds to let you know it is alive)
#  * A student registers by submitting a file.
#    The file name must conform to the following naming convention - the contents of the file do not matter.
#      #LastFirst????_register.$$
#    where # is the student's class period, ???? is a unique 4 digit code for the student, $$ is either py, java, or zip.
#
#    Ideally students students have a way to "submit" a file directly to a class period folder on your hard drive.
#    This can be achieved by having them submit to an online folder that is automatically synched on your PC -
#    something like the Dropbox File Request feature. However, for this demo instead of students submitting a file to
#    the class Period directory demo/1/ folder, we will instead copy the two files in
#    demo/sampleSubmissions/studentRegistrations/ to demo/1/.  The program
#    (which is still waiting for activity in this directory) detects the two files and
#    registers the students (by creating/updating a file called REGISTER.txt).
#    NOTE:  The demo/5/ and demo/6/ already come with a REGISTER.txt file in the demo.
#  * A student submits their code for an assignment in the same way they register except the "register" in the file name is
#    replaced by the assignment name. The assignment name must match one of the name of one of the
#    assignment folders inside one of the assignment group folders in the ASSIGNMENT_GROUPS folder.
#    Again for the demo, we'll just copy the file demo/sampleSubmissions/studentProblems/1LovelaceAda1234_Collatz.java to demo/1/.
#    This represents the students solution to the collatz assignment. The program tests the student's code for the assignment collatz and compares it to the expected output stored in the test's gold.txt file
#    (demo\ASSIGNMENT_GROUPS\first6weeksAssignments\collatz\gold.txt). In this case the program will report *** CORRECT *** and
#    then bring you to the assignment menu.
#
#       y/n [i a o c e s f l](r){x} h=help?
#
#    Here
#    
#  * To associate an email address with a student manually edit the demo/1/REGISTER.txt file and enter
#    a student email as a 4th field for the student.
#      
#
#
#
# Run & judge all student assignment that are in a directory for their class on your computer.
# Each assignment is part of an assignment group, that has its own PC2 like scoreboard.
# Currently supports python submissions (.py extension) as well as java (.java,.zip extensions)

# SETUP
#  * set pythonIdeLoc,javaIdeLoc,tkdiffLoc variables below.
#  * Create the main directory for this program and set the rootDir variable to the path of this directory
#  * Set the validclassPeriods variable below to a list of your class periods
#  * Inside the root directory create a class directory for each of your classes in the validclassPeriods variable
#  * Inside each class directory create an assignmentGroup directory named ##_????? (## unique two digit number, ???? = name of assignmentGroup)
#  * Inside each assignmentGroup directory
#    - Create a directory named 00GOLDEN. Inside 00GOLDEN create a directory for each assignment with the name of that assignment.
#      Inside each assigment directory create a file named gold.txt (aka the judge's output file). The student's program output for
#      an assignment will be compared to this gold.txt file using tkdiff.  Also put any input file(s) (aka the judge's data files)
#      that will be read by the student's program into this assignment directory.
#    - For a java assignment create a directory named 00TESTER and put the JAVA test program named TESTER?????.
#      (where ????? is the assignment name). This is the program that will be run to test a student's program.
#  * Create a directory for the scoreboard files and set the scoreboardDir variable to the path of this directory
# RUNNING (TEACHER)
#  Program is run in a timed stamped assignment folder for the student that is inside the assignmentGroup directory in a folder
#  named for the student.
#  After the program runs (or has an error) teacher is prompted with   y/n [i a e s f l](r){x} h=help?
#   'y' submission correct. UPDATE scoreboard, CONTINUE to next submission.
#   'n' submission incorrect. UPDATE scoreboard, CONTINUE to next submission.
#   'i' show the program in IDE.
#   'a' run the program again.
#   'o' print output to screen with \n replaced by ↵
#   'c' copy information to clipboard (in case email is blocked).
#   'e' email student.
#   'r' remove submitted file. CONTINUE to next submission.
#   's' save submission in 00SAVE directory.
#   'f' print files in student directory.
#   'l' print class log file (chosing l again will get the next earlier set of lines)
#   'x' exit this program (does not remove submitted file).
#   'h' help for menu choices.
# SUBMITTING (STUDENT)
#  Submitted programs must be named ^^(\d+)([a-zA-Z-]+)(\d+)_(.+)\. (e.g. 1LovelaceAda5678_collatz.py)
#   * (\d+) = class ID
#   * ([a-zA-Z-]+) = student name
#   * (\d+) = student code
#   * (.+) = assignment name (all characters between _ and last .

# TODO/IMPROVEMENTS
#   * extract the latest submission from each student into an "assignment directory"
#   * (optionally) sort the program output (for random order JUNIT tests)
#   * (optionally) sort dictionaries
#   * add a 'g' option for grading.  Enter absolute grade or a deduction (how to handle multiple deductions).
#   * multiple tests per assignment (e.g. easy, medium, hard tests)

import scoreboard  # import the associated scoreboard.py which creates the scoreboard files

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
import ssl     # for gmail
import smtplib # for gmail & outlook
from   email.mime.text      import MIMEText      # for outlook
from   email.mime.multipart import MIMEMultipart # for outlook
from   email.mime.base      import MIMEBase      # for outlook 
from   email                import encoders      # for outlook
import pyperclip        # allows python to add things to the clipboard (so it can be quickly pasted)



rootDir = r'C:/Users/E151509/Dropbox/Apps/StudentFiles/'  # root directory containing the class directories
rootDir = r'C:/Users/E151509/Google Drive/My LASA/misc/tools/CSAssignmentChecker/demo1/'

validClassPeriods = ["1","4","5"]         # my java and python class periods
validClassPeriodsString = "(1 4 5)"       # used in MAIN menu

# rootDir = r'C:/Users/E151509/Downloads/testDir/'  # root directory containing the class directories
scoreboardDir = r'C:/Users/E151509/Google Drive/Course Materials/Introduction to Computer Science/10.Python/scoreboard'
# scoreboardDir = r'C:/Users/E151509/Downloads/testDir/scoreboards/'
pythonIdeLoc = r'C:\Users\E151509\AppData\Local\Programs\Python\Python310\Lib\idlelib\idle.pyw'
javaIdeLoc = r'c:/Program Files (x86)/jGRASP/bin/jgrasp.exe'              # location of JAVA IDE   executable
tkdiffLoc = r'c:/Program Files/TkDiff/tkdiff.exe'                         # location of tkdiff     executable
#################### OBFUSCATE IF SHARING PROGRAM ###################
emailSendFromAddress = "rainer.mueller@austinisd.org"
emailSendFromPassword = "farGoMcm97"
emailSignature = "\n\nMr. Mueller\n\n"
emailAttachmentDir = r"C:/Users/E151509/Downloads/StudentAttachment/"  # use newest file in this dir as email attachment
#################### OBFUSCATE IF SHARING PROGRAM ###################

validFileExtensions = [".py",".java",".zip"]  # .py for python, .java/.zip for java

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
                    print(" ", file)

# return a dictionary of all registered students and create student directory
# if it does not yet exist
def loadRegisteredStudents(assignmentGroups):
    classRegistration = {}
    if os.path.isfile("REGISTER.txt"):
        with open("REGISTER.txt", "r") as freg:
            for line in freg:
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
    for globalAssignmentGroupDirOnly in listOfGlobalAssignmentGroupDirectories:
        globalAssignmentGroupDir = os.path.join(rootDir,"ASSIGNMENT_GROUPS",globalAssignmentGroupDirOnly)
        classesFile = os.path.join(globalAssignmentGroupDir,"periods.txt")
        with open(classesFile, "r") as cfile:
            classPeriods = cfile.read().replace("\n"," ").split()
        for classPeriod in classPeriods:
            classAssignmentGroupDir = os.path.join(rootDir,classPeriod,globalAssignmentGroupDirOnly)
            if not os.path.isdir(classAssignmentGroupDir):
                os.mkdir(classAssignmentGroupDir)
                print("Created directory",classAssignmentGroupDir)
            goldenDir = os.path.join(classAssignmentGroupDir,"00GOLDEN")
            saveDir = os.path.join(classAssignmentGroupDir,"00SAVE")
            if not os.path.isdir(saveDir):
                os.mkdir(saveDir)
                print("Created directory",saveDir)
            plagiarismDir = os.path.join(classAssignmentGroupDir,"00PLAGIARISM")
            if not os.path.isdir(plagiarismDir):
                os.mkdir(plagiarismDir)
                print("Created directory",plagiarismDir)
            testersDir = os.path.join(classAssignmentGroupDir,"00TESTERS")
            assignmentGroup = {}  # create content dict, then add to it
            assignmentGroup["assignmentGroupDir"] = classAssignmentGroupDir
            assignmentGroup["goldenDir"] = globalAssignmentGroupDir   # this is in the GLOBAL assignment group directory
            assignmentGroup["testersDir"] = testersDir
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
    print("  ready to send", subject, "email to", receiverEmailAddress)
    comment = commentFromFile(submission)
    response = ""
    if comment:
       response = input("  attachment (y)? ")
    attachment = ""
    if response == "y":
        listOfFiles = glob.glob(os.path.join(emailAttachmentDir,r"*"))
        newestFileInDirectory = max(listOfFiles, key=os.path.getctime)
        filename = os.path.basename(newestFileInDirectory)
        filename = filename.replace(" ", "_")  # Outlook email routine does not like spaces in filename
        dirname = os.path.dirname(newestFileInDirectory)
        attachment = os.path.join(dirname,filename)
        os.rename(newestFileInDirectory, attachment)
        comment = comment + "\nBe sure to look at the attachment."
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
    print("    0 enter a new comment for assignment " + submission["Assignment"] + " that will also be saved.")
    lines1 = lines2 = []
    choice1 = 0
    if os.path.exists(os.path.join(submission["goldenAssignmentDir"],"comments.txt")):
        with open(os.path.join(submission["goldenAssignmentDir"],"comments.txt")) as commentFile:
            lines1 = commentFile.readlines()
            print("    SAVED COMMENTS for assignment " + submission["Assignment"])
            for line in lines1:
                choice1 += 1
                print(f'   {choice1:2d} ' + line.rstrip()[:80])
    choice2 = chr(ord('a')-1)
    if os.path.exists(os.path.join(rootDir,"ASSIGNMENT_GROUPS","comments.txt")):
        with open(os.path.join(rootDir,"ASSIGNMENT_GROUPS","comments.txt")) as commentFile:
            lines2 = commentFile.readlines()
            print("    GLOBAL COMMENTS")
            for line in lines2:
                choice2 = chr(ord(choice2)+1)
                print(f'    {choice2} ' + line.rstrip()[:80])
        lines = lines1 + lines2
    while True:
        response = input("    Select <0-" + str(choice1) + "> or <a-" + choice2 + "> (<ENTER> for one time comment)? ")
        if response == "":
            comment = input("    enter one time comment that will not be saved for next time (use \\n for newline) \n    -> ")
            break
        response = int(response) if response.lstrip('-').isnumeric() else ord(response)-96+choice1
        if not(response >= 0 and response <= len(lines)):
            print("  Not a valid response.")
        else:
            if response == 0:
                comment = input("  enter new comment (use \\n for newline) -> ")
                response = input("  add comment to assignment's comments.txt file (y)? ")
                if response == 'y':
                    with open(os.path.join(submission["goldenAssignmentDir"],"comments.txt"),"a") as commentFile:
                        commentFile.write(comment + '\n')                       
            else:
                comment = lines[response-1]
            break
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

def processCurrentSubmission(currentSubmission, assignmentGroups, assignments,classRootDir):
    submission = {}
    # submission["dateTime"] = datetime.now().strftime("%Y_%m_%d_%Hh%Mm%Ss")
    # submission["dateTime"] = datetime.now().strftime("%b_%d_%Hh%Mm%Ss")
    submission["FileName"] = currentSubmission
    submission["FileNameRoot"] = os.path.splitext(submission["FileName"])[0]
    submission["FileExtension"] = os.path.splitext(submission["FileName"])[1]
    if submission["FileExtension"] == ".py":
        submission["language"] = "python"
    else:
        submission["language"] = "java"
    fname = Path(currentSubmission)
    submission["submissionDateTime"] = datetime.fromtimestamp(fname.stat().st_mtime).strftime("%b_%d_%Hh%Mm%Ss")
    submission["submittedFileNameWithDate"] = submission["FileNameRoot"] + "_" + submission["submissionDateTime"] + submission["FileExtension"]
    match1 = re.search("^(\d+)((.+)_(.+))\.", submission["FileName"])
    submission["validAssignment"] = False
    submission["assignmentInGroup"] = False
    submission["valid"] = False
    if match1:  # file name has main three parts
        classPeriod = match1.group(1)
        nameAndCode = match1.group(3)
        assignment = match1.group(4)
        match2 = False
        match3 = False
        if '(' in nameAndCode:   # Handle pair filenames 2Lovelace(Turing)Ada(Alan)1234(6789)_test
            match2 = re.search("(.*?)\((.*?)\)(.*?)\((.*?)\)(.*?)\((.*?)\)",nameAndCode)
            if match2:
                name = match2.group(1) + match2.group(3)
                code = match2.group(5)
                submission["partnerName"] = match2.group(2) + match2.group(4)
                submission["partnerCode"] = match2.group(6)
        else:
            match3 = re.search("(.*?)(\d+)",nameAndCode)
            if match3:
                name = match3.group(1)
                code = match3.group(2)
    submission["validFormat"] = match1 and (match2 or match3)
    if submission["validFormat"]:
        submission["classPeriod"] = classPeriod.strip()
        submission["studentName"] = name.strip()
        submission["studentCode"] = code.strip()
        submission["Assignment"]  = assignment.strip()
##        print("*** DBG",submission["classPeriod"],submission["studentName"],submission["studentCode"],submission["Assignment"])
##        if match2:
##            print("*** DBG","(partner",submission["partnerName"],submission["partnerCode"]+')')
        submission["validAssignment"] = submission["Assignment"] in assignments
        submission["assignmentFileName"] = submission["Assignment"] + submission["FileExtension"]
        submission["outFileName"] = submission["Assignment"] + "_out.txt"
        submission["outCorrectFileName"] = submission["Assignment"] + "_" + submission["submissionDateTime"] + "_out_CORRECT.txt"
        submission["outLongFileName"] = submission["Assignment"] + "_" + submission["submissionDateTime"] + "_out.txt"
        submission["compileErrFileName"] = submission["Assignment"] + "_" + submission["submissionDateTime"] + "_compileErr.txt"
        submission["runErrFileName"] = submission["Assignment"] + "_" + submission["submissionDateTime"] + "_runErr.txt"
        submission["errorFileName"] = submission["Assignment"] + "_err.txt"
        if submission["validAssignment"]:
            submission["assignmentGroupId"] = assignments[submission["Assignment"]]  # assignment group assignment belongs to
            assignmentGroup = assignmentGroups[submission["assignmentGroupId"]]  # dictionary with info for this assignment group
            submission["listOfAssignments"] = assignmentGroup["listOfAssignments"]
            submission["assignmentInGroup"] = submission["Assignment"] in submission["listOfAssignments"]
            if submission["assignmentInGroup"]:  # valid assignment name for group, so setup everything for the submitted assignment
                submission["valid"] = True
                # directories
                submission["classDir"] = classRootDir;
                submission["assignmentGroupDir"] = assignmentGroup["assignmentGroupDir"]
                submission["goldenDir"] = assignmentGroup["goldenDir"]
                submission["goldenAssignmentDir"] = os.path.join(assignmentGroup["goldenDir"], submission["Assignment"])
                submission["goldFile"] = os.path.join(submission["goldenAssignmentDir"], "gold.txt")
                submission["testersDir"] = assignmentGroup["testersDir"]
                submission["saveDir"] = assignmentGroup["saveDir"]
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
                if "partnerName" in submission:
                    submission["partnerDir"] = os.path.join(submission["assignmentGroupDir"],submission["partnerName"] + "_" + submission["partnerCode"])
                    if not os.path.isdir(submission["partnerDir"]):
                        os.mkdir(submission["partnerDir"])

    return submission

def copyFromGolden(goldenAssignmentDir, pgmRunDir):
    goldenDirFiles = os.listdir(goldenAssignmentDir)
    for goldenDirFile in goldenDirFiles:
        if goldenDirFile != "gold.txt":
            fullGoldenDirFile = os.path.join(goldenAssignmentDir, goldenDirFile)
            if os.path.isfile(fullGoldenDirFile):
                copy(fullGoldenDirFile, pgmRunDir)

# returns True if output file matches golden file EXACTLY (except for line ending spaces or extra spaces/newlines at end of file)
def filesMatch(outputFile,goldenFile):
    with open(outputFile) as ofile:
        output = ofile.read().rstrip().split("\n")
    with open(goldenFile) as gfile:
        golden = gfile.read().rstrip().split("\n")
    match = True
    if len(output) != len(golden):
        match = False
    else:
        for i in range(len(golden)):
            if golden[i].rstrip() != output[i].rstrip():
                match = False
                break
    return match   

def runProgram(submission, classRootDir):
    correct = False
    error = False
    #os.chdir(classRootDir)
    if submission["FileExtension"] == ".java":
        copyfile(os.path.join(classRootDir,submission["FileName"]),os.path.join(submission["studentPgmRunDir"],submission["assignmentFileName"]))  # filename has to match assignment name for java
    else:  # .zip files or Python .py files
        copyfile(os.path.join(classRootDir,submission["FileName"]),os.path.join(submission["studentPgmRunDir"],submission["FileName"])) 
    copyFromGolden(submission["goldenAssignmentDir"], submission["studentPgmRunDir"])
    os.chdir(submission["studentPgmRunDir"])
    if submission["language"] == "python":
        compileCmd = ["python","-m","py_compile",submission["FileName"]]
        runCmd = ["python", submission["FileName"]]
    elif submission["language"] == "java":
        if submission["FileExtension"] == ".zip":
            result = subprocess.run(["tar", "-xf", submission["FileName"]])  # EXTRACT zip file
        # Think about having multiple Tester programs for each program (e.g. easy, medium, hard???)
        #for file in glob.glob(os.path.join(submission["testersDir"],submission["Assignment"] + "Tester.java")):  # copy TESTERS program to student directory
        #   copy(file, os.path.join(submission["studentPgmRunDir"],"."))
        if os.path.exists(os.path.join(submission["Assignment"] + "Tester.java")):
            javaPgmName = submission["Assignment"] + "Tester.java"
        else:
            javaPgmName = submission["assignmentFileName"]
        compileCmd = ["javac", "*.java"]
        runCmd = ["java", javaPgmName]
    else:
        print("ERROR!!! Unsupported language")
        sys.exit()
    # language independant code
    with open("CompilerOutput.txt", "w") as fout:      
        with open("CompilerError.txt", "w") as ferr:
            result = subprocess.run(compileCmd, stdout=fout, stderr=ferr)  #COMPILE PROGRAM
    errorCompile = checkErrorFileForErrors("CompilerError.txt", "  COMPILE ERROR")
    if errorCompile:
        copyfile("CompilerError.txt", os.path.join(submission["classDir"],submission["studentName"] + "_compileError.txt"))  # copy compile error file to class directory
        copyfile("CompilerError.txt", os.path.join(submission["studentDir"],submission["compileErrFileName"]))  # copy output file to data directory
        if "partnerName" in submission:
            copyfile("CompilerError.txt",os.path.join(submission["partnerDir"],submission["compileErrFileName"]))  # copy output file to partner's data directory
        updateLogFile(submission, "  ERROR!!! " + submission["FileName"] + " had a compile time error.",False)        
    else:
        if os.path.exists(os.path.join(submission["classDir"],submission["studentName"] + "_compileError.txt")):
            os.remove(os.path.join(submission["classDir"],submission["studentName"] + "_compileError.txt"))
        with open(submission["outFileName"], "w") as fout:
            with open(submission["errorFileName"], "w") as ferr:
                result = subprocess.run(runCmd, stdout=fout, stderr=ferr)   # RUN PROGRAM
        errorRun = checkErrorFileForErrors(submission["errorFileName"], "  RUNTIME ERROR")            
        if errorRun:
            if os.path.exists(submission["outFileName"]):
                os.remove(submission["outFileName"])
            copyfile(submission["errorFileName"], os.path.join(submission["classDir"],submission["studentName"] + "_runTimeError.txt"))  # copy compile error file to class directory
            copyfile(submission["errorFileName"], os.path.join(submission["studentDir"],submission["runErrFileName"]))  # copy output file to data directory
            if "partnerName" in submission:
                copyfile(submission["errorFileName"],os.path.join(submission["partnerDir"],submission["runErrFileName"]))  # copy output file to partner's data directory
            updateLogFile(submission, "  ERROR!!! " + submission["FileName"] + " had a run time error.",False)        
        else:
            if os.path.exists(os.path.join(submission["classDir"],submission["studentName"] + "_runTimeError.txt")):
                os.remove(os.path.join(submission["classDir"],submission["studentName"] + "_runTimeError.txt"))
    error = errorCompile or errorRun
    if not error:
        correct = filesMatch(submission["outputFile"],submission["goldFile"])
        if correct:
            print("  *** CORRECT ***")
        else:
            if autoJudging:
                print("  INCORRECT (autojudged)")
            else:
                tkdiffCmd = [tkdiffLoc,submission["outputFile"],submission["goldFile"]]
                result = subprocess.run(tkdiffCmd, shell=True)     # TKDIFF
            with open(os.path.join(submission["studentPgmRunDir"], "tkdiff.bat"), "w") as ftkdiff:  
                ftkdiff.write('"' + tkdiffLoc + '"' + " " + submission["outFileName"] + " " + os.path.join(submission["goldenAssignmentDir"], "gold.txt"))
            # also write tkdiff batch file to class directory (for quick access to each student's last run results)
            if os.path.exists(os.path.join(classRootDir,submission["studentName"] + "_tkdiff" + ".bat")):
                os.remove(os.path.join(classRootDir,submission["studentName"] + "_tkdiff" + ".bat"))
            with open(os.path.join(classRootDir,submission["studentName"] + "_tkdiff" + ".bat"), "w") as ftkdiff:
                ftkdiff.write('"' + tkdiffLoc + '"' + " " + os.path.join(submission["studentPgmRunDir"],submission["outFileName"]) + " " + os.path.join(submission["goldenAssignmentDir"], "gold.txt"))
    os.chdir(classRootDir)
    return correct, error

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

def submissionCorrect(submission):
    if not os.path.exists(os.path.join(submission["plagiarismAssignmentDir"],submission["submittedFileNameWithDate"])):
        os.rename(submission["FileName"], os.path.join(submission["plagiarismAssignmentDir"],submission["submittedFileNameWithDate"]))  # move pgm to PLAGIARISM directory
    copyfile(os.path.join(submission["studentPgmRunDir"],submission["outFileName"]), os.path.join(submission["studentDir"],submission["outCorrectFileName"]))  # copy output file to data directory
    if "partnerName" in submission:
        copyfile(os.path.join(submission["studentPgmRunDir"],submission["outFileName"]), os.path.join(submission["partnerDir"],submission["outCorrectFileName"]))  # copy output file to partner's data directory
    scoreboard.updateScoreboard(scoreboardDir,submission["assignmentGroupDir"],submission["assignmentGroupId"],submission["classPeriod"],submission["listOfAssignments"])
    updateLogFile(submission, "  *** CORRECT *** ")

def submissionIncorrect(submission):
    if submission["valid"]:
        if os.path.exists(os.path.join(submission["studentPgmRunDir"],submission["outFileName"])):
            copyfile(os.path.join(submission["studentPgmRunDir"],submission["outFileName"]),os.path.join(submission["studentDir"],submission["outLongFileName"]))  # copy output file to data directory
            if "partnerName" in submission:
                copyfile(os.path.join(submission["studentPgmRunDir"],submission["outFileName"]),os.path.join(submission["partnerDir"],submission["outLongFileName"]))  # copy output file to partner's data directory
        scoreboard.updateScoreboard(scoreboardDir,submission["assignmentGroupDir"],submission["assignmentGroupId"],submission["classPeriod"],submission["listOfAssignments"])
        updateLogFile(submission, "  >>> INCORRECT <<< ")
    else:
        updateLogFile(submission, "  >>> INVALID SUBMISSION <<< ")        
    os.remove(submission["FileName"])

            
### MAIN PROGRAM ###
def main():
    global interrupted, autoJudging, autoJudgingPeriods, autoJudgingSleepTime

    allAssignmentGroups, allAssignments = setup()
    autoJudging = False
    autoJudgingFirstTime = True
    autoJudgingSleepTime = 60  # in seconds
    while True:
        print("Directory =",rootDir)
        os.chdir(rootDir)
        inputContinue = False
        lCount = 0
        while not(inputContinue or not autoJudgingFirstTime):
            check4Activity()
            response = input("\n" + validClassPeriodsString + " manual (a)utojudge (l)og e(x)it (<ENTER>=check)? ")
            inputContinue = (response == 'x') or (response in validClassPeriods)
            if response in validClassPeriods:
                classPeriod = response
            elif response == "a":
                response2 = input(validClassPeriodsString + " autojudge (m)ultiple (<ENTER>=all periods)? ")
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
                submission = processCurrentSubmission(currentSubmission, assignmentGroups, assignments,classRootDir)
                updateLogFile(submission,"\nRECEIVED " + submission["FileName"])
                if submission["validFormat"]:  # format for assignment submission name is valid
                    if submission["Assignment"] == "register":  # student submitted a registration request
                        if submission["studentCode"] in classRegistration:
                            print(submission["studentCode"], "is already registered")
                            print("  current submission   ", submission["FileName"])
                            print("  previous registration", classRegistration[submission["studentCode"]])
                        else:
                            with open("REGISTER.txt", "a") as freg:
                                freg.write(f'{submission["studentCode"]} {submission["studentName"]} {submission["classPeriod"]}\n')
                                classRegistration[submission["studentCode"]] = (submission["studentName"],submission["classPeriod"])
                                updateLogFile(submission,"registered " + submission["studentCode"] + " " + submission["studentName"] + " " + submission["classPeriod"],True)
                        os.remove(submission["FileName"])  # remove registration file (assignment name was register, file has served its purpose)
                        continue  # CONTINUE TO NEXT SUBMISSION

                    if registrationRequired:  # if registration is required, check to see if student is registered
                        if (not submission["studentCode"] in classRegistration) or (classRegistration[submission["studentCode"]][0] != submission["studentName"]):
                            if submission["studentCode"] in classRegistration:
                                print("  code " + submission["studentCode"] + " was previously registered as",classRegistration[submission["studentCode"]])
                                response = input("  show registered students (y)? ")
                                if response == "y":
                                    with open("REGISTER.txt", "r") as r:
                                        for line in sorted(r):
                                            print(line, end="")
                            else:                              
                                updateLogFile(submission, "  ERROR!!! " + submission["studentCode"] + " has not been previously registered!!!",True)
                    # if it is a known assignment
                    if submission["validAssignment"]:
                        if submission["assignmentInGroup"]:
                            ### run the program ###
                            print("\n"+submission["studentName"] + " * " + submission["Assignment"] + " * " + " (" + submission["FileName"] + ") " + submission["submissionDateTime"])
                            correct,error = runProgram(submission, classRootDir)
                        else:
                            updateLogFile(submission, "  ERROR!!! >>" + submission["Assignment"] + "<< is not an assignment in", submission["assignmentGroupId"],"(submitted file " + submission["FileName"] + ")",True)
                    else:
                        updateLogFile(submission, "  ERROR!!! >>" + submission["Assignment"] + "<< is not a known assignment name (submitted file " + submission["FileName"] + ")",True)
                else:  # format for assignment submission name is INVALID
                    print("  Submitted file name not in  correct format -> " + submission["FileName"])
                lCount = 0
                if autoJudging:
                    if correct:
                        submissionCorrect(submission)                                               
                    else:
                        submissionIncorrect(submission)                         
                while not autoJudging:    # loop until a valid response
                    if submission["valid"]:
                        answer = input("  y/n [i a o c e s f l](r){x} h=help? ")
                    else:
                        answer = input("  Invalid submission c [i e s](r){x} h=help? ")
                    if submission["valid"] and answer == "y":  # submission correct. UPDATE scoreboard, CONTINUE to next submission.
                        submissionCorrect(submission)
                        break
                    elif submission["valid"] and answer == "n":  # submission incorrect. UPDATE scoreboard, CONTINUE to next submission.
                        submissionIncorrect(submission)
                        break
                    elif answer == "i":  # open program in IDE
                        if submission["valid"]:
                            os.chdir(submission["studentPgmRunDir"])
                        if submission["language"] == "python":
                            if os.path.exists(pythonIdeLoc):
                                pythonIdeCmd = [pythonIdeLoc,submission["FileName"]]
                                result = subprocess.run(pythonIdeCmd, shell=True)
                            else:
                                print("Did not find IDE executable at " + pythonIdeLoc + "\nSet pythonIdeLoc variable in program to correct IDE location")
                        elif submission["language"] == "java":
                            javaIdeCmd = [javaIdeLoc,submission["Assignment"] + ".java"]
                            result = subprocess.run(javaIdeCmd, shell=True)
                        os.chdir(classRootDir)
                    elif answer == "o":   # open program in Notepad++
                        outfile = os.path.join(submission["studentPgmRunDir"],submission["outFileName"])
                        with open(outfile,'r') as outf:
                           for line in outf:
                               line = line.replace("\n","↵")
                               print(line)
                    elif submission["valid"] and answer == "a":  # run program again
                        runProgram(submission, classRootDir)
                    elif answer == "e":  # email student
                        emailStudent(submission, classRegistration)
                    elif answer == "n":  # new submission name
                        if autoJudging:
                            break
                        else:
                            newFileName = input("  Enter new filename for " + submission["FileName"] + " -> ")
                            copyfile(submission["FileName"],newFileName)  # move output file to data directory
                            updateLogFile(submission, "  changed name from " + submission["FileName"] + " to " + newFileName)
                    elif answer == "s":  # save submission
                        copyfile(os.path.join(classRootDir,submission["FileName"]),os.path.join(submission["saveDir"],submission["FileName"]))  # copy (replace if already there) pgm to 00SAVE directory
                        updateLogFile(submission, "  copied to " + os.path.join(submission["saveDir"],submission["FileName"]),True)
                    elif submission["valid"] and answer == "f":  # files (show files in student directory)
                        print("    " + submission["studentPgmRunDir"])
                        # print("    " + '/'.join(submission["studentPgmRunDir"].split('/')[-3:]))   # print the last 3 folders in path
                        for file in glob.glob(os.path.join(submission["studentPgmRunDir"],"*")):
                            print("    " + os.path.basename(file))
                    elif answer == "l":  # log, show the class log file (chosing l again will get the next earlier set of lines)
                        with open(os.path.join(rootDir,"logGlobal.txt")) as logfile:
                            lines = logfile.readlines()
                            fromLine = -min((lCount+1)*20,len(lines))
                            if lCount > 0:
                                for line in lines[fromLine:-(lCount*20)]:
                                    print(line.rstrip())
                            else:
                                for line in lines[fromLine:]:
                                    print(line.rstrip())
                        lCount += 1                        
                    elif answer == "r":  # remove submitted file. CONTINUE to next submission.
                        response = input("  Save in directory" + submission["saveDir"] + " before removing (y)? ")
                        if response == "y":
                            os.replace(os.path.join(classRootDir,submission["FileName"]),os.path.join(submission["saveDir"],submission["FileName"]))  # move (replace if already there) pgm to 00SAVE directory
                        else:
                            response = input("Confirm remove (y)? ")
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
                        if "studentCode" in submission and submission["studentCode"] in classRegistration:
                            if len(classRegistration[submission["studentCode"]]) > 2:  # email address was manually added to REGISTER.txt
                                receiverEmailAddress = classRegistration[submission["studentCode"]][2]
                        subject = "P"+ submission["classPeriod"] + "StudentDrop (" + submission["Assignment"] + ")"
                        pyperclip.copy(subject)
                        time.sleep(0.5)
                        pyperclip.copy(receiverEmailAddress)
                        print("  ready to paste (subject & email address)!!!")
                    elif answer == "x":  # exit program
                        print("exiting program")
                        sys.exit()
                    elif answer == "h":
                        if submission["valid"]:
                            print("  'y' submission correct. UPDATE scoreboard, CONTINUE to next submission.")
                            print("  'n' submission incorrect. UPDATE scoreboard, CONTINUE to next submission.")
                        print("  'i' show the program in IDE.")
                        print("  'o' print output with newline replaced by ↵")
                        if submission["valid"]:                        
                            print("  'a' run the program again.")
                        else:
                            print("  'c' change name of the submitted file.")
                        print("  'c' copy information to clipboard (in case email is blocked).")
                        print("  'e' email student (to avoid having to enter student's email add email after class number in REGISTER.txt file).")
                        print("  'r' remove submitted file. CONTINUE to next submission.")
                        print("  's' save submission in 00SAVE directory.")
                        if submission["valid"]:
                             print("  'f' print files in student directory.")
                        print("  'l' print class log file (chosing l again will get the next earlier set of lines)")
                        print("  'x' exit this program (does not remove submitted file).")
                        print("  'h' help for menu choices.")
                    elif answer == "t":   # temporary functionality
                        if "studentCode" in submission and submission["studentCode"] in classRegistration:
                            if len(classRegistration[submission["studentCode"]]) > 2:  # email address was manually added to REGISTER.txt
                                receiverEmailAddress = classRegistration[submission["studentCode"]][2]
                    else:
                        if submission["valid"]:
                            print("  Please answer with y/n [i a e s f l](r){x} h=help?")
                        else:
                            print("  Please answer with c [i e s l](r){x} h=help? ")
                             
            elif not autoJudging:  # no current submissions (wait for new ones)
                currentSubmissions = getSubmissions(validFileExtensions)
                print("PERIOD *",classPeriod,"* waiting for new submissions (<Ctrl-C> back to main menu) ", end="",flush=True)
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
