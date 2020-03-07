# File Analyzer for MacOS

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


NOTE: Mach-O is the native executable format of binaries in OS X and is the preferred format for shipping code.
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

# 1 File size
def get_FileSize(aFile, verbose):
  getFileSize = subprocess.run(["du", "-h", aFile], capture_output=True, check=True, text=True)
  getFileSize = getFileSize.stdout

  if aFile in getFileSize:
    getFileSize = getFileSize.replace(aFile, '')

    if verbose:
      print("\n--- File Size ---\n", getFileSize)
    else:
      make_file("file_size", getFileSize)

# 2 File Attributes
# Owner, Group, Timestamps
def get_FileAttributes(aFile, verbose):
  getFileAttributes = subprocess.run(["ls", "-l", aFile], capture_output=True, check=True, text=True)
  fileAttributesList = getFileAttributes.stdout.split()
  ownerName = fileAttributesList[2]
  groupID = fileAttributesList[3]
  #fileSizeBytes = fileAttributesList[4]
  lastModified_Month = fileAttributesList[5]
  lastModified_Day = fileAttributesList[6]
  lastModified_Hour = fileAttributesList[7]

  if verbose:
    print("--- File Attributes ---")
    print("Owner Name:", ownerName)
    print("Group Name or ID:", groupID)
    print("Last Modified:", lastModified_Month, lastModified_Day, lastModified_Hour)
  else:
    attr_dict = {"Owner" : ownerName, "Group Name or ID" : groupID, "Last Modified Month" : lastModified_Month, "Last Modified Day" : lastModified_Day, "Last Modified Hour" : lastModified_Hour}
    make_file("file_attributes", attr_dict)

# Permissions
def get_FilePermissions(aFile, verbose):
  getFilePermOctal = subprocess.run(["stat", "-f", "'%A'", aFile], capture_output=True, check=True, text=True)
  fileOctal = getFilePermOctal.stdout
  owner = fileOctal[1]
  group = fileOctal[2]
  other = fileOctal[3]

  if verbose:
    print("\n--- File Permissions ---")
    print("Owner Permissions:", absoluteNumerics[owner])
    print("Group Permissions:", absoluteNumerics[group])
    print("All Others Permissions:", absoluteNumerics[other])
  
  else:
    perm_dict = {"Owner" : absoluteNumerics[owner], "Group" : absoluteNumerics[group], "Others" : absoluteNumerics[other]}
    make_file("file_permissions", perm_dict)

# Extended File Attributes
# Trying to use lsattr: lsattr: Inappropriate ioctl for device While reading flags on a.out
def get_File_Extended_Attributes(aFile, verbose):
  getExtendedAttr = subprocess.run(["xattr", aFile], capture_output=True, check=True, text=True)
  getExtendedAttr = getExtendedAttr.stdout

  if verbose:
    print('\n--- Extended File Attributes ---')
    if getExtendedAttr:
      print(getExtendedAttr)
    else:
      print('None.')

  else:
    if getExtendedAttr:
      make_file("extended_attributes", getExtendedAttr)
    else:
      make_file("extended_attributes", "None")

# 4 Get the File Type
def get_FileType(aFile, verbose):
  getFileType = subprocess.run(["file", "-b", aFile], capture_output=True, check=True, text=True)

  if verbose:
    print("--- File Type ---\n", getFileType.stdout)
  else:
    make_file("file_type", getFileType.stdout)

# 5 Interesting strings within the file
# use option '-el' to get unicode strings
def get_FileStrings(aFile, verbose):
  getASCII = subprocess.run(["strings", "-a", aFile], capture_output=True, check=True, text=True)
  stringFileText = getASCII.stdout

  if verbose:
    print("--- Extracted ASCII Strings ---")
    print("output too large, sending to file:")
  
  make_file("asciiStrings", stringFileText)

# 6 Symbols Defined in the Executable
def get_Internal_File_Symbols(aFile, verbose):
  getSymbols = subprocess.run(["nm", aFile], capture_output=True, check=True, text=True)
  symbolText = getSymbols.stdout

  if verbose:
    print("\n--- Symbols Defined in Executable ---", symbolText)
  else:
    make_file("symbols", symbolText)

# Get hexdump
def get_FileHexdump(aFile, verbose):
  getHexDump = subprocess.run(["hexdump", "-C", aFile], capture_output=True, check=True, text=True)
  hexFileText = getHexDump.stdout

  if verbose:
    print("\n--- HexDump ---\n output too large, sending to file:")
  
  make_file("hexDump", hexFileText)

# 7 Symbols Imported into the Executable
# display only external symbols of executable
def get_External_File_Symbols(aFile, verbose):
  getExternalSymbols = subprocess.run(["nm", "-g", aFile], capture_output=True, check=True, text=True)
  externalSymbols = getExternalSymbols.stdout

  if verbose:
    print("\n--- External Symbols ---\n output too large, sending to file")

  make_file("externalSymbols", externalSymbols)

# 8 Required Libraries - *NOT WORKING FOR OSX YET*
# otool -L
def get_File_Required_Libraries(aFile, verbose):
  try:
    getReqLibraries = subprocess.run(["ldd", "-v", aFile], capture_output=True, check=True, text=True)
    if verbose:
        print("\n--- Required Libraries ---\n")
        print(getReqLibraries.stdout)
    
    else:
      make_file("required_libs", getReqLibraries.stdout)

  except subprocess.CalledProcessError as er:
    print(er)

  except FileNotFoundError as f:
    print("\n Problem getting required libraries:")
    print(f)

# 9 System Calls Performed when Run
# to trace all system calls (strace) involving memory mapping: sudo strace -q -e trace=memory df -h
# trace all system calls (strace) involving process mgmt: sudo strace -q -e trace=process df -h	
# 
# what is the c start up, what is dynamic linker, and what is the 'main' execution (entry point, (_start))
def get_File_System_Calls(aFile, verbose):
  runFileFormat = "./{}".format(aFile)

  try:
    getSysCalls = subprocess.run(["strace", "-c", runFileFormat], capture_output=True, check=True, text=True)
    sysCallsText = getSysCalls.stdout

    if verbose:
      print("\n--- System Calls ---\n")
      print(getSysCalls.stderr)
    else:
      make_file("system_calls", sysCallsText)

  except subprocess.CalledProcessError as er:
    print(er)

  except FileNotFoundError as f:
    print("\n Problem getting system calls:")
    print(f)


# 10 Library Calls Performed when Run
def get_File_Library_Calls(aFile, verbose):
  runFileFormat = "./{}".format(aFile)

  try:
    getLibCalls = subprocess.run(["ltrace", runFileFormat], capture_output=True, check=True, text=True)
    libCallsText = getLibCalls.stdout

    if verbose:
      print("\n--- Library Calls ---\n")
      print(getLibCalls.stderr)
    else:
      make_file("library_calls", libCallsText)

  except subprocess.CalledProcessError as er:
    print(er)

  except FileNotFoundError as f:
    print("\nProblem getting library calls")
    print(f)


# 11 How the system and library calls differ, and why
"""
def get_System_Library_Delta(aFile):
  runFileFormat = "./{}".format(aFile)
  sysCallNames = ">(awk '$1 ~ /^-----/ {toprint = !toprint; next} {if (toprint) print $NF}')" 
  part4 = ">/dev/null 2>/dev/null"
  getSysNames = subprocess.run(["strace", "-o", ">(awk '$1 ~ /^-----/ {toprint = !toprint; next} {if (toprint) print $NF}')", "-c", runFileFormat, ">/dev/null 2>/dev/null"], capture_output=True, check=True, text=True)
  print('System Call Names:')
  print(getSysNames.stdout)
"""

# 12 Executable sections and the Information they Contain


# 13 Assembly Code



# 14 Start Address of Program
#_start

# 15 Compiler Used to Compile the Program


# 16 What Happens Differently Between the First and Second times 'printf' is Called

# Method for creating file output when verbosity is turned off
def make_file(file_name, content):
  file_name = file_name + ".txt"
  print(content, file=open(file_name, "w"))
  print("\nFile created: ", file_name)

def print_welcome():
  print("\n\t\t\t###########################################################")
  print("\t\t\t\t A program for analyzing binaries")
  print("\t\t\t**** made by Amanda N. Leeson, master of the universe ****")
  print("\t\t\t###########################################################")

def exit():
  print("\n")
  print("Program complete, exiting....")
  print("Goodbye!")
  sys.exit(0)



# Main
def main(argv):
  aFile = ""
  verbose = False

  parser = argparse.ArgumentParser(description='A simply python program for analyzing binaries.')
  parser.add_argument("-f", "--file", required=True, type=str, help="The file name (with extension) you wish to analyze.")
  parser.add_argument("-v", "--verbose", type=bool, help="Set to 1 for True, False by default.")
  args = parser.parse_args()
  aFile = args.file
  verbose = args.verbose

  # print welcome (really its for keeping track of output)
  print_welcome()

  # call functions
  get_FileSize(aFile, verbose)
  get_FileAttributes(aFile, verbose)
  get_FilePermissions(aFile, verbose)
  get_File_Extended_Attributes(aFile, verbose)
  get_FileType(aFile, verbose)
  get_FileStrings(aFile, verbose)
  get_Internal_File_Symbols(aFile, verbose)
  get_FileHexdump(aFile, verbose)
  get_External_File_Symbols(aFile, verbose)

  # Commands not working:
  # ldd, strace, and ltrace not built for OSX
  get_File_Required_Libraries(aFile, verbose)
  get_File_System_Calls(aFile, verbose)
  get_File_Library_Calls(aFile, verbose)

  # Not implemented yet:
  #get_System_Library_Delta(aFile)

  exit()


# Call main, pass in command line argument given
if __name__ == "__main__":
  main(sys.argv[1:])