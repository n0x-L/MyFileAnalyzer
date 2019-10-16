# For python 3.5 - 3.6.5


import os, subprocess, sys, argparse

# Global Variables
absoluteNumerics = {'0': 'No Permission',
                    '1': 'Execute',
                    '2': 'Write',
                    '3':'Execute+Write',
                    '4': 'Read',
                    '5': 'Read+Execute',
                    '6':'Read+Write',
                    '7':'Read+Write+Execute'}


# 1 Get the File size
def get_FileSize(aFile):
  getFileSize = subprocess.run(['du', '-h', aFile], check=True, stdout=subprocess.PIPE, universal_newlines=True)
  getFileSize = getFileSize.stdout
  if aFile in getFileSize:
    getFileSize = getFileSize.replace(aFile, '')
    print("\n--- File Size ---\n", getFileSize)
  """
  aFile = aFile
  getFileSize = subprocess.run(["du", "-h", aFile], check=True, check=True, text=True)
  getFileSize = getFileSize.stdout

  if aFile in getFileSize:
    getFileSize = getFileSize.replace(aFile, '')
    print("\n--- File Size ---\n", getFileSize)
  """

# 2 Get File Attributes
# Owner, Group, Timestamps
def get_FileAttributes(aFile):
  getFileAttributes = subprocess.run(["ls", "-l", aFile], check=True, check=True, text=True)
  fileAttributesList = getFileAttributes.stdout.split()
  ownerName = fileAttributesList[2]
  groupID = fileAttributesList[3]
  #fileSizeBytes = fileAttributesList[4]
  lastModified_Month = fileAttributesList[5]
  lastModified_Day = fileAttributesList[6]
  lastModified_Hour = fileAttributesList[7]

  print("--- File Attributes ---")
  print("Owner Name:", ownerName)
  print("Group Name or ID:", groupID)
  print("Last Modified:", lastModified_Month, lastModified_Day, lastModified_Hour)

# Permissions
def get_FilePermissions(aFile):
  getFilePermOctal = subprocess.run(["stat", "-c", "'%a %n'", aFile], check=True, check=True, text=True)
  fileOctal = getFilePermOctal.stdout
  owner = fileOctal[1]
  group = fileOctal[2]
  other = fileOctal[3]

  print("Owner Permissions:", absoluteNumerics[owner])
  print("Group Permissions:", absoluteNumerics[group])
  print("All Others Permissions:", absoluteNumerics[other])

# 3 Extended attributes (NOT WORKING ON SCHOOL COMP)
# Trying to use lsattr: lsattr: Inappropriate ioctl for device While reading flags on a.out
#etExtendedAttr = subprocess.run(["xattr", aFile], check=True, check=True, text=True)
#getExtendedAttr = getExtendedAttr.stdout
#print('\n--- Extended File Attributes ---')
#if getExtendedAttr:
#    print(getExtendedAttr)
#else:
#    print('None.')

# 4 Get the File Type
def get_FileType(aFile):
  getFileType = subprocess.run(["file", "-b", aFile], check=True, check=True, text=True)
  print("\n--- File Type ---", '\n', getFileType.stdout)


# 5 Interesting strings within the file
# use option '-el' to get unicode strings
def get_FileStrings(aFile):
  getASCII = subprocess.run(["strings", "-a", aFile], check=True, check=True, text=True)
  stringFileText = getASCII.stdout
  print(stringFileText, file=open("fileStrings.txt", "w"))
  print("\n--- Extracted ASCII Strings ---\n")
  print("FILE CREATED: fileStrings.txt")


# 6 Symbols Defined in the Executable
def get_Internal_File_Symbols(aFile):
  getSymbols = subprocess.run(["nm", aFile], check=True, check=True, text=True)
  symbolText = getSymbols.stdout
  print("\n--- Symbols Defined in Executable ---\n")
  print(symbolText)

# Get hexdump
def get_FileHexdump(aFile):
  getHexDump = subprocess.run(["hexdump", "-C", aFile], check=True, check=True, text=True)
  hexFileText = getHexDump.stdout
  print(hexFileText, file=open("hexDump.txt", "w"))
  print("\n--- HexDump ---\n")
  print("FILE CREATED: hexDump.txt\n")


# 7 Symbols Imported into the Executable
# display only external symbols of executable
def get_External_File_Symbols(aFile):
  getExternalSymbols = subprocess.run(["nm", "-g", aFile], check=True, check=True, text=True)
  externalSymbols = getExternalSymbols.stdout
  print(externalSymbols, file=open("externalSymbols.txt", "w"))
  print("\n--- External Symbols ---\n")
  print("FILE CREATED: externalSymbols.txt\n")


# 8 Required Libraries
def get_File_Required_Libraries(aFile):
  getReqLibraries = subprocess.run(["ldd", "-v", aFile], check=True, check=True, text=True)
  print("\n--- Required Libraries ---\n")
  print(getReqLibraries.stdout)


# 9 System Calls Performed when Run
# to trace all system calls (strace) involving memory mapping: sudo strace -q -e trace=memory df -h
# trace all system calls (strace) involving process mgmt: sudo strace -q -e trace=process df -h	
# 
def get_File_System_Calls(aFile):
  runFileFormat = "./{}".format(aFile)
  getSysCalls = subprocess.run(["strace", "-c", runFileFormat], check=True, check=True, text=True)
  sysCallsText = getSysCalls.stdout
  print(sysCallsText, file=open("systemCallTrace.txt", "w"))
  print("\n--- System Calls ---\n")
  print(getSysCalls.stderr)


# 10 Library Calls Performed when Run
def get_File_Library_Calls(aFile):
  runFileFormat = "./{}".format(aFile)
  getLibCalls = subprocess.run(["ltrace", runFileFormat], check=True, check=True, text=True)
  libCallsText = getLibCalls.stdout
  print(libCallsText, file=open("libCallsTrace.txt", "w"))
  print("\n--- Library Calls ---\n")
  print(getLibCalls.stderr)


# 11 How the system and library calls differ, and why
def get_System_Library_Delta(aFile):
  runFileFormat = "./{}".format(aFile)
  sysCallNames = ">(awk '$1 ~ /^-----/ {toprint = !toprint; next} {if (toprint) print $NF}')" 
  part4 = ">/dev/null 2>/dev/null"
  getSysNames = subprocess.run(["strace", "-o", ">(awk '$1 ~ /^-----/ {toprint = !toprint; next} {if (toprint) print $NF}')", "-c", runFileFormat, ">/dev/null 2>/dev/null"], check=True, check=True, text=True)
  print('System Call Names:')
  print(getSysNames.stdout)
