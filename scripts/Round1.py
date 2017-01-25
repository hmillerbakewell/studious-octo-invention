#!/usr/bin/env python
# Python 2.7
# Round 1


import sys
import numpy
import math
import time


start_time = time.time()

data_file = open("../data_files/POS_ONLY","r")
pos_sentence_length = {}
max_sentence_length = 0
histogram =  {}

output = "" # A comma-delineated output of the data
out_file = open("../data_files/Round1","w")

sentences_with_htags = 0

for line in data_file.readlines():
    if ("-hl" in line) or ("-tl" in line) or ("-nc" in line):
        sentences_with_htags += 1
    all_pos = line.split()
    sentence_length = len(all_pos)
    max_sentence_length = max(max_sentence_length,sentence_length)
    # Add in the POS "SENTENCE" that simply records the distribution of sentence lengths
    pos_sentence_length["SENTENCE"] = pos_sentence_length.get("SENTENCE", []) + [sentence_length]
    for pos in all_pos:
        pos_sentence_length[pos] = pos_sentence_length.get(pos, []) + [sentence_length]

bins = numpy.arange(0,max_sentence_length+1,1)

for pos in pos_sentence_length.keys():
    histogram[pos] = numpy.histogram(pos_sentence_length[pos],bins,density=True)

# The bins list contains one more entry than is useful
output += "Histogram, " + ", ".join(map(str,bins[1:])) + ", TOTAL\n"

for pos in histogram.keys():
    name = str(pos)
    hist_data = ", ".join(map(str,histogram[pos][0])) 
    total_appearances = str(len(pos_sentence_length[pos]))
    output += str(pos).replace(",","COM") + ", " + hist_data + ", " + total_appearances + "\n"

output+="\n" # Empty line to denote end of a data chunk

output += "Sentences with hyphenated tags: " + str(sentences_with_htags) + "\n"


end_time = time.time()
output += "Time taken: " + str(end_time-start_time) + " seconds\n"

out_file.write(output)