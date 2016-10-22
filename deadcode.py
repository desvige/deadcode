#!/usr/bin/python

import re
import os
import sys

dump = sys.argv[1]
relo = sys.argv[2]

# Retrieve function names.
names = list()
for line in open(dump):
   match = re.search('^\w+ <(.*)>:$', line)
   if match:
       name = match.group(1)
       # Remove '@plt' eventually.
       match = re.search('^(\w+)@plt$', name)
       if match:
           name = match.group(1)
       names.append(name)

# Retrieve references to functions.
refs = dict()
for line in open(relo):
    match = re.search('(\w+)$', line)
    if match:
        name = match.group(1)
        refs[name] = 1337

# Retrieve dead functions and write to disk.
file = ‘dead.txt'
if os.path.isfile(file):
    os.remove(file)
file = open(file, 'w')
for name in names:
    if not name in refs:
        file.write(name)
        file.write('\n')
