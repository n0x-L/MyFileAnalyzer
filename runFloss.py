#!/usr/bin/env python3
import subprocess

python3_command = "py2file.py arg1 arg2"  # launch your python2 script using bash

process = subprocess.Popen(python3_command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()  # receive output from the python2 script