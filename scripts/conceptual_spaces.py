"""
Conceptual Spaces modelling of natural language
"""
#!/usr/bin/env python
# Python 2.7

import re
import random
import numpy

DATA = "../data_files/"


def create_histogram(infilename, outfilename):
    "Create histogram of POS data in outfile, from data in infile"

    # TODO: This function used to need numpy
    # Could now be achieved without it
    # Leaving for now, as may need numpy later

    infile = open(DATA+infilename, "r")

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

    # The bins list contains one more entry than is needed
    output += "Histogram, " + ", ".join(map(str, bins[1:])) + ", TOTAL\n"

    for pos in histogram:
        hist_data = ", ".join(map(str, histogram[pos][0]))
        total_appearances = str(len(pos_sentence_length[pos]))
        # Replace commas with "COM" to aid legibility
        output += str(pos).replace(",", "COM") + ", " + hist_data + ", " + total_appearances + "\n"

    infile.close()
    outfile = open(DATA+outfilename, "w")
    outfile.write(output)
    outfile.close()



def strip_pos(infilename, outfilename):
    "Remove the word data and keep only the POS data from infile"

    infile = open(DATA+infilename, "r")
    output = ""

    for line in infile.readlines():
        all_pos = re.findall(r'[^\s]*\/([^\s]*)', line)
        just_pos = " ".join(all_pos)
        split_plus = re.sub(r"\+", " ", just_pos) # Split up joined tags, e.g. "wanna"
        move_asterisk = re.sub(r"(^|[^\s])\*", " *", split_plus)
        output += move_asterisk + "\n"

    infile.close()
    outfile = open(DATA+outfilename, "w")
    outfile.write(output)
    outfile.close()

def bigram_data(infilename, outfilename):
    "Calculate bigram information from infile and print to outfile"

    infile = open(DATA+infilename, "r")
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

    infile.close()
    outfile = open(DATA+outfilename, "w")
    outfile.write(output)
    outfile.close()


def pos_replace(infilename, outfilename, replacements):
    "Subsitute occurences of certain POS in the infile and print to outfile"

    infile = open(DATA+infilename, "r")
    output = "" # A text file, having made type-substitutions for certain POS

    for line in infile.readlines():
        all_pos = line.split(" ")
        for pos in all_pos:
            if pos in replacements:
                output += replacements[pos] + " "
            else:
                output += pos + " "

    infile.close()
    outfile = open(DATA+outfilename, "w")
    outfile.write(output)
    outfile.close()

def group_runs(infilename, outfilename, regex, replacement):
    "Group together consecutive instances of regex-matched POS and then replace"

    infile = open(DATA+infilename, "r")
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

    infile.close()
    outfile = open(DATA+outfilename, "w")
    outfile.write(output)
    outfile.close()

PREGROUP_REDUCE = [
    r"N Nr",
    r"Nl N",
    r"S Sr",
    r"Sl S"
]

def sentence_reduce(sentence, patterns):
    "Replace any matches in the sentence with the empty string"
    # Relies on random chance
    old = sentence + " "
    new = sentence
    while len(new) < len(old):
        old = new
        random.shuffle(patterns)
        for pattern in patterns:
            new = re.sub(pattern, "", new)
            new = re.sub(r"\s+", " ", new)
            new = new.strip()
    return new

def lazy_measure_sentence(sentence):
    "Compare the counts of types to assess sentence score"

    pos = sentence.split()
    n_inv_count = pos.count("Nl") + pos.count("Nr")
    n_count = pos.count("N")
    s_inv_count = pos.count("Sl") + pos.count("Sr")
    s_count = pos.count("S")
    n_disparity = abs(n_count - n_inv_count)
    s_disparity = abs(s_count - 1 - s_inv_count)
    # The "ideal" sentence reduces to a single S type
    return s_disparity + n_disparity

def lazy_measure(infilename):
    "Apply the lazy measure to each sentence in the file"
    infile = open(DATA+infilename, "r")
    score = 0
    for line in infile.readlines():
        score += lazy_measure_sentence(line)

    infile.close()
    return score

def random_type_balanced():
    "Return a random type, based purely on balance for now."
    n_balance = random.randint(-1, 2)
    s_balance = random.randint(-1, 2)
    n_part = {
        "-1": "Nr N Nl",
        "0": "N Nl",
        "1": "N",
        "2": ""
    }[str(n_balance)]
    s_part = {
        "-1": "Sr S Sl",
        "0": "S Sl",
        "1": "S",
        "2": ""
    }[str(s_balance)]
    if n_part == "" and s_part == "":
        return random_type_balanced()
    elif n_part == "":
        return s_part
    else:
        return n_part + " " + s_part

ASSIGNABLE_POS_FILE = "ASSIGNABLE_POS"

def assignable_pos(count=-1):
    "Get a list of POS, optionally get only the <count> most common."
    infile = open(DATA+ASSIGNABLE_POS_FILE, "r")
    pos_list = []
    if count > 0:
        for line in infile.readlines()[:count]:
            pos_list += [line.strip()]
    else:
        for line in infile.readlines():
            pos_list += [line.strip()]

    infile.close()
    return pos_list

def random_replacements(count=-1, fixed={}):
    """Get the <count> most common POS and offer substitute types.
    Any pos-type specified in <fixed> will have that type returned instead"""
    pos_list = assignable_pos(count)
    replacements = {}
    for pos in pos_list:
        if pos not in fixed:
            replacements[pos] = random_type_balanced()
        else:
            replacements[pos] = fixed[pos]
    return replacements

def replace_random_types_and_score(infilename, outfilename, count=-1):
    "Replace the <count> most common POS with a random type, and APPENDS the score to outfile"
    replacements = random_replacements(count)
    pos_replace(infilename, "TEMP", replacements)
    score = lazy_measure("TEMP")
    output = str(score) + ", "
    for pos in replacements:
        output += replacements[pos] + ", "
    outfile = open(DATA+outfilename, "a")
    outfile.write(output+"\n")
    outfile.close()
