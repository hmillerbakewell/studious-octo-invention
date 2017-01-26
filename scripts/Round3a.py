"""
Make POS replacements:
nn, nns -> N
jj, at -> N Nl
"""
#!/usr/bin/env python
# Python 2.7
# Round 3

import time

def pos_replace(infile, outfile, replacements):
    "Subsitute occurences of certain pos in the infile and print to outfile"
    start_time = time.time()


    output = "" # A text file, having made type-substitutions for certain POS

    for line in infile.readlines():
        all_pos = line.split(" ")
        for pos in all_pos:
            if pos in replacements:
                output += replacements[pos] + " "
            else:
                output += pos + " "

    output += "\n" # Empty line to denote end of a data chunk

    end_time = time.time()
    output += "Time taken: " + str(end_time-start_time) + " seconds\n"

    outfile.write(output)


INPUT = open("../data_files/POS_ONLY", "r")
OUTPUT = open("../data_files/Round3_repl", "w")
REPLACE = {
    "nn" : "N",
    "nns": "N",
    "jj" : "N Nl",
    "at" : "N Nl"
}
pos_replace(INPUT, OUTPUT, REPLACE)
