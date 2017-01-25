#!/usr/bin/env python
# Python 2.7
# Round 3


import sys
import numpy
import math
import time


start_time = time.time()

data_file = open("../data_files/POS_ONLY","r")

output = "" # A text file, having made type-substitutions for certain POS
out_file = open("../data_files/Round3_repl","w")

replacements = {
    "nn" : "N",
    "nns": "N",
    "jj" : "N Nl",
    "at" : "N Nl"
    }

for line in data_file.readlines():
    all_pos = line.split(" ")
    for pos in all_pos:
        if pos in replacements:
            output += replacements[pos] + " "
        else:
            output += pos + " "
    output += "\n"

output+="\n" # Empty line to denote end of a data chunk

end_time = time.time()
output += "Time taken: " + str(end_time-start_time) + " seconds\n"

out_file.write(output)