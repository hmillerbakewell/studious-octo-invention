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





def ignore():
    manb = open("../data_files/MERGE_ALL_NO_BLANKS","r")
    pos_sentence_length = {}
    histogram =  {}
    bins = numpy.arange(0,71,7)


    for line in manb.readlines()[:15]:
        all_pos = re.findall('[^\s]*\/([^\s]*)',line)
        sentence_length = len(all_pos)-1 #length-1 because of trailing full-stop
        for pos in all_pos:
            pos_sentence_length[pos] = pos_sentence_length.get(pos, []) + [sentence_length]

    for pos in pos_sentence_length.keys():
        histogram[pos] = numpy.histogram(pos_sentence_length[pos],bins,density=True)

    for pos in histogram.keys():
        print str(pos) + ", " + ", ".join(map(str,histogram[pos][0]))