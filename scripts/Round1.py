"""
Create frequency histograms for each POS
"""
#!/usr/bin/env python
# Python 2.7
# Round 1


# import time
import numpy

def create_hist(infile, outfile):
    "Create histogram data in outfile, from data in infile"
    # start_time = time.time()

    pos_sentence_length = {}
    max_sentence_length = 0
    histogram = {}

    output = "" # A comma-delineated output of the data

    sentences_with_htags = 0

    for line in infile.readlines():
        if ("-hl" in line) or ("-tl" in line) or ("-nc" in line):
            sentences_with_htags += 1
        all_pos = line.split()
        sentence_length = len(all_pos)
        max_sentence_length = max(max_sentence_length, sentence_length)
        aget = lambda p: pos_sentence_length.get(p, [])
        # Add in the POS "SENTENCE" that simply records the distribution of sentence lengths
        pos_sentence_length["SENTENCE"] = aget("SENTENCE") + [sentence_length]
        for pos in all_pos:
            pos_sentence_length[pos] = aget(pos) + [sentence_length]

    bins = numpy.arange(0, max_sentence_length+1, 1)

    for pos in pos_sentence_length:
        histogram[pos] = numpy.histogram(pos_sentence_length[pos], bins, density=True)

    # The bins list contains one more entry than is useful
    output += "Histogram, " + ", ".join(map(str, bins[1:])) + ", TOTAL\n"

    for pos in histogram:
        hist_data = ", ".join(map(str, histogram[pos][0]))
        total_appearances = str(len(pos_sentence_length[pos]))
        output += str(pos).replace(",", "COM") + ", " + hist_data + ", " + total_appearances + "\n"

    output += "\n" # Empty line to denote end of a data chunk

    # output += "Sentences with hyphenated tags: " + str(sentences_with_htags) + "\n"


    # end_time = time.time()
    # output += "Time taken: " + str(end_time-start_time) + " seconds\n"

    outfile.write(output)
    outfile.close()
    infile.close()

INPUT = open("../data_files/POS_ONLY", "r")
OUTPUT = open("../data_files/Round1", "w")
create_hist(INPUT, OUTPUT)
