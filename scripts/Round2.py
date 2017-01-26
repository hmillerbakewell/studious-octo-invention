"""
Get frequency data on 2-grams
"""
#!/usr/bin/env python
# Python 2.7
# Round 2


import time

def bigram_data(infile, outfile):
    "Calculate bigram information from infile and print to outfile"
    start_time = time.time()

    pos_bi_freq = {}

    output = "" # A comma-delineated output of the data

    for line in infile.readlines():
        all_pos = line.split()
        def increment(_pos):
            "Increment the counter"
            pos_bi_freq[_pos] = pos_bi_freq.get(_pos, 0) + 1
        if len(all_pos) > 1:
            for i in range(0, len(all_pos)-1):
                first = all_pos[i]
                second = all_pos[i+1]
                increment(first)    # count the number of times `a` appears
                # count the number of times the bigram appears, as `a++b`
                increment(first+"++"+second)
            # Account for the fact we aren't counting the last word in the sentence
            increment(all_pos[len(all_pos)-1])
        elif len(all_pos) == 1:
            increment(all_pos[0])

    for pos in pos_bi_freq:
        output += str(pos).replace(",", "COM")  + ", " + str(pos_bi_freq[pos]) + "\n"

    output += "\n" # Empty line to denote end of a data chunk

    end_time = time.time()
    output += "Time taken: " + str(end_time-start_time) + " seconds\n"

    outfile.write(output)


INPUT = open("../data_files/POS_ONLY", "r")
OUTPUT = open("../data_files/Round2", "w")
bigram_data(INPUT, OUTPUT)
