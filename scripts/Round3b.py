#!/usr/bin/env python
# Python 2.7
# Round 2


import sys
import numpy
import math
import time


start_time = time.time()

data_file = open("../data_files/Round3_repl","r")
pos_bi_freq = {}
histogram =  {}

output = "" # A comma-delineated output of the data
out_file = open("../data_files/Round3_2grams","w")

for line in data_file.readlines():
    all_pos = line.split()
    def increment(s):
        pos_bi_freq[s] = pos_bi_freq.get(s, 0) + 1
    if len(all_pos) > 1:
        for i in range(0,len(all_pos)-1):
            a = all_pos[i]
            b = all_pos[i+1]
            increment(a)    # count the number of times `a` appears
            increment(a+"++"+b)  # count the number of times the bigram appears, as `a++b`
        increment(all_pos[len(all_pos)-1]) # Account for the fact we aren't counting the last word in the sentence
    elif len(all_pos) == 1:
        increment(all_pos[0])

for pos in pos_bi_freq.keys():
    output += str(pos).replace(",","COM")  + ", " + str(pos_bi_freq[pos]) + "\n"

output+="\n" # Empty line to denote end of a data chunk

end_time = time.time()
output += "Time taken: " + str(end_time-start_time) + " seconds\n"

out_file.write(output)