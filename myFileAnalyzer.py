import os

aFile = input('Name of file to analyze (in quotes): ')
cmd_file = "file {}".format(aFile)
aFileType = os.system(cmd_file)
