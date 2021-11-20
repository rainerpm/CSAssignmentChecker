# CSAssignmentChecker

### Overview

The **CSAssignmentChecker.py** program verifies python or java assignments submitted by students. This program does basic verification by simply running the submitted student's .py or .java program and comparing the program's output to a teacher provided "gold" output file. If the two don't match, the program shows the highlighted differences. More advanced verification is possible for JAVA assignments by allowing a student to submit multiple .java files which can then verified by a teacher provided Checker and/or Tester program. 

### Required Python packages
  * pip install pyperclip
  * pip install pillow
  
### Other Requirements
  * download & install a diff program such as meld (https://meldmerge.org/).

### Assignment Submission and Verification
Student submit an assignment by submitting a single file to their class period folder on the teacher's computer running this program.
The submitted file must be named **#LastFirst?_@.$** (KEY for whole README: **#** student's class period, **LastFirst** student's name, **?** unique student number, **@** assignment name, **$** file extension: either py, java for individual files or zip for multiple files) and the java class must be named @. Since a java program's file name must match its class name, this program renames **#LastFirst?_@.java** to simply **@.java**.

Ideally students students have a way to submit a file in real time directly to the class's period folder on the teacher's hard drive (one way to do this is to have the students submit to an online folder that is automatically synched to the teacher's PC - e.g. [Dropbox File Request feature](https://fileinbox.com/articles/dropbox-file-requests-ultimate-guide#:~:text=Unfortunately%2C%20Dropbox%20File%20Requests%20don,to%20create%20a%20Dropbox%20account.).

* **Basic Verification**  When the student submits a Python or JAVA program that simply prints its output, this program runs the student's program and compares the program's generated output to the teacher provided "golden" output.  The student's program can optionally read test data from a file named **@.dat**. As part of an assignment, student's are usually provided a **@.dat** file with a few basic test cases. A teacher will typically provide this program a **@.dat** file with more comprehensive test cases.  The student's program can optionally prompt the user for input - e.g. Python: input() JAVA: scan.nextInt().  To provide this user input, the teacher provides this program with one or more **pgmUserInput&.txt** files (& is a unique identifier, usually 1,2,3, ...). The submitted program is run once for each user input file.

* **Advanced Verification (JAVA only)** This program runs any or all of these OPTIONAL programs 
  * **@Checker.java**  [provided by teacher] Code to check the contents of the student's program (number and type of instance variables as well as details on the constructors and methods in the student's program). The output is compared to **checker.txt** file provided by the teacher. 
  * **@Runner.java**  [submitted by students] Contains the code that the student wrote that uses/tests the class(es) they wrote. The output is compared to the  **gold.txt** output file provided by the teacher. The @Runner.java program can optionally prompt the user for input. To provide this user input to this program, the teacher provides one or more runnerUserInput&.txt files (& is a unique identifier, usually 1,2,3, ...). The @Runner.java program will be run once for each user input file.
  * **@Tester.java**  [provided by teacher] Contains the code that the teacher wrote that uses/tests the program submitted by the student. The output is compared to the  **gold.txt** output file provided by the teacher.    

### Program (and Demo) Setup
* unzip demo.zip to a folder on your hard drive (i.e. C:/YourPathToDemoDir/demo)
  * **ASSIGNMENT_GROUPS** folder
    * **first6weeksAssignments, pythonAssignments** (these are the assignment group folders)
      * **Collatz, encryption** (these are the assignment folders  - the name of the assignment folder **is** the **assignment name**, assignment names must be unique)
         * **@.dat** is the teacher provided input data file for the assignment (@ is the **assignment name**). Typically this file contains more/harder test data then what's been given to the students.
         * **@Tester.java** is an optional test program (@ is the **assignment name**)
         * **@Checker.java** is an optional checker program (@ is the **assignment name**)
         * **pgmUserInput&.txt** user input files if the student's program requires user input - e.g. Python: input() JAVA: scan.nextInt() 
         * **runnerUserInput&.txt** user input files if the student also submits **@Runner.java** file
         * **gold.txt** is the teacher provided golden output for the assignment
         * **checker.txt** is the teacher provided checker output for the assignment
         * **comments.txt** contains the assignment specific comments used in student emails or clipboard
      * **periods.txt** indicates which class periods this assignment group is assigned to
    * **comments.txt** contains the global comments used in student emails or clipboard
  * **1,4,5** (these are the class period folders)
* set the following folder/directory variables in **customize.py**
  * set the **rootDir** variable to the location of the unzipped demo folder - C:/YourPathToDemoDir/demo 
  * set the **scoreboardDir** variable to C:/YourPathToDemoDir/demo/scoreboard
  * hereafter C:/YourPathToDemoDir/demo is abbreviated /demo.
* set the following executable variables
  * set the **pythonIdeLoc** variable to the location of the Python IDE (e.g. IDLE) executable.
  * set the **javaIdeLoc** variable to the location of the JAVA IDE (e.g. jGrasp) executable.
    * NOTE: The program uses *-parameters* compile option to ensure that JAVA reflection reflects parameter types instead of just using arg0
  * set the **textEditorLoc** variable to the location of a text editor (e.g. Notepad++) executable.
  * set the **diffLoc** variable to the location of the diff program (e.g. meld, kdiff, or tkdiff) executable.
### Run the Demo
The demo verifies two student assignments (1) [encryption](https://docs.google.com/document/d/1mr5FHL-cf3T1kRR0F10KCWwGGdjZC4Cj/edit?usp=sharing&ouid=117088614197672338242&rtpof=true&sd=true) (2) [Collatz](https://docs.google.com/document/d/1TKC45I9ZGvg82XGRzkpnoEnlxtC9xXnPdiv9Qmajf9g/edit?usp=sharing)
* run CSassignmentChecker.py
  * since this is the first time the program has been run, the program creates some required directories.
  * You should now see the Main Menu\
    **(1 4 5)manual (a)utojudge (l)og e(x)it (ENTER=check)?**\
  **Answer 4** to have the program enter the manual mode for class period 4. In this mode, the program continually checks for new submissions to the class period folder /demo/4/. The program creates the directories for the two students have been registered with this class period.
  When there is no submission to process, the program will print a period every 2 seconds to let you know it is alive. Leave the program running (and printing periods) for now
* For this demo, instead of students submitting files to the class period folder, *we will simply copy example files from /demo/sampleSubmissions/*
* To demo the basic verification of a student program, copy /demo/sampleSubmissions/studentProblems/4ShotwellGwynne4381_encryption.py to the class period 4 folder /demo/4/. This file is Period 4's student Gwynne Shotwell's submission of the encryption assignment. The program (which up to now had been printing periods) will detect this file and run the program. 
   * Since this initial student program has an error, the program will use diff program to display the differences between the students program output and the expected "gold" output.
   * After you close the diff window, the program displays the Assignment Menu **y/n \[s d a i o g e c m f l ls](r){x} h=help?**
     * **Answer s** to show the program in the Python IDE.
     * **Answer n** to judge the program as incorrect. The student's program status is reflected in /demo/scoreboard/ (one file with the student's name and one that is annoymized using the student's 4 digit code that can be made accessible to the class).
   * Since the output was incorrect, the program also created a file (ShotwellGwynne.bat) in the latestResults folder inside the class period folder that enables the teacher to easily run diff program for the student's last incorrect submission and optionally bring up the program in the IDE or look at the data input file in the text editor.
   * fix the error on line 21 (changing thing[1] to thing[0]) in /demo/sampleSubmissions/studentProblems/4ShotwellGwynne4381_encryption.py and then once again copy the file to the class period 4 folder /demo/4/. 
    * Since the student now program works as expected the program reports *** CORRECT ***. NOTE: The program ignores any whitespace at the end of a line or the end of the output when comparing the student's output to the expected output in the assignment's gold.txt file.
     * **Answer y** to judge the program as correct and update the program's status in /demo/scoreboard/.
   * NOTE: This particular student program when run with the teacher supplied input file /demo/ASSIGNMENT_GROUPS/pythonAssignments/encryption/encryption.dat is expected to print out exactly what's found in /demo/ASSIGNMENT_GROUPS/pythonAssignments/encryption/gold.txt. 
* The program should now be in the mode of continually checking for new submissions to the class period folder /demo/4/. 
  * Use Ctrl-C to go back to the Main Menu.
* Each student should be registered with the program. To register two example students copy the two files in demo/sampleSubmissions/studentRegistrations/ to /demo/1/ 
  (NOTE: For registration purposes the assignment name part of the file name must be the word "register").
  **Answer 1** in the Main Menu.  The program detects the registration files in /demo/1/ and registers the 2 students by creating/updating a file called REGISTER.txt (and then deleting the registration files).
  For the demo the directories /demo/5/ and /demo/6/ already had predefined student registrations in a REGISTER.txt file.
* To demo the more advanced verification of a JAVA program, copy the student program /demo/sampleSubmissions/studentProblems/1LovelaceAda1234_Collatz.zip to the class period 1 folder /demo/1/.
  This represents the student's code for an assignment named "Collatz". The student submitted a zip file containing Collatz.java (definining the Collatz object) and the test code for that object that the student wrote in CollatzRunner.java. In addition to the expected output file gold.txt, the teacher has also supplied a specific test program called CollatzTester.java in the folder /demo/ASSIGNMENT_GROUPS/first6weeksAssignments/collatz/ as well as two runnerUserInput&.txt files to provide input to the Collatz. The program runs the CollatzTester program and should report *** CORRECT *** since the program's output matches the expected output.  Selecting **d** in the assignment menu will show the program and expected (which match). You'll see the output from the runs of CollatzTeseter.java, CollatzRunner.java (with runnerUserInput1.txt providing the user input),  and CollatzRunner.java (with runnerUserInput2.txt providing the user input)
  
### Main Menu  
The program's Main Menu\
**(? ? ?)manual (a)utojudge (l)og e(x)it (ENTER=check)?**\
has the following options
* **(? ? ?)** A choice of class period numbers which cause the program to enter manual mode and monitor that class period's folder for student program submissions.  The program processes any current (and future) program submissions to that class period's folder - oldest submission is processed first. Incorrect output differences will be shown in **diff window** after which the **Assignment Menu** is displayed.
* **(a)utojuge** Brings up the Autojudge Menu **(? ? ?)autojudge (m)ultiple (<ENTER>=all periods)?**. Specified class period folders are checked and any current (and future) program submissions are processed and automatically judged - if program output is not correct, the submission is counted as incorrect. 
* **(l)og** Program displays the last 20 lines of logGlobal.txt in **rootDir** 
* **e(x)it** Exits the program
* **ENTER** Pressing the *Enter* key causes the program to check all class periods for submissions and then returns to the Main Menu.

### Assignment Menu
In manual mode after a student's program submission has been run and either the program was correct or the program was incorrect and the **diff window** has been closed, the Assignment Menu\
**y/n \[s d a i o rn g e c s f l](r){x} h=help?**\
is displayed with the following options (NOTE: Be sure that you are done with the current assignment submission before answering y n m r as this will make program proceed to the next submission)
* **y** judge the student's program as correct, update the program's status in /demo/scoreboard/, and then move on to the next student submission. The teacher can choose to ignore inconsequential differences in the output shown in the **diff window** and still count the program correct.
* **n** judge the student's program as incorrect, update the program's status in /demo/scoreboard/, and then move on to the next student submission.
* **s** show the student's program submission in the IDE.
* **d** run diff program again
* **a** run the program again
* **i** show the data input file (@.dat file in assignment folder - @ is the **assignment name**) for the assignment (newline's are shown as ↵)
* **o** print the student's output (newline's are shown as ↵)
* **rn** rename submission and then process the renamed submission. 
* **g** prompt for grade and note and write to grades.txt file in student's assignment folder 
* **e** email the student with information regarding the assignment status.
* **c** copy information about the assignment status to the Clipboard (requires Windows 10’s October 2018 Update which provided a Clipboard History enabling multiple items to be saved on the clipboard). This option is provided, since emailing directly from the program may not be allowed by the school network.
* **m** move the student's program submission to the 00SAVE directory and then move on to the next student submission.
* **f** print a list of the files in the student's assignment directory.
* **l** print the last 20 lines of the global log file (logGlobal.txt).  Choosing l again shows the previous 20 lines.
* **ls** print the last 20 lines of the student's log file (log.txt).  Choosing ls again shows the previous 20 lines.
* **r** remove the submission from the class period directory and then move on to the next student's submission.
* **x** exit the program.
* **h** open web browser showing this page
 
### Sending Emails or using the Clipboard 
* To associate an email address with a student manually edit the REGISTER.txt file in the class period folder and enter a student email as a 4th field for the student.
* The program will give you options to use a saved set of comments or enter a new comment to be used in the mail or put on the clipboard. You can chooose from preset assignment specific comments (stored in the comments.txt file in the assignments folder) or global comments (stored in ASSIGNMENT_GROUPS/comments.txt)

### Batch Files
The latestResults directory inside the class directory will contain a batch file for each student's last submission. If the submission compiled & ran the batch file will run diff and then offer to open the IDE and input data files. If the submission did not compile or run, instead of running diff, the batch file will open the error file.
