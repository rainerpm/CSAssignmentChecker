# CSAssignmentChecker

### What the program does

This program verifies student submitted python or java programs. The program does basic verification by simply running the submitted student's .py or .java program and comparing the program's printed output to a teacher supplied expected "gold" output file. If the two don't match, the program shows the highlighted differences. More advanced verification is possible in JAVA by enabling a student to submit a single  .java file or multiple .java files (in a .zip file) which are then verified by a teacher provided TESTER program. The TESTER program enables verification of multiple classes as well as sing techniques like JAVA reflection to inspect student's code (see Collatz in Demo below).

### Required Python packages
  * pip install pyperclip
  
### Other Requirements
  * download & install tkdiff (https://sourceforge.net/projects/tkdiff/)

### Demo Setup
* unzip demo.zip to a folder on your hard drive (i.e. C:/YourPathToDemoDir/demo)
  * ASSIGNMENT_GROUPS folder
    * assignment group folders
        * assignment folders  - the name of the assignment folder **is** the **assignment name** (assignment names must be unique)
           * gold.txt  (the teacher provided golden output for the program)
           * ?Tester.java, where ? is the **assignment name** 
    * periods.txt (indicates which class periods are doing this assignment Group)
    * comments.txt  (global comments - used in student emails or clipboard)
  * 1,4,5 class period folders for the demo
* set the following folder (aka directory) variables
  * set the **rootDir** variable to the location of the unzipped demo folder - C:/YourPathToDemoDir/demo 
  * set the **scoreboardDir** variable to C:/YourPathToDemoDir/demo/scoreboard
  * hereafter C:/YourPathToDemoDir/demo is abbreviated /demo.
* set the following executable variables
  * set the **tkdiffLoc** variable to the location of the **tkdiff.exe** executable.
  * set the **pythonIdeLoc** variable to the location of the Python IDE (e.g. IDLE) executable.
  * set the **javaIdeLoc** variable to the location of the JAVA IDE (e.g. jGrasp) executable.
### Run the Demo
* run CSassignmentChecker.py
  * since this is the first time the program has been run, the program creates some required directories.
  * You should now see the Main Menu\
    **(1 4 5) manual (a)utojudge (l)og e(x)it (ENTER=check)?**\
  **Answer 4** to have the program enter the manual mode for class period 4. In this mode, the program continually checks for new submissions to the class period folder /demo/4/. The program creates the directories for the two students have been registered with this class period.
  When there is no submission to process, the program will print a period every 2 seconds to let you know it is alive. Leave the program running (and printing periods) for now.
* A student interacts with this program by submitting a file to a class period folder.
  The file name submitted must be named\
    **#LastFirst?_@.$**\
  where # is the student's class period, ? is a student number, @ is the assignment name (or "register"), $ is the file extension: py, java, or zip.
  * Ideally students students have a way to submit a file directly to a class period folder on the teacher's hard drive in real time.
  This can be achieved by having students submit to an online folder that is automatically synched to the teacher's PC using 
  something like the Dropbox File Request feature.
* For this demo, instead of students submitting files to the class period folder, *we will simply copy example files from /demo/sampleSubmissions/*
* To demo the basic verification of a student program, copy /demo/sampleSubmissions/studentProblems/4ShotwellGwynne4381_encryption.py to the class period 4 folder /demo/4/. This file is Period 4's student Gwynne Shotwell's submission of the encryption assignment. The program (which up to now had been printing periods) will detect this file and run the program. 
   * Since this initial student program has an error, the program will use tkdiff to display the differences between the students program output and the expected "gold" output.
   * After you close the tkdiff window, the program displays the Assignment Menu **y/n \[i a o e c s f l](r){x} h=help?**
     * **Answer i** to display the program in the Python IDE.
     * **Answer n** to judge the program as incorrect. The student's program status is reflected in /demo/scoreboard/ (one file with the student's name and one that is annoymized using the student's 4 digit code that can be made accessible to the class).
   * Since the output was incorrect, the program also created a file (ShotwellGwynne_tkdiff.bat) in the class period folder that enables the teacher to easily run tkdiff for the student's last incorrect submission.
   * copy /demo/sampleSubmissions/studentProblems/4ShotwellGwynne4381_encryption.py to the class period 4 folder /demo/4/ but now fix the error line 21 (changing thing[1] to thing[0])
    * Since the student now program works as expected the program reports *** CORRECT ***. NOTE: The program ignores any whitespace at the end of a line or the end of the output when comparing the student's output to the expected output in the assignment's gold.txt file.
     * **Answer y** to judge the program as correct and update the program's status in /demo/scoreboard/.
   * NOTE: This particular student program when run with the teacher supplied input file /demo/ASSIGNMENT_GROUPS/pythonAssignments/encryption/encryption.dat is expected to print out exactly what's found in /demo/ASSIGNMENT_GROUPS/pythonAssignments/encryption/gold.txt. 
* The program should now be in the mode of continually checking for new submissions to the class period folder /demo/4/. 
  * Use Ctrl-C to go back to the Main Menu.
* Each student should be registered with the program. To register two example students copy the two files in demo/sampleSubmissions/studentRegistrations/ to /demo/1/ 
  (NOTE: For registration purposes the assignment name part of the file name must be the word "register").
  **Answer 1** in the Main Menu.  The program detects the registration files in /demo/1/ and registers the 2 students by creating/updating a file called REGISTER.txt (and then deleting the files).
  For the demo the directories /demo/5/ and /demo/6/ already had predefined student registrations in a REGISTER.txt file.
* To demo the more advanced verification of a JAVA program using a teacher provided TESTER program, copy the student program /demo/sampleSubmissions/studentProblems/1LovelaceAda1234_Collatz.java to the class period 1 folder /demo/1/.
  This represents the student's code for an assignment named "Collatz". In addition to the expected output file gold.txt, the teacher has also supplied a specific test program called CollatzTester.java in the folder /demo/ASSIGNMENT_GROUPS/first6weeksAssignments/collatz/. The program runs the CollatzTester program and should report *** CORRECT *** since the program's output matches the expected output.
  
### Main Menu  
The program's Main Menu\
**(? ? ?) manual (a)utojudge (l)og e(x)it (ENTER=check)?**\
has the following options
* **(? ? ?)** A choice of class period numbers which cause the program to enter manual mode and monitor that class period's folder.  The program processes any current (and future) program submissions to that class period's folder - oldest submission is processed first. Incorrect output differences will be shown in **tkdiff** after which the **Assignment Menu** is displayed.
* **(a)utojuge** Checks all class period folders and will process any current (and future) program submissions. If program output is not correct, the submission is counted as incorrect. The Assignment Menu is not displayed.
* **(l)og** Program displays the last 20 lines of logGlobal.txt in **rootDir** 
* **e(x)it** Exits the program
* **ENTER** Pressing the *Enter* key causes the program to check all class periods for submissions and then returns to the Main Menu.

### Assignment Menu
In manual mode after a student's program submission has been run and either the program was correct or the program was incorrect and the **tkdiff** window has been closed, the Assignment Menu\
**y/n \[i a o e c s f l](r){x} h=help?**\
is displayed with the following options
* **y** judge the student's program as correct and update the program's status in /demo/scoreboard/. The teacher can choose to ignore inconsequential differences in the output shown in the **tkdiff** window and still count the program correct.
* **n** judge the student's program as incorrect and update the program's status in /demo/scoreboard/.
* **i** show the student's program submission in the IDE.
* **a** run the program again
* **o** print the student's output (newline's are shown as ↵)
* **e** email the student with information regarding the assignment status.
* **c** copy information about the assignment status to the Clipboard (requires Windows 10’s October 2018 Update which provided a Clipboard History enabling multiple items to be saved on the clipboard). This option is provided, since emailing directly from the program may not be allowed by the school network.
* **s** save the student's program submission and removes it from the class period directory (enabling the program to process the next submission).
* **f** print a list of the files that are in the student's assignment directory.
* **l** print the last 20 lines of the logGlobal.txt file.
* **r** remove the program from the class period directory (enabling the program to process the next submission).
* **x** exit the program.
* **h** print out help on the Assignment Menu options
 
### Sending Emails or using the Clipboard 
* To associate an email address with a student manually edit the REGISTER.txt file in the class period folder and enter a student email as a 4th field for the student.
* The program will give you options to use a saved set of comments or enter a new comment to be used in the mail or put on the clipboard. You can chooose from preset assignment specific comments (stored in the comments.txt file in the assignments folder) or global comments (stored in ASSIGNMENT_GROUPS/comments.txt)

