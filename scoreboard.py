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
     else:
        count = 0
        correctFound = False
        for studentDataFile in listOfStudentDataFiles:
           if not studentDataFile.endswith("CORRECT.txt"):
              count += 1
           else:
              correctFound = True
        if correctFound:
           if count == 0:
              result = "C"
              points = 60
           else:
              result = "C" + str(count)
              points = 60 - (count*5)
        else:
           result = str(count) + 'x'
     return result,points,correctFound 

def updateScoreboard(scoreboardDir,contestDataDir,assignmentGroupId,classId,listOfTestNames):
   currentDate = datetime.now().strftime("%m-%d-%y")
   if not os.path.isdir(scoreboardDir + '/annonymous/'):
      os.mkdir(scoreboardDir + '/annonymous/')
   scoreboardFile = scoreboardDir + '/annonymous/' + 'Period' + classId + "_" + assignmentGroupId + '.txt'
   if not os.path.isdir(scoreboardDir + '/withNames/'):
      os.mkdir(scoreboardDir + '/withNames/')
   scoreboardFileWithNames = scoreboardDir + '/withNames/' + 'Period' + classId + "_" + assignmentGroupId + '.txt'
   for includeNames in [True,False]:
      if includeNames:
        fscoreboard  = open(scoreboardFileWithNames,'w')
        spaces = 13 * ' '
      else:
        fscoreboard = open(scoreboardFile,'w')
        spaces = ' '
      fscoreboard.write(datetime.now().strftime("%c") + '  Period ' + classId + '  ' + assignmentGroupId)
      fscoreboard.write('\n')
      i = 0
      for testName in listOfTestNames:
         i += 1
         fscoreboard.write('(' + str(i) + ')' + testName + ' ')
      fscoreboard.write('\n\n      ' + spaces)
      j = 0

      if includeNames:
        fscoreboard.write('TOTALS Code  ')      
      while j < i:
         j += 1
         fscoreboard.write(f'({j:>2})')
      if includeNames:
         fscoreboard.write(' POINTS\n')
      else:
         fscoreboard.write(' TOTALS POINTS\n')
      listOfStudentDirectories = getListOfStudentDirectories(contestDataDir)
##      print("DBG0",contestDataDir)
##      print("DBG1",listOfStudentDirectories)
##      print("DBG2",includeNames)
##      for x in listOfStudentDirectories:
##        print("DBG3",x)
##        print("DBG4",x.split('_')[1])
##        print("DBG5",int(x.split('_')[1]))
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
           fscoreboard.write(f'{name:20s} {correctCount:>2d}   {code:<6s} {studentResult} {totalPoints:>4d}' + '\n')
        else:
           fscoreboard.write(f'{code:<6s}  {studentResult}  {correctCount:>2d}    {totalPoints:>4d}' + '\n')
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
         fscoreboard.write('TOTALS             ' + f'{sumTotals:>4d}' + '          ' + totals + '\n\n')
      else:
         fscoreboard.write('TOTALS  ' + totals + f'{sumTotals:>4d}' + '\n\n')
        
      fscoreboard.write("Ec  = latest submission had a compile or syntax error.\n")
      fscoreboard.write("Er  = latest submission had a run-time error - e.g. div by 0, index out range.\n")
      fscoreboard.write("Ep  = latest submission had a presentation error - e.g. incorrect spelling, missing text, spacing, capitalization, punctuation.\n")
      fscoreboard.write("C#  = test ran successfully, had # of incorrect submissions.\n")
      fscoreboard.write("#x  = test never ran successfully, submitted # times.")
      fscoreboard.write("\nThe POINTS column indicates your UIL programming competition score (60 pts/problem, -5 pts for every incorrect submission)")
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


   
   
   

          


      


      

      





