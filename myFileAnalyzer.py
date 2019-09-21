# Python 3.7
# Running on macOS

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
"""
import os, subprocess, floss

results = []
absoluteNumerics = {'0': 'No Permission',
                    '1': 'Execute',
                    '2': 'Write',
                    '3':'Execute+Write',
                    '4': 'Read',
                    '5': 'Read+Execute',
                    '6':'Read+Write',
                    '7':'Read+Write+Execute'}

aFile = input('\nFile to analyze (ie test.txt): ')

# 1 Get the File size
getFileSize = subprocess.run(["du", "-h", aFile], capture_output=True, check=True, text=True)
getFileSize = getFileSize.stdout

# output formatting
if aFile in getFileSize:
    getFileSize = getFileSize.replace(aFile, '')
print("\n--- File Size ---\n", getFileSize)

# 2 Get File Attributes (owner, group, permissions, timestamps, &c)
getFileAttributes = subprocess.run(["ls", "-l", aFile], capture_output=True, check=True, text=True)
fileAttributesList = getFileAttributes.stdout.split()
ownerName = fileAttributesList[2]
groupID = fileAttributesList[3]
fileSizeBytes = fileAttributesList[4]
lastModified_Month = fileAttributesList[5]
lastModified_Day = fileAttributesList[6]
lastModified_Hour = fileAttributesList[7]

print("--- File Attributes ---")
print("Owner Name:", ownerName)
print("Group Name or ID:", groupID)
print("Last Modified:", lastModified_Month, lastModified_Day, lastModified_Hour)

getFilePermOctal = subprocess.run(["stat", "-f", "'%A'", aFile], capture_output=True, check=True, text=True)
fileOctal = getFilePermOctal.stdout
owner = fileOctal[1]
group = fileOctal[2]
other = fileOctal[3]

print("Owner Permissions:", absoluteNumerics[owner])
print("Group Permissions:", absoluteNumerics[group])
print("All Others Permissions:", absoluteNumerics[other])

# 3 Get extended File Attributes
getExtendedAttr = subprocess.run(["xattr", aFile], capture_output=True, check=True, text=True)
getExtendedAttr = getExtendedAttr.stdout
print('\n--- Extended File Attributes ---')
if getExtendedAttr:
    print(getExtendedAttr)
else:
    print('None.')

# 4 Get the File Type
fileType = 'file {}'.format(aFile)
getFileType = subprocess.run(["file", "-b", aFile], capture_output=True, check=True, text=True)
print("\n--- File Type ---", '\n', getFileType.stdout)

# 5 Interesting strings within the file
getUnicodeStr = subprocess.run(["strings", "-a", "-el", aFile], capture_output=True, check=True, text=True)
print("FILE CREATED: strings.txt")
#print(getUnicodeStr.stdout, file=open("strings.txt", "w"))

# 6 Symbols defined in the executable

# Store Final results as object
results.append({'FileSize': getFileSize,
                'OwnerName': ownerName,
                'GroupID': groupID,
                'SizeBytes': fileSizeBytes,
                'LastModifiedMonth': lastModified_Month,
                'LastModifiedDay': lastModified_Day,
                'LastModifiedHour': lastModified_Hour,
                'FileOctal': fileOctal,
                'FileType': fileType,
                'ExtendedAttributes': getExtendedAttr
                })