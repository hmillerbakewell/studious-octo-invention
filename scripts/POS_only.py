#!/usr/bin/env python
# Python 2.7


import sys
import re # Regular expressions
import numpy


manb = open("../data_files/MERGE_ALL_NO_BLANKS","r")
outfile = open("../data_files/POS_ONLY","w")
output = ""

for line in manb.readlines():
    all_pos = re.findall('[^\s]*\/([^\s]*)',line)
    just_pos = " ".join(all_pos)
    split_plus = re.sub("\+"," ",just_pos) # Split up joined tags, e.g. "wanna"
    move_asterisk = re.sub("(^|[^\s])\*"," *",split_plus)
    output += move_asterisk + "\n"

outfile.write(output)