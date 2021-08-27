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
        points = 0
        for test in listOfTestNames:
           listOfStudentDataFiles = glob.glob(contestDataDir + '/' + studentDirectory + '/' + test + r'_*.txt')
           newestTestDataFile = ""
           if len(listOfStudentDataFiles) > 0:
              newestTestDataFile = max(listOfStudentDataFiles, key=os.path.getmtime)
           if newestTestDataFile.endswith("compileErr.txt"):
              result = "Ec"
           elif newestTestDataFile.endswith("runErr.txt"):
              result = "Er"
           else:
              count = 0
              correctFound = False
              for studentDataFile in listOfStudentDataFiles:
                 if not studentDataFile.endswith("CORRECT.txt"):
                    count += 1
                 else:
                    correctFound = True
              if correctFound:
                 correctCount = correctCount + 1
                 testsCorrect[test] = testsCorrect.get(test,0) + 1
                 if count == 0:
                    result = "C"
                    points = points + 60
                 else:
                    result = "C" + str(count)
                    points = points + (60 - (count*5))
              else:
                 result = str(count) + 'x'
           studentResult = studentResult + f'{result:<2s}' + '  '
           countTestsInRow += 1
        if includeNames:
           fscoreboard.write(f'{name:20s} {correctCount:>2d}   {code:<6s} {studentResult} {points:>4d}' + '\n')
        else:
           fscoreboard.write(f'{code:<6s}  {studentResult}  {correctCount:>2d}    {points:>4d}' + '\n')
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
      fscoreboard.write("C#  = test ran successfully, had # of incorrect submissions.\n")
      fscoreboard.write("#x  = test never ran successfully, submitted # times.")
      fscoreboard.close()  


def getListOfStudentDirectories(contestDataDir):
   listOfDataDirectories = [ f.name for f in os.scandir(contestDataDir) if f.is_dir() ]  # https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
   listOfDataDirectoriesSorted = sorted(listOfDataDirectories, key=str.casefold)  # sorts case insensitvely:  https://stackoverflow.com/questions/10269701/case-insensitive-list-sorting-without-lowercasing-the-result
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

         


          


      


      

      





