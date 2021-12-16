# CSAssignmentChecker

### Overview

The **CSAssignmentChecker.py** program verifies python or java assignments submitted by students. This program currently supports basic verification for Python programs and more advanced verification for JAVA programs. Student assignments are organized into assignment groups, each of which has a "scoreboard" file showing the results for each student. The program supports directly emailing a teacher comment to a student.

### Requirements
The following programs are required (the programs in parenthesis are what I use, but may be replaced with something equivilant).
  * Python (https://www.python.org/downloads/)
    * The following are only required for providing a student feeback comment via email or the clipboard and can be installed later
      * pip install pyperclip (enables the program to access the clipboard)
      * pip install pillow (enables the program to "grab" an image from the most recent clipboard entry) 
  * JAVA (https://www.jgrasp.org/)
  * Text Editor (https://notepad-plus-plus.org/downloads/ **CSAssignmentChecker.py** uses a Notepad++ session file to open multiple files)
  * download & install a diff program (https://meldmerge.org/).

### Assignment Submission and Verification
Student submit an assignment by submitting a single file to the class period folder on the teacher's computer that is running this program.
The submitted file must be named **Last First ? - @.$** (where **Last** student's last name, **First** student's first name,  **?** unique student number, **@** assignment name, **$** file extension: either py, java for individual files or zip for multiple files). For JAVA, the class in the **Last First ? - @.$** file must be named @. An example of a valid filename is **Shotwell Gwynne 4381 - encryption.py**.

Ideally students students have a way to submit a file in real time directly to the class period folder on the teacher's hard drive (one way to do this is to have the students submit to an online folder that is automatically synched to the teacher's PC - e.g. [Dropbox File Request feature](https://fileinbox.com/articles/dropbox-file-requests-ultimate-guide#:~:text=Unfortunately%2C%20Dropbox%20File%20Requests%20don,to%20create%20a%20Dropbox%20account.).

* **Basic Verification**  When the student submits a Python or JAVA program that simply prints its output, this program runs the student's program and compares the program's generated output to the teacher provided "golden" output.  The student's program can optionally read test data from a file named **@.dat**. As part of an assignment, student's are usually provided a **@.dat** file with a few basic test cases. A teacher will typically provides a **@.dat** file with more comprehensive test cases to this program.  The student's program can optionally prompt the user for input - e.g. Python: input() JAVA: scan.nextInt().  To provide this user input, the teacher provides this program with one or more **pgmUserInput&.txt** files (& is a unique identifier, usually 1,2,3, ...). The submitted program is run once for each user input file.

* **Advanced Verification (JAVA only)** This program runs any or all of these OPTIONAL programs 
  * **@Checker.java**  [provided by teacher] Code provided by the teacher to check the contents of the student's program (number and type of instance variables as well as details on the constructors and methods in the student's program). The output is compared to the **checker.txt** file provided by the teacher. 
  * **@Runner.java**  [submitted by students] Code that the student wrote that uses the class(es) they wrote. The output is compared to the  **gold.txt** output file provided by the teacher. The @Runner.java program can optionally prompt the user for input. To provide this user input to this program, the teacher provides one or more runnerUserInput&.txt files (& is a unique identifier, usually 1,2,3, ...). The @Runner.java program will be run once for each user input file.
  * **@Tester.java**  [provided by teacher] Code provided by the teacher that tests the program submitted by the student. The output is compared to the  **gold.txt** output file provided by the teacher.    

### Program (and Demo) Setup
* unzip demo.zip to a folder on your hard drive (i.e. C:/YourPathToDemoDir/demo)
  * **ASSIGNMENT_GROUPS** folder
    * **first6weeksAssignments, pythonAssignments** (these folders contain a group of related assignments, each of which will have it's own scoreboard file)
      * **GCD, encryption** (these are the assignment folders  - the name of the assignment folder **is** the **assignment name**, assignment names must be unique)
         * **@.dat** is the teacher provided input data file for the assignment (@ is the **assignment name**). Typically this file contains more/harder test data then what's been given to the students.
         * **@Tester.java** is an optional test program (@ is the **assignment name**)
         * **@Checker.java** is an optional checker program (@ is the **assignment name**)
         * **pgmUserInput&.txt** user input files if the student's program requires user input - e.g. Python: input() JAVA: scan.nextInt() 
         * **runnerUserInput&.txt** user input files if the student also submits **@Runner.java** file
         * **gold.txt** is the teacher provided golden output for the assignment
         * **checker.txt** is the teacher provided checker output for the assignment
         * **comments.txt** contains the assignment specific comments used in student emails or clipboard
      * **periods.txt** indicates which class periods this assignment group is assigned to
    * **commentsJAVA.txt** and **commentsPYTHON.txt** contain the global comments used in student emails or clipboard
  * **1,4,5** (these are the class period folders, new files are submitted to these folders via something like a Dropbox File Request. Each assignment group has a folder here that has folders for each of the students containing folders for the student's program submissions.
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
* setup your email address and login in **login.py**
### Run the Demo
The demo verifies two student assignments (1) [encryption](https://docs.google.com/document/d/1mr5FHL-cf3T1kRR0F10KCWwGGdjZC4Cj/edit?usp=sharing&ouid=117088614197672338242&rtpof=true&sd=true) (2) [GCD](https://docs.google.com/document/d/14nIXTUOr70_zRUZojzMZhbs9AmTWs5WxatsVtjNT_c4/edit?usp=sharing)
* run CSassignmentChecker.py
  * since this is the first time the program has been run, the program creates some required directories.
  * You should now see the Main Menu\
    **(1 4 5)manual (a)utojudge (l)og e(x)it (ENTER=check)?**\
  **Answer 4** to have the program enter the manual mode for class period 4. In this mode, the program continually checks for new submissions to the class period folder /demo/4/. The program creates the directories for the two students have been registered with this class period.
  Since there is currently no submission to process, the program prints a period every 2 seconds to let you know it is alive. Leave the program running (and printing periods) for now
* For this demo, instead of students submitting files to the class period folder, *we will simply copy example files from /demo/sampleSubmissions/*
* To demo the basic verification of a student program, copy **/demo/sampleSubmissions/studentProblems/Shotwell Gwynne 4381 - encryption.py** to the class period 4 folder **/demo/4/**. This file is Period 4's student Gwynne Shotwell's (student code 4381) submission of the encryption assignment. The program (which up to now had been printing periods) will detect this file and run the program. 
   * Since this student program has an error, the program will use the diff program to display the differences between the students program output and the expected "gold" output.
   * After you've had a chance to look at the difference, close the diff window. The program now displays the Assignment Menu **y/n/p [s d a h i o g e c m f l ls](r){x}?**
     * **Answer s** to show/see the program in the Python IDE. After you've run and/or inspected the program, close the IDE.
     * **Answer n** to judge the program as incorrect. The student's program status is reflected in /demo/scoreboard/ (one file with the student's name and one that is annoymized using the student's code that can be made accessible to the class).
   * Since the output was incorrect, the program also created a file (ShotwellGwynne.bat) in the latestResults folder inside the class period folder that enables the teacher to easily run diff program for the student's last incorrect submission and optionally bring up the program in the IDE or look at the data input file in the text editor.
   * Edit **/demo/sampleSubmissions/studentProblems/Shotwell Gwynne 4381 - encryption.py** and fix the error on line 21 (changing thing[1] to thing[0]) and then once again copy the file to the class period 4 folder **/demo/4/**. 
    * Since the student's program output matches the assignments gold.txt file the program reports *** CORRECT ***. NOTE: The program ignores any whitespace at the end of a line or the end of the output when comparing the student's output to the expected output in the assignment's gold.txt file.
     * **Answer y** to judge the program as correct and update the program's status in /demo/scoreboard/.
   * NOTE: This particular student program when run with the teacher supplied input file /demo/ASSIGNMENT_GROUPS/pythonAssignments/encryption/encryption.dat is expected to print out exactly what's found in /demo/ASSIGNMENT_GROUPS/pythonAssignments/encryption/gold.txt. 
* The program is once again in the mode of continually checking for new submissions to the class period folder **/demo/4/**. 
  * Use Ctrl-C to go back to the Main Menu.
* The class Period directories for Period 4 & 5 (**/demo/4/** and **/demo/5/**) already contained student registrations in the REGISTER.txt file. For class Period 1, we will now register two students in the **/demo/1/Register.txt** file. To register the students copy the two files in demo/sampleSubmissions/studentRegistrations/ to  **/demo/1/**.
* **Answer 1** in the Main Menu.  The program detects the registration files in **/demo/1/** and registers the 2 students by creating/updating the file REGISTER.txt in the student's class period folder.
* To demo the more advanced verification of a JAVA program, copy the student program /demo/sampleSubmissions/studentProblems/Lovelace Ada 1234 - GCD.zip to the class period 1 folder /demo/1/.
  This represents the student's code for an assignment named "GCD". The student submitted a zip file containing **GCD.java** (definining the GCD object) and the test code for that object that the student wrote in **GCDRunner.java**. In addition to the expected output file gold.txt, the teacher has also supplied a specific test program called **GCDTester.java** in the folder **/demo/ASSIGNMENT_GROUPS/first6weeksAssignments/GCD/** as well as **runnerUserInput&.txt** files to provide user input to GCDRunner.java. The program runs the GCDTester program and should report *** CORRECT *** since the program's output matches the expected output in gold.txt.  Selecting **d** in the assignment menu shows the program and expected output in the diff program. This is the output from the runs of GCDTester.java and GCDRunner.java (with the runnerUserInput*.txt files providing the user input).
  
### Main Menu  
The program's Main Menu\
**(? ? ?)manual (a)utojudge (l)og e(x)it (ENTER=check)?**\
has the following options
* **(? ? ?)** A choice of class period numbers which cause the program to enter manual mode and monitor that class period's folder for student program submissions.  The program processes any current (and future) program submissions to that class period's folder - oldest submission is processed first. Incorrect output differences will be shown in **diff window** after which the **Assignment Menu** is displayed.
* **(a)utojuge** Brings up the Autojudge Menu **(? ? ?)autojudge (m)ultiple (<ENTER>=all periods)?**. Specified class period folders are checked and any current (and future) program submissions are processed and automatically judged - if program output is not correct, the submission is counted as incorrect. 
* **(l)og** Program opens the global log file (logGlobal.txt in **rootDir**) in the text editor. 
* **e(x)it** Exits the program
* **ENTER** Pressing the *Enter* key causes the program to check all class periods for submissions and then returns to the Main Menu.

### Assignment Menu
In manual mode after a student's program submission has been run and either the program was correct or the program was incorrect and the **diff window** has been closed, the Assignment Menu\
**y/n/p [s d a h i o g e c m f l ls](r){x}?**\
is displayed with the following options (NOTE: Be sure that you are done with the current assignment submission before answering y n m r as this will make program proceed to the next submission)
* **y** judge the student's program as correct, update the program's status in /demo/scoreboard/, and then **move on** to the next student submission. The teacher can choose to ignore inconsequential differences in the output shown in the **diff window** and still count the program correct.
* **n** judge the student's program as incorrect, update the program's status in /demo/scoreboard/, and then **move on** to the next student submission.
* **p** judge the student's program as incorrect due to a presentation error (e.g. incorrect spacing,punctuation,capitalization), update the program's status in /demo/scoreboard/, and then **move on** to the next student submission.
* **s** show the student's program submission in the IDE.
* **d** run diff program again
* **a** run the program again
* **i** show the data input file (@.dat file in assignment folder - @ is the **assignment name**) for the assignment (newline's are shown as ↵)
* **o** print the student's output (newline's are shown as ↵)
* **g** prompt for grade and note and write to grades.txt file in student's assignment folder 
* **e** email the student with information regarding the assignment status.
* **c** copy information about the assignment status to the Clipboard (be sure to enable Windows Clipboard History). This option is provided, since emailing directly from the program may not be allowed by the school network.
* **m** move the student's program submission to the 00SAVE directory and then **move on** to the next student submission.
* **f** print a list of the files in the student's assignment directory.
* **l** opens the global log file (logGlobal.txt) in the text editor.
* **ls** opens the student's log file (log.txt) in the text editor.
* **r** remove the submission from the class period directory and then move on to the next student's submission.
* **x** exit the program.
* **h** open web browser showing this page
 
### Student Registration
To register each student submits a text file with the assignment name **registerMe**. This file must contain the student's unique student number on line 1 and email address on line 2.
 
### Sending Emails or using the Clipboard 
When sending an email or using the clipboard, you can choose to include a local (i.e. assignment specific) comment from the comments.txt file in the assignments folder or general comment from ASSIGNMENT_GROUPS/commentsLANGUAGE.txt. From the comment menu **Comment (g[#], l[#], (o)ne-time comment, (n)o comment)?** choose **g** or **l** to open the global or local comment file in the text editor.  Append a number to select one of the comments (e.g. **l2** selects **comment 2** from the local comments.txt).

### Batch Files
The latestResults directory inside the class directory will contain a batch file for each student's last submission. If the submission compiled & ran the batch file will run diff and then offer to open the IDE and input data files. If the submission did not compile or run, instead of running diff, the batch file will open the error file.
