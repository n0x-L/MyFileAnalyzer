# Python 3

"""
1     File size
2     File attributes: owner, group, permissions, timestamps, &c.
3     Extended file attributes
4     File type
5     Interesting strings within the file
6     Symbols defined in the executable
7     Symbols imported into the executable
8     Required libraries
9     System calls performed when run
10    Library calls performed when run
11    How the system and library calls differ, and why
12    Executable sections and the information they contain
13    Assembly code
14    Start address of program
15    Compiler used to compile the program
16    What happens differently between the first and second times printf is called
"""
import os, subprocess

results = []

aFile = input('File to analyze (ie test.txt): ')

# 1 Get the File size
getFileSize = subprocess.run(["du", "-h", aFile], capture_output=True, text=True)
getFileSize = getFileSize.stdout
getFileSize.replace(aFile, '')
print("File Size:", getFileSize)
results.append({'File Size':getFileSize})

# 2 Get File Attributes (owner, group, permissions, timestamps, &c)

# 3 Get extended File Attributes


# 4 Get the File Type
fileType = 'file {}'.format(aFile)
getFileType = subprocess.run(["file", "-b", aFile], capture_output=True, text=True)
print("File Type:", getFileType.stdout)
results.append({'File Type':getFileType})

# 5 Interesting strings within the file

