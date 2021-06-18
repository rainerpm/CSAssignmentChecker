# CSAssignmentChecker

### What the program does

This program verifies python or java programs submitted by students. The program does basic verification by simply running the submitted student's .py or .java program and comparing the output of the student's program to a teacher provided expected "golden" output. If the outputs don't match, the program shows the highlighted differences. More advanced verification is possible in JAVA by enabling a student to submit multiple .java files (in a .zip file) which are then verified by a teacher provided TESTER program . The TESTER program not only enables verification of multiple classes, but also enables using techniques like JAVA reflection to inspect student's code (e.g. demo\ASSIGNMENT_GROUPS\first6weeksAssignments\Collatz\CollatzTester.java).

### Required Python packages
  * pip install pyperclip
  
### Other Requirements
  * download & install tkdiff (https://sourceforge.net/projects/tkdiff/)

### Demo
* unzip demo.zip to a folder on your hard drive (i.e. C:/YourPathToDemoDir/demo)
  * ASSIGNMENT_GROUPS folder
    * assignment Group folders
        * assignment folders (the name of the assignment folder **is** the **assignment name**)
           * gold.txt  (the teacher provided golden output for the program)
           * ????Tester.java, where ???? is the **assignment name**
    * periods.txt (indicates which class periods are doing this assignment Group)
    * comments.txt  (global comments)
  * 1,4,5 a folder for each class period
* set the following directory variables
  * set the **rootDir** variable to the location of the unzipped demo folder - C:/YourPathToDemoDir/demo (hereafter abbreviated /demo)
  * set the **scoreboardDir** variable to /demo/scoreboard
* set the following executable variables
  * set the **tkdiffLoc** variable to the location of the **tkdiff.exe** executable.
  * set the **pythonIdeLoc** variable to the location of the Python IDE (e.g. IDLE) executable.
  * set the **javaIdeLoc** variable to the location of the JAVA IDE (e.g. jGrasp) executable.
* run CSassignmentChecker.py
  * since this is the first the program has been run, the program creates some required directories.
  * You should now see the main menu\
    **(1 4 5) manual (a)utojudge (l)og e(x)it (<ENTER>=check)?**\
  **Answer 4** to have the program enter the manual mode for class period 4. For now the program continually checks for new submissions to the class period folder /demo/4/. 
  When there is no submission to process, the program will print a period every 2 seconds to let you know it is alive. Leave the program running (and printing periods) for now.
* A student interacts with this program by submitting a file to a class period folder.
  The file name submitted must be named\
    **#LastFirst?_@.$**\
  where # is the student's class period, ? is a student number, @ is the assignment name (or "register"), $ is the file extension: py, java, or zip.
  * Ideally students students have a way to "submit" a file directly to a class period folder on the teacher's hard drive in real time.
  This can be achieved by having students submit to an online folder that is automatically synched to the teacher's PC using 
  something like the Dropbox File Request feature.
* For this demo, instead of students submitting files to the class period folder, **we will simply copy example files from demo/sampleSubmissions/*
* To demo the basic verification of a student program, copy /demo/sampleSubmissions/studentProblems/4ShotwellGwynne4381_encryption.py to the class period 4 folder /demo/4/. The program will detect this file and run the program. Since the student program works as expected the program reports *** CORRECT ***.  
   * This particular student program when run with the teacher supplied input file /demo/ASSIGNMENT_GROUPS/pythonAssignments/encryption/encryption.dat is expected to print out exactly what's found in /demo/ASSIGNMENT_GROUPS/pythonAssignments/encryption/gold.txt. 
* prints the assignment menu.
    **y/n \[i a o c e s f l](r){x} h=help?**
* Each student should be registered with the program. To register two example students copy the two files in demo/sampleSubmissions/studentRegistrations/ to /demo/1/ 
  (NOTE: That for registration purposes the assignment name part of the file name must be the word "register").
  The program, which was still printing periods, detects these files in demo/1/ and registers the students by creating/updating a file called REGISTER.txt and then deletes the files.
  For the demo the directories /demo/5/ and /demo/6/ already have predefined registrations in a REGISTER.txt file.
* To demo the more advanced verification of a JAVA program using a teacher provided TESTER program, copy demo/sampleSubmissions/studentProblems/1LovelaceAda1234_Collatz.java to  to the class period 1 folder /demo/1/.
  This represents the student's code for an assignment named "Collatz". assignment collatz and compares it to the expected output stored in the test's gold.txt file
  (/demo/ASSIGNMENT_GROUPS/first6weeksAssignments/collatz/gold.txt). In this case the program will report *** CORRECT *** and
 
  Here
  
* To associate an email address with a student manually edit the demo/1/REGISTER.txt file and enter
  a student email as a 4th field for the student.
