"""
Grouping together of Proper Nouns and Titles
"""
#!/usr/bin/env python
# Python 2.7
# Round 2

import time
import re

def group_runs(infile, outfile, regex, replacement):
    "Group together instances of pos that match a given regex"
    start_time = time.time()
    output = ""

    for line in infile.readlines():
        all_pos = line.split()
        matched = False
        for pos in all_pos:
            if re.match(regex, pos):
                if not matched:
                    matched = True
                    output += replacement + " "
            else:
                matched = False
                output += pos + " "
        output += "\n"

    end_time = time.time()
    output += "Time taken: " + str(end_time-start_time) + " seconds\n"

    outfile.write(output)


INPUT = open("../data_files/Round3_repl", "r")
TEMPOUT = open("../data_files/Round4_temp", "w")
TEMPIN = open("../data_files/Round4_temp", "r")
OUTPUT = open("../data_files/Round4", "w")

group_runs(INPUT, TEMPOUT, r'^.*-tl$', "TL")
group_runs(TEMPIN, OUTPUT, r'^nps?$', "P")
