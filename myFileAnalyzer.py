# Python 3.7

"""
1     File size
2     File attributes: owner, group, permissions, timestamps, &c.
3     Extended file attributes:
                 - a mechanism for adding your own metadata to files. 
                   File systems supporting include ext2, ext3, ext4, jfs, xfs, squashfs
                - 4 namespaces for extended attributes: user, trusted, security, system
                - The system namespace could be used for adding metadata controlled by root. It is used 
                  primarily by the kernel for access control lists
                - The security namespace is used by SELinux
                - User namespace meant to be used by user and its applications
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

NOTE: All of these may not yeild results

Helpful Commands:
ls … file size and attributes
lsattr … extended file attributes
file … file type, may not be exact in all cases
strings … seemingly-printable strings within file
od and hexdump … print binary data in readable ways
nm … file symbol information
ldd … shared library information
strace … trace system calls
ltrace … trace library calls
readelf … ELF executable information
objdump … assembly code and more
ndisasm … also disassembly, but better with unstructured binary code
"""
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
  aFile = aFile
  getFileSize = subprocess.run(["du", "-h", aFile], capture_output=True, check=True, text=True)
  getFileSize = getFileSize.stdout

  if aFile in getFileSize:
    getFileSize = getFileSize.replace(aFile, '')
    print("\n--- File Size ---\n", getFileSize)

# 2 Get File Attributes
# Owner, Group, Timestamps
def get_FileAttributes(aFile):
  getFileAttributes = subprocess.run(["ls", "-l", aFile], capture_output=True, check=True, text=True)
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
  getFilePermOctal = subprocess.run(["stat", "-c", "'%a %n'", aFile], capture_output=True, check=True, text=True)
  fileOctal = getFilePermOctal.stdout
  owner = fileOctal[1]
  group = fileOctal[2]
  other = fileOctal[3]

  print("Owner Permissions:", absoluteNumerics[owner])
  print("Group Permissions:", absoluteNumerics[group])
  print("All Others Permissions:", absoluteNumerics[other])

# 3 Extended attributes (NOT WORKING ON SCHOOL COMP)
# Trying to use lsattr: lsattr: Inappropriate ioctl for device While reading flags on a.out
#etExtendedAttr = subprocess.run(["xattr", aFile], capture_output=True, check=True, text=True)
#getExtendedAttr = getExtendedAttr.stdout
#print('\n--- Extended File Attributes ---')
#if getExtendedAttr:
#    print(getExtendedAttr)
#else:
#    print('None.')

# 4 Get the File Type
def get_FileType(aFile):
  getFileType = subprocess.run(["file", "-b", aFile], capture_output=True, check=True, text=True)
  print("\n--- File Type ---", '\n', getFileType.stdout)


# 5 Interesting strings within the file
# use option '-el' to get unicode strings
def get_FileStrings(aFile):
  getASCII = subprocess.run(["strings", "-a", aFile], capture_output=True, check=True, text=True)
  stringFileText = getASCII.stdout
  print(stringFileText, file=open("fileStrings.txt", "w"))
  print("\n--- Extracted ASCII Strings ---\n")
  print("FILE CREATED: fileStrings.txt")


# 6 Symbols Defined in the Executable
def get_Internal_File_Symbols(aFile):
  getSymbols = subprocess.run(["nm", aFile], capture_output=True, check=True, text=True)
  symbolText = getSymbols.stdout
  print("\n--- Symbols Defined in Executable ---\n")
  print(symbolText)

# Get hexdump
def get_FileHexdump(aFile):
  getHexDump = subprocess.run(["hexdump", "-C", aFile], capture_output=True, check=True, text=True)
  hexFileText = getHexDump.stdout
  print(hexFileText, file=open("hexDump.txt", "w"))
  print("\n--- HexDump ---\n")
  print("FILE CREATED: hexDump.txt\n")


# 7 Symbols Imported into the Executable
# display only external symbols of executable
def get_External_File_Symbols(aFile):
  getExternalSymbols = subprocess.run(["nm", "-g", aFile], capture_output=True, check=True, text=True)
  externalSymbols = getExternalSymbols.stdout
  print(externalSymbols, file=open("externalSymbols.txt", "w"))
  print("\n--- External Symbols ---\n")
  print("FILE CREATED: externalSymbols.txt\n")


# 8 Required Libraries
def get_File_Required_Libraries(aFile):
  getReqLibraries = subprocess.run(["ldd", "-v", aFile], capture_output=True, check=True, text=True)
  print("\n--- Required Libraries ---\n")
  print(getReqLibraries.stdout)


# 9 System Calls Performed when Run
def get_File_System_Calls(aFile):
  runFileFormat = "./{}".format(aFile)
  getSysCalls = subprocess.run(["strace", runFileFormat], capture_output=True, check=True, text=True)
  sysCallsText = getSysCalls.stdout
  print(sysCallsText, file=open("systemCallTrace.txt", "w"))
  print("\n--- System Calls ---\n")
  print(getSysCalls.stderr)


# 10 Library Calls Performed when Run
def get_File_Library_Calls(aFile):
  runFileFormat = "./{}".format(aFile)
  getLibCalls = subprocess.run(["ltrace", runFileFormat], capture_output=True, check=True, text=True)
  libCallsText = getLibCalls.stdout
  print(libCallsText, file=open("libCallsTrace.txt", "w"))
  print("\n--- Library Calls ---\n")
  print(getLibCalls.stderr)


# 11 How the system and library calls differ, and why



# 12 Executable sections and the Information they Contain


# 13 Assembly Code



# 14 Start Address of Program


# 15 Compiler Used to Compile the Program


# 16 What Happens Differently Between the First and Second times 'printf' is Called


# Main
def main(argv):
  aFile = ""
  parser = argparse.ArgumentParser(description='A program for analyzing binaries.')
  parser.add_argument("--file", default=1, type=str, help="The file name (with extension) you wish to analyze.")
  
  args = parser.parse_args()
  aFile = args.file

  # call functions
  get_FileSize(aFile)
  get_FileAttributes(aFile)
  get_FilePermissions(aFile)
  get_FileType(aFile)
  get_Internal_File_Symbols(aFile)
  get_FileHexdump(aFile)
  get_External_File_Symbols(aFile)
  get_File_Required_Libraries(aFile)
  get_File_System_Calls(aFile)
  get_File_Library_Calls(aFile)


# Call main, pass in command line argument given
if __name__ == "__main__":
  main(sys.argv[1:])