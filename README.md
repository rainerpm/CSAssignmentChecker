# CSAC - Computer Science Assignment Checker

### Overview

The **CSAC.py** program verifies python or java assignments submitted by students. **CSAC** supports basic verification for Python programs and more advanced verification for JAVA programs. Student assignments are organized into assignment groups, each of which has a *scoreboard* file showing the results of all the students in a class. [Demo video](https://youtu.be/nl750S_3hOY).

### Requirements
The **CSAC.py** requires several packages to be available. Make sure these packages are installed for your IDE. Like my students, I use [Thonny](https://thonny.org/). To install these packages in Thonny use **Tools → Open system shell to** and run the following  
* pip install numpy
* pip install pywin32
  * only required if you want to use the option to email students directly from the program by having the program use the Windows Outlook app
* pip install pyperclip (enables the program to access the clipboard)
  * only required for providing a student feedback comment via email or the clipboard
* pip install pillow (enables the program to "grab" an image from the most recent clipboard entry)
  * only required for providing a student feeback comment via email or the clipboard

The following programs are required to be installed on your computer. The programs in parenthesis are what I use, but can be replaced with something equivalent by updating the variables at the top of the **CSACcustomize.py** file. NOTE: A 2nd Python IDE is used by **CSAC** to enable the student program to be viewed and run separately from the **CSAC** program itself.
* Python IDE (https://www.python.org/downloads/)
* JAVA IDE (https://www.jgrasp.org/)
* Text Editor (https://notepad-plus-plus.org/downloads/)
* diff program (https://winmerge.org/?lang=en).
 
### Program (and Demo) Setup
* unzip **demo.zip** to a folder on your hard drive (e.g. C:/Users/*YourUserName*/Downloads)
* in **CSACcustomize.py**
  * replace all occurences of *YourUserName* with your user name 
  * set the **pythonIdeLoc** variable to the location of the Python IDE (e.g. IDLE) executable.
  * set the **javaIdeLoc** variable to the location of the JAVA IDE (e.g. jGrasp) executable.
    * NOTE: The program uses *-parameters* compile option to ensure that JAVA reflection reflects parameter types instead of just using arg0
  * set the **textEditorLoc** variable to the location of a text editor (e.g. Notepad++) executable.
  * set the **diffLoc** variable to the location of the diff program (e.g. winMerge) executable.
* in **CSACgradesData.py**
  * replace all occurences of *YourUserName* with your user name  
* you are now ready to run the demo - see the Running the Demo section below.
* if you look inside the demo folder you will find
  * **CSAC.py** the CSAC program
  * **CSACcustomize.py** file that customizes CSAC for your setup. 
  * **CSACscoreboard.py** generates the scoreboard (aka student results) output.
  * **CSACgrades.py** Run separately to generate grades for assignments (reds in the assignment grading information from **CSACgradesData.py**)
  * **CSACcheat.py** Run separately to detect similarities between programs submitted to **CSAC**.
  * **ASSIGNMENT_GROUPS** folder
    * **first6weeksAssignments, pythonAssignments** (these folders contain a group of related assignments, each of which will have it's own scoreboard file)
      * **GCD, encryption** (these are two of the assignment folders  - the name of the assignment folder **is** the **assignment name**, assignment names must be unique, @ = **assignment name**)
         * **@.dat** is the teacher provided input data file for the assignment. Typically this file contains more/harder test data then what's been given to the students.
         * **@Tester.java** an optional test program (@ is the **assignment name**)
         * **@Checker.java** an optional checker program (@ is the **assignment name**)
         * **pgmUserInput&.txt** user input files if the student's program requires user input - e.g. Python: input() JAVA: scan.nextInt() 
         * **runnerUserInput&.txt** user input files if the student also submits **@Runner.java** file
         * **gold.txt** the teacher provided expected (aka golden) output for the assignment
         * **find.txt** [OPTIONAL] the teacher provided file that contains text that is searched for in the student's submission.
         * **findGold.txt** [OPTIONAL] the teacher provided file that contains the expected (aka golden) output for the searches specified in **find.txt**
         * **checker.txt** the teacher provided checker output for the assignment
         * **comments.txt** contains the assignment specific comments used in student emails or clipboard
         * **timeout.txt** contains the amount of seconds the test should be given before timing out (optional: overrides the TIMEOUT_DEFAULT set in CSACcustomize.py)
         * **solutions** optional folder that contains possible solutions for the problem (CSACcheat.py will compare these files to all the students submissions). See **Detecting Cheating** section below for more information.
    * **commentsJAVA.txt** and **commentsPYTHON.txt** contain the global comments used in student emails or clipboard
  * **P1,P4,P5** (these are the class period folders to which student assignment files are either explicitly copied by the teacher or directly submitted  via something like [a Google Form](https://docs.google.com/document/d/1-4K8yRds6PuprkSgZoZCg_ll3ykIpoFIFzKsf9gEwNE/edit?usp=sharing) or [a Dropbox File Request](https://fileinbox.com/articles/dropbox-file-requests-ultimate-guide#:~:text=Unfortunately%2C%20Dropbox%20File%20Requests%20don,to%20create%20a%20Dropbox%20account.](https://docs.google.com/document/d/1R93KHIYiwyKRqjzm3_vxHb4VJ6b_4BD-f0hwP55qVKw/edit?usp=drive_link)) by the students. Inside each folder you will find the REGISTER.txt file containing the students registered to this class (for each student: a unique ID, last name, first name, class period, email address). Also in this folder is a folder for each assignment group that contains folders for each of the students which contain folders for the student's program submissions. 
  * **sampleSubmissions** Two example student submissions.
  * **dueDates.txt** Optional file that contains the due date followed by 1 or more assignment names.
  * **scoreboard_for_demo** This folder will contain the results for the student's assignments.
  * **emailAttachmentDir** This folder temporarily stores the email attachment that is screen captured when running CSAC.
  
### Running the Demo
The demo verifies two student assignments (1) [encryption](https://docs.google.com/document/d/1mr5FHL-cf3T1kRR0F10KCWwGGdjZC4Cj/edit?usp=sharing&ouid=117088614197672338242&rtpof=true&sd=true) (2) [GCD](https://docs.google.com/document/d/14nIXTUOr70_zRUZojzMZhbs9AmTWs5WxatsVtjNT_c4/edit?usp=sharing). Follow the below steps and/or watch the demo video (NOTE: CSAC & the demo has changed slightly since the video was made): [download](https://drive.google.com/file/d/1o7TA-ym4WC4xezXcMf3mqvpzbMRN7Awm/view?usp=sharing) or [YouTube](https://youtu.be/Nr0t-hp050Y) 
* run **CSAC.py**  
  * since this is the first time the program has been run, the program creates some required directories.
  * You should now see the Main Menu\
    **(1 4 5)judge (a)utojudge score(b)oard (l)og e(x)it (\<ENTER\>=check)?**\
  The 3 numbers in the parenthesis are the "shortcut" names provided in the python list classPeriodNamesForMenu in the CSACcustomize.py file.
  **Answer 4** to have the program enter the judging mode for class period 4. In this mode, the program continually checks for new submissions to the class period folder **/demo/P4/**.
  Since there is currently no submission to process, the program prints a period every 2 seconds to indicate that it is waiting for submissions.
* For this demo, instead of students submitting files directly to the teacher's class period folder via something like [a Google Form](https://docs.google.com/document/d/1R93KHIYiwyKRqjzm3_vxHb4VJ6b_4BD-f0hwP55qVKw/edit?usp=sharing) or [a Dropbox File Request](https://fileinbox.com/articles/dropbox-file-requests-ultimate-guide#:~:text=Unfortunately%2C%20Dropbox%20File%20Requests%20don,to%20create%20a%20Dropbox%20account.](https://docs.google.com/document/d/1R93KHIYiwyKRqjzm3_vxHb4VJ6b_4BD-f0hwP55qVKw/edit?usp=drive_link)), *we will simply copy example files from /demo/sampleSubmissions/*.
* To demo the basic verification of a student program, copy **/demo/sampleSubmissions/Shotwell Gwynne 112233_encryption.py** to the class period 4 folder **/demo/P4/**. This file is Period 4's student Gwynne Shotwell's (student secret code 112233) submission of the encryption assignment. CSAC (which up to now had been printing periods to indicate its waiting for submissions) will detect this file and run the student's program. 
   * This student's program output does not match the expected "gold" output, and thus **CSAC** will use the diff program to display the differences between the student's program output and the expected "gold" output in the **gold.txt** file.
   * After you've had a chance to look at the difference, close the diff window. The program now displays the Assignment Menu **y/late/2late/n/p [s d a b h i o g e c m f k t ?](r){x}(#)**
     * **Answer s** to show/see the program in the Python IDE. After you've run and/or inspected the program, close the IDE.
     * **Answer n** to judge the program as incorrect. The student's program status is reflected in the scoreboard (one file with the student's name and one that is annoymized using the student's code that can be made accessible to the class). The result is reflected in the scoreboard file for that assignment group which is somwhat buried in the **C:/Users/YourUserName/Downloads/demo/scoreboard_for_demo/** folder.
   * Since the output was incorrect, the program also created a file (ShotwellGwynne.bat) in the latestResults folder inside the class period folder that enables the teacher to easily run diff program for the student's last incorrect submission and optionally bring up the program in the IDE or look at the data input file in the text editor.
   * Edit **/demo/sampleSubmissions/Shotwell Gwynne 112233_encryption.py** and fix the error on line 21 (changing thing[1] to thing[0]) and then once again copy the file to the class period 4 folder **/demo/P4/**. 
    * Since the student's program output matches the assignments gold.txt file the program reports *** CORRECT ***. NOTE: The program ignores any whitespace at the end of a line or the end of the output when comparing the student's output to the expected output in the assignment's gold.txt file.
     * **Answer y** to judge the program as correct and update the program's status in the scoreboard.
   * NOTE: This particular student program when run with the teacher supplied input file **/demo/ASSIGNMENT_GROUPS/pythonAssignments/encryption/encryption.dat** is expected to print out exactly what's found in **/demo/ASSIGNMENT_GROUPS/pythonAssignments/encryption/gold.txt**. 
  * The program is once again in the mode of continually checking for new submissions to the class period folder **/demo/P4/**. Use Ctrl-C to go back to the Main Menu (this works in Python Idle, but not in Thonny). If Ctrl-C does not work in your IDE, simply restart **CSAC** to switch class periods.
* To demo the more advanced verification of a JAVA program, **answer 1** in the Main Menu, so that **CSAC** is now awaiting program submissions in the **/demo/P1/** folder. Then copy the student program **/demo/sampleSubmissions/Lovelace Ada 123456 - GCD.zip** to the **/demo/P1/** folder.
  This represents the student's code for an assignment named "GCD" ([Greatest Common Divisor](https://docs.google.com/document/d/14nIXTUOr70_zRUZojzMZhbs9AmTWs5WxatsVtjNT_c4/edit?usp=sharing)). For this assignment the students submit **GCD.java** and  **GCDRunner.java**. in the folder **/demo/ASSIGNMENT_GROUPS/first6weeksAssignments/GCD/**, the teacher has provided a checker program called **GCDChecker.java**, a testing program called **GCDTester.java**, the expected output files **checker.txt** and **gold.txt**, as well as **runnerUserInput&.txt** files to provide user input to **GCDRunner.java**.
  * CSAC runs the **GCDChecker.java** program and reports >>> CHECK CORRECT <<< since the programs output matches the expected output in **checker.txt**. This means that the student's **GCD.java** program contains all the correct instance variables and method signatures.
  * CSAC runs the **GCDTester.java** program and reports *** RUN CORRECT *** since the program's output matches the expected output in gold.txt. This means the student's **GCD.java** and **GCDRunner.java** produce the expected output to the teacher's testing stimulus.
  * Selecting **d** in the assignment menu shows the program and expected output in the diff program. This is the output from the runs of **GCDTester.java** and **GCDRunner.java** (with the **runnerUserInput&.txt** files providing the user input). Since everything in the student's code is correct there will be no differences.
* The teacher would now answer y to judge the program as correct.
* Run **CSACgrades.py** to create a grading file in the **Grades4Gradebook** directory. When prompted select **4** as the class period and then **1** to generate a file for the **python encrypt** grade.
* Run **CSACcheat.py** then select **2** when prompted to select an assignment. If you want to try out **compare50** or **moss** see how to set things up in the **Detecting Cheating** section below.

### Student Registration
Students are registered with **CSAC** via a REGISTER.txt file in each class period folder. Each line in the REGISTER.txt file contains 6 pieces of information for each student (each separated by one or more spaces) (1) secret code - used to annonymously identify a student's results (2) first name (3) last name (4) class period (5) email address (6) school student id (**CSAC** currently does not support spaces in student's first or last names). You can create the REGISTER.txt file manually, or use a [Google Form](https://docs.google.com/document/d/1BaU-_KyqOs55-iTgqofZ8XuDYRqWC9_9-3l_4Etynp0/edit?usp=sharing).  

### Assignment Submission
To submit an assignment a student submits a single file using the naming convention **Last First ?_@.$** (where **Last** = student's last name, **First** = student's first name,  **?** = student secret code, **@** = assignment name, **$** = file extension: either py, java for individual files or zip for multiple files). For JAVA, the class in the **Last First ?_@.$** file must be named **@**.  An example of a valid filename is **Shotwell Gwynne 112233_encryption.py**.

The student's assignment files can be explicitly copied by the teacher to the class period folder on the teacher's PC or 
can be submitted directly to that folder in real time by the students (one way to do this is to have the students submit to an online folder that is automatically synched to the teacher's PC - e.g. [using a Google Form](https://docs.google.com/document/d/1R93KHIYiwyKRqjzm3_vxHb4VJ6b_4BD-f0hwP55qVKw/edit?usp=sharing) or [using a Dropbox File Request](https://fileinbox.com/articles/dropbox-file-requests-ultimate-guide#:~:text=Unfortunately%2C%20Dropbox%20File%20Requests%20don,to%20create%20a%20Dropbox%20account.](https://docs.google.com/document/d/1R93KHIYiwyKRqjzm3_vxHb4VJ6b_4BD-f0hwP55qVKw/edit?usp=drive_link))).

### Assignment  Verification
* **Basic Verification.**  For a Python or JAVA program that simply prints its output, **CSAC** runs the student's program and compares the program's generated output to a teacher provided "golden" output file named **gold.txt**.
  * The student's program may optionally read test input data from a file named **@.dat** (as part of an assignment, student's are usually provided a **@.dat** file with a few basic test cases; typically a teacher will provide **CSAC** a **@.dat** file with more comprehensive test cases).
  * The student's program may optionally prompt the user for input - e.g. Python: input() JAVA: scan.nextInt().  To provide this user input, the teacher provides **CSAC** with one or more **pgmUserInput&.txt** files (& is a unique identifier, usually 1,2,3, ...) - **CSAC** runs the submitted program once for each user input file.
  * [OPTIONAL] The teacher may provide a **find.txt** file that specifies text to search for in the student's submission which CSAC then compares to the expected results in the **findGold.txt** file. Each line in **find.txt** specifies the name of a function/method and the text to search for in that function/method.  To search anywhere in the program submission use "canBeAnywhere" in place of the function/method name.  Or to search code that is outside any functions in Python use "outsideAFunction".  For example, this enables the teacher to see if the student did (or did not) use a print statment inside a function (instead of returning the value) or a while loop instead of a for loop.

* **Advanced Verification (JAVA only).** **CSAC** does the **Basic Verification** above and then runs these OPTIONAL programs 
  * **@Checker.java**  [provided by teacher] Code provided by the teacher to check the contents of the student's program (number and type of instance variables as well as details on the constructors and methods in the student's program). The output is compared to the **checker.txt** file provided by the teacher.
  * **@Tester.java**  [provided by teacher] Code provided by the teacher that tests the program submitted by the student. The output is compared to the  **gold.txt** output file provided by the teacher.
  * **@Runner.java**  [submitted by students] Code that the student wrote that uses the class(es) they wrote. The output is compared to the  **gold.txt** output file provided by the teacher. The **@Runner.java** program can optionally prompt the user for input. To provide this user input to **CSAC**, the teacher provides one or more **runnerUserInput&.txt** files (& is a unique identifier, usually 1,2,3, ...). The **@Runner.java** program will be run once for each user input file.  The output is compared to the **gold.txt** output file provided by the teacher. If both **@Tester.java** and **@Runner.java** are used for an assignment, **CSAC** runs **@Tester.java** first and thus its output should appear first in the **gold.txt** file.
  
### Main Menu  
The program's Main Menu\
**(? ? ?)judge (a)utojudge score(b)oard (l)og e(x)it (\<ENTER\>=check)?**\
has the following options
* **(? ? ?)** A choice of class period numbers which cause the program to enter judging mode. **CSAC** now processes program submissions to that class period folder - the oldest submission is processed first. A **diff window** will show any difference between the program's output and the expected output. Then **Assignment Menu** is displayed.
* **(a)utojuge** Brings up the Autojudge Menu **(? ? ?)autojudge (m)ultiple (\<ENTER\>=all periods)?**. Specified class period folders are checked and any current (and future) program submissions are processed and automatically judged - if program output is not correct, the submission is counted as incorrect. 
* **(l)og** Program opens the global log file (logGlobal.txt in **rootDir**) in the text editor. 
* **e(x)it** Exits the program
* **ENTER** Pressing the *Enter* key causes the program to check all class periods for submissions and then returns to the Main Menu.

### Assignment Menu
In manual mode after a student's program submission has been run and either the program was correct or the program was incorrect and the **diff window** has been closed, the Assignment Menu\
**y/late/2late/n/p [s d a b h i o g e c m f k t ?](r){x}(#) days1:days2**\
is displayed with the following options (NOTE: Be sure that you are done with the current assignment submission before answering y n m r as this will make program proceed to the next submission)
* **y** judge the student's program as correct, update the program's status in the scoreboard, and then **move on** to the next student submission. The teacher can choose to ignore inconsequential differences in the output shown in the **diff window** and still count the program correct.
* **late** same as y above, but submission is marked as being LATE in the scoreboard
* **2late** same as y above, but submission is marked as being Too LATE in the scoreboard
* **n** judge the student's program as incorrect, update the program's status in the scoreboard, and then **move on** to the next student submission.
* **p** judge the student's program as incorrect due to a presentation error (e.g. incorrect spacing,punctuation,capitalization), update the program's status in the scoreboard, and then **move on** to the next student submission.
* **s** show the student's program submission in the IDE.
* **d** run diff program again
* **a** run the program again (runs all the checks again, retaining any edits that may have been made in the directory where the student program is run).
* **b** bring up file explorer in the scoreboard directory.
* **h** open web browser showing this page
* **i** open the data input file for the assignment in the text editor
* **o** open the student's stdout in the text editor
* **g** opens grades.txt file in student's assignment folder using the text editor.
* **e** email the student with information regarding the assignment status.
* **c** copy information about the assignment status to the Clipboard (be sure to enable Windows Clipboard History). This option is provided, since emailing directly from the program may not be allowed by the school network.
* **m** move the student's program submission to the 00MANUAL directory (so it may be run manually later) and then **move on** to the next student submission.
* **f** opens Windows file explorer in the student's assignment directory.
* **k** kill any open texteditor, IDE, or diff processes (does not work on file explorer - couldn't figure out why).
* **t** set the timestamp of the current file to NOW (so program will process all other currently pending submissions before this one)
* **w** set the timestamp of the submission to NOW (this will make the file the lowest priority of the submitted files in the queue and thus run after all the others).
* **r** remove the submission from the class period directory and then move on to the next student's submission.
* **x** exit the program.
* **#** number of submissions currently waiting to be run
* **days1** number of school days until due date (negative is before the due date, positive is after). Program implements my current [Due Dates](https://docs.google.com/document/d/1FsaO3KNpjzn3G6qckAgyCPEAJk7UymidAZuEi5ZzSjs/edit#heading=h.ltopyeuk8xw6) policy.
* **days2** number of calendar days until due date (negative is before the due date, positive is after) 

### Scoreboard
Student results for each assignment group are stored in two scoreboard files (one using the student's name, the other using the student's secret code for anonymity). The teacher can share the link to the scoreboard file to allow students to see the results. Sometimes I use Notepad++ to project the live scoreboard (see https://www.raymond.cc/blog/monitor-log-or-text-file-changes-in-real-time-with-notepad/ on how to make Notepad++ display live results).

### Assignment Groups
An assignment group is simply a grouping of assignments that use one scoreboard. The currently active assignment groups are listed in the javaAssignmentGroups and pythonAssignmentGroups dictionaries in the **CSACcustomize.py** file. 

### Sending Emails or using the Clipboard 
**CSAC** currently uses the Windows Outlook app (see **emailWithOutlook** function) to email students. I've also used to use the Outlook web app (see **emailWithOutlookSMTP()** function) successfully from home, but our school district blocked that functionality on the school network.  The **emailWithGmail()** function is also provided but has not been tested much. The information content of a **CSAC** email can also be accessed via the Windows clipboard (Windows 10 and Windows 11 have a [“Clipboard History” tool](https://www.popsci.com/diy/windows-clipboard-manager/) that allows the Clipboard to store multiple items). When sending an email or using the clipboard, you can choose to include a local (i.e. assignment specific) comment from the **comments.txt** file in the assignment's folder or a general comment from **ASSIGNMENT_GROUPS/commentsLANGUAGE.txt**. From the comment menu **Comment (g[#], l[#], (o)ne-time comment, (n)o comment)?** choose **g** or **l** to open the global or local comment file in the text editor. Appending the comment name to the **g** selects the named comment from the global comments file in the ASSIGNMENT_GROUPS directory (e.g. **gabc** selects **comment abc**). Similarly **lxyz** selects **comment xyz** from the local comments file in the assignment's folder.  
 
### Group submission
A group of 2 or more students can submit an assignment to **CSAC**. For example three students can submit an assignment by submitting a file named **Last1+Last2+Last3 First1+First2+First3 ?1+?2+?3_@.$** (where **Last1** **Last2** **Last3** are their last names, **First1** **First2** **First3** are their first names,  **?1**  **?2**  **?3** are their unique student numbers, **@** assignment name, **$** file extension: either py, java for individual files, or zip for multiple files).  For example, you can use the same Google Form you do for an individual student submission to also have a [group submit](https://docs.google.com/document/d/1WkCn_ozAQ22LSrUmLF2GLAzSpkTZwYIU6qMJVUXpM18/edit?usp=sharing).

### Grading
The **CSACgrades.py** program generates a file of grades that can be imported into your gradebook. Grading information is contained in the **CSACgradesData.py** file (see example in demo).  Multiple assignments can be combined into a single grade in a variety of ways.

### Detecting Cheating
[PYTHON only for now] The **CSACcheat.py** program makes it easy to check for similarities among files submitted to CSAC. The program can use compare50 or moss for similarity checking. The program can also search the submitted files for a provided regular expressions and analyse frequency of variable names. For compare50 & moss the program will submit all files that were judged to be correct and are thus in the assignment's **00PLAGIARISM** folder as well as any files that are in the assignment's **solutions** folder (where you can put common/online solutions that you suspect students may be copying from).  **CSACcheat.py** assumes you've set up [compare50](https://cs50.readthedocs.io/projects/compare50/en/latest/) to run in the Windows Subsystem for Linux (wsl) and/or that you have replaced 11111111 in the **CSAClogin.txt** with your [moss](https://theory.stanford.edu/~aiken/moss/) userid.

### Batch Files
The **latestResults** directory inside the class directory will contain a batch file for each student's last submission. If the submission compiled & ran the batch file will run diff and then offer to open the IDE and input data files. If the submission did not compile or run, instead of running diff, the batch file will open the error file.
 
