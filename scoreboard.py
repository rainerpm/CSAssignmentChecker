import os
import glob
import subprocess
import re
from datetime import datetime
from pathlib import Path
from shutil import copyfile
import ctypes
import time
import random

# This file is imported into checkStudentPgmSubmissions.py
# It generates two scoreboard files (one with a student name and
# one with a students secret code).

def assignmentResults(listOfStudentDataFiles):
     newestStudentDataFile = ""
     correctFound = False
     points = 0
     if len(listOfStudentDataFiles) > 0:
        newestStudentDataFile = max(listOfStudentDataFiles, key=os.path.getmtime)
     if newestStudentDataFile.endswith("compileErr.txt"):
        result = "Ec"
     elif newestStudentDataFile.endswith("runErr.txt"):
        result = "Er"
     elif newestStudentDataFile.endswith("presentationErr.txt"):
        result = "Ep"
     elif newestStudentDataFile.endswith("manualCheck.txt"):
        result = "Ea"        
     else:
        count = 0
        correctFound = False
        resultChar = 'C'     
        late = False
        toolate = False
        for studentDataFile in listOfStudentDataFiles:
           if not (studentDataFile.endswith("CORRECT.txt") or studentDataFile.endswith("CORRECT_LATE.txt") or studentDataFile.endswith("CORRECT_2LATE.txt") or studentDataFile.endswith("manualCheck.txt")):
              count += 1
           if studentDataFile.endswith("CORRECT.txt") or studentDataFile.endswith("CORRECT_LATE.txt") or studentDataFile.endswith("CORRECT_2LATE.txt"):
              correctFound = True
              if not late and studentDataFile.endswith("CORRECT_LATE.txt"):
                 late = True
                 resultChar = 'L'
              if not toolate and studentDataFile.endswith("CORRECT_2LATE.txt"):
                 toolate = True
                 resultChar = 'T'              
        if correctFound:
           if count == 0:
              result = resultChar
              points = 60
           else:
              result = resultChar + str(count)
              points = 60 - (count*5)
        else:
           result = str(count) + 'x'
     return result,points,correctFound 

def updateScoreboard(scoreboardDir,contestDataDir,assignmentGroupId,classId,listOfTestNames):
   SCOREBOARD4EACHSTUDENT = False   # only use this for a contest, so that there is a scoreboard for each team
     
   footer = """
C#  = test ran successfully (was submitted incorrectly # of times)
L#  = test ran successfully (was submitted incorrectly # of times) but was LATE
T#  = test ran successfully (was submitted incorrectly # of times) but was TOO LATE for a grade.
#x  = test never ran successfully, submitted # times.
Ea  = latest submission was not 100% correct when using automatic judging (submission will be checked manually later)
Ec  = latest submission had a compile or syntax error.
Ep  = latest submission had a presentation error - e.g. incorrect spelling, missing text, spacing, capitalization, punctuation.
Er  = latest submission had a run-time error - e.g. div by 0, index out range.

The POINTS column indicates your UIL programming competition score (60 pts/problem, -5 pts for every incorrect submission)"""

     
   currentDate = datetime.now().strftime("%m-%d-%y")
   directories1 = [scoreboardDir, scoreboardDir + '/annonymous/', scoreboardDir + '/annonymous/Period' + classId,  scoreboardDir + '/annonymous/Period' + classId + '/noFooterForLiveMonitoring']
   for directory in directories1:
     if not os.path.isdir(directory):
       os.mkdir(directory)
   directories2 = [scoreboardDir, scoreboardDir + '/withNames/', scoreboardDir + '/withNames/Period' + classId,  scoreboardDir + '/withNames/Period' + classId + '/noFooterForLiveMonitoring']
   for directory in directories2:
     if not os.path.isdir(directory):
       os.mkdir(directory)   
##   if not os.path.isdir(scoreboardDir):
##      os.mkdir(scoreboardDir)
##   if not os.path.isdir(scoreboardDir + '/annonymous/'):
##      os.mkdir(scoreboardDir + '/annonymous/')
##   if not os.path.isdir(scoreboardDir + '/annonymous/'):
##      os.mkdir(scoreboardDir + '/annonymous/Period' + classId)
##      os.mkdir(scoreboardDir + '/annonymous/Period' + classId + '/noFooterForLiveMonitoring')
   scoreboardFile = scoreboardDir + '/annonymous/Period' + classId + "/" + assignmentGroupId + '.txt'
   scoreboardFileNoFooter = scoreboardDir + '/annonymous/Period' + classId + '/noFooterForLiveMonitoring' + "/" + assignmentGroupId + '.txt'
##   if not os.path.isdir(scoreboardDir + '/withNames/'):
##      os.mkdir(scoreboardDir + '/withNames/')
##      os.mkdir(scoreboardDir + '/withNames/Period' + classId)
##      os.mkdir(scoreboardDir + '/withNames/Period' + classId + '/noFooterForLiveMonitoring')
   scoreboardFileWithNames = scoreboardDir + '/withNames/Period' + classId + "/" + assignmentGroupId + '.txt'
   for includeNames in [True,False]:
      if includeNames:
        fscoreboard  = open(scoreboardFileWithNames,'w')
        spaces = 13 * ' '
      else:
        fscoreboard = open(scoreboardFile,'w')
        spaces = ' '
      fscoreboard.write(datetime.now().strftime("%c") + '  Period ' + classId + '  ' + assignmentGroupId + '\n')
      i = 0
      for testName in listOfTestNames:
         i += 1
         fscoreboard.write('(' + str(i) + ')' + testName + ' ')
      fscoreboard.write('\n\n      ' + spaces)
      j = 0

      if includeNames:
        fscoreboard.write('  CODE  TOTALS ')      
      while j < i:
         j += 1
         fscoreboard.write(f'({j:>2})')
      if includeNames:
         fscoreboard.write(' POINTS\n')
      else:
         fscoreboard.write(' TOTALS POINTS\n')
      listOfStudentDirectories = getListOfStudentDirectories(contestDataDir)
      if not includeNames:
         listOfStudentDirectories.sort(key = lambda x: int(x.split('_')[1]))  # https://stackoverflow.com/questions/31306951/how-to-sort-a-list-by-last-character-of-string
      testsCorrect = {}
      for studentDirectory in listOfStudentDirectories:
        nameCode = studentDirectory.split('_')
        name = nameCode[0]
        code  = nameCode[1]
        studentResult = ''
        correctCount = 0
        countTestsInRow = 1
        totalPoints = 0
        for test in listOfTestNames:
           listOfStudentDataFiles = glob.glob(contestDataDir + '/' + studentDirectory + '/' + test + r'_*.txt')
           result,points,correctFound = assignmentResults(listOfStudentDataFiles)
           totalPoints = totalPoints + points
           if correctFound:
              correctCount = correctCount + 1
              testsCorrect[test] = testsCorrect.get(test,0) + 1           
                           
           studentResult = studentResult + f'{result:<2s}' + '  '
           countTestsInRow += 1
        if includeNames:
           fscoreboard.write(f'{name[0:19]:20s} {code:<6s} {correctCount:>2d}     {studentResult} {totalPoints:>4d}' + '\n')
        else:
           fscoreboard.write(f'{code:<6s}  {studentResult}  {correctCount:>2d}    {totalPoints:>4d}' + '\n')

        # scoreboard file for each student/competitor
        if SCOREBOARD4EACHSTUDENT:
             if not os.path.isdir(scoreboardDir + '/Period' + classId):
                os.mkdir(scoreboardDir + '/Period' + classId)
             scoreboardFileForIndividual = scoreboardDir + '/Period' + classId + "/" + name + '_' + code + '.txt'
             fscoreboardIndividual  = open(scoreboardFileForIndividual,'w')           
             fscoreboardIndividual.write(datetime.now().strftime("%c") + '  Period ' + classId + '  ' + assignmentGroupId + '\n\n')
             i = 0
             j = 0
             for testName in listOfTestNames:
               i += 1
               fscoreboardIndividual.write('(' + str(i) + ')' + testName + ' ')
             fscoreboardIndividual.write('\n\n')  
             while j < i:
                j += 1
                fscoreboardIndividual.write(f'({j:>2})')
             fscoreboardIndividual.write(' POINTS\n')
             fscoreboardIndividual.write(f' {studentResult} {totalPoints:>4d}' + '\n')
             fscoreboardIndividual.write(footer)
             fscoreboardIndividual.close()  
      totals = ''
      sumTotals = 0
      for test in listOfTestNames:
        testCorrectStr = "   "
        if test in testsCorrect:
          testCorrectStr = str(testsCorrect[test])
          totals = f'{totals}{testCorrectStr:>2}  '
          sumTotals = sumTotals + int(testCorrectStr)
        else:
          #totals = f'{totals}  0 '
          testCorrectStr = "0"
          totals = f'{totals}{testCorrectStr:>2}  '

      if includeNames:
         fscoreboard.write('TOTALS                    ' + f'{sumTotals:>4d}' + '     ' + totals)
      else:
         fscoreboard.write('TOTALS  ' + totals + f'{sumTotals:>4d}')

      if includeNames:
         fscoreboard.write('\n' + footer)
         fscoreboard.close()
      else:   # annonymous scoreboard
         fscoreboard.close()
         copyfile(scoreboardFile,scoreboardFileNoFooter)  # the NoFooter Scoreboard is the right size for live monitoring of the score with Notepad++'s Document Monitor plugin (since the plugin scrolls to the end you can't fit the whole file on the screen if it has the footer lines)
         fscoreboard = open(scoreboardFile,'a')
         fscoreboard.write('\n' + footer)
         fscoreboard.close()         

         
def lastname(directoryName):
## 2nd capital letter
##   m = re.search(r'^([^A-Z]*[A-Z]){2}', directoryName);
##   idxOf2ndCapitalLetter = m.span()[1]

   ## last capitol letter
   res = [idx for idx in range(len(directoryName)) if directoryName[idx].isupper()]
   lastName = directoryName[:res[-1]]
   return(lastName)

def getListOfStudentDirectories(contestDataDir):
   listOfDataDirectories = [ f.name for f in os.scandir(contestDataDir) if f.is_dir() ]  # https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
   # listOfDataDirectoriesSorted = sorted(listOfDataDirectories, key=str.casefold)  # sorts case insensitvely:  https://stackoverflow.com/questions/10269701/case-insensitive-list-sorting-without-lowercasing-the-result
   #listOfDataDirectoriesSorted = sorted(listOfDataDirectories, key=lastname)  # sorts by everything up to the last capital letter, which means the lastname (unless first name has 2 capitals in it)
   listOfDataDirectoriesSorted = sorted(listOfDataDirectories)  # sorts by everything up to the last capital letter, which means the lastname (unless first name has 2 capitals in it)

   listOfStudentDirectories = []
   for dataDirectory in listOfDataDirectoriesSorted:
     if not dataDirectory.startswith('00'):
        listOfStudentDirectories.append(dataDirectory)
   return listOfStudentDirectories  # sorted alphabetically but case insensitely

def getListOfStudentNamesFromStudentDirectories(contestDataDir):
   listOfStudentNames = []
   for studentDirectory in getListOfStudentDirectories(contestDataDir):
     nameCode = studentDirectory.split('_')
     name = nameCode[0]
     code  = nameCode[1]
     listOfStudentNames.append(name)
   return listOfStudentNames


   
   
   

          


      


      

      





