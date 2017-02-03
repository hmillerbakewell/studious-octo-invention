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

    weight = 0
    pos = sentence.split()
    n_inv_count = pos.count("Nl") + pos.count("Nr")
    n_count = pos.count("N")
    s_inv_count = pos.count("Sl") + pos.count("Sr")
    s_count = pos.count("S")
    n_disparity = abs(n_count - n_inv_count)
    s_disparity = abs(s_count - 1 - s_inv_count)
    # The "ideal" sentence reduces to a single S type
    # huge advantage to finishing with only one S and all N matched
    if n_disparity == 0 and s_disparity == 0:
        weight -= 10
    weight += pow(s_disparity, 2) + pow(n_disparity, 2)
    return weight

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
    n_balance = random.randint(-1, 1) # For now
    s_balance = random.randint(-1, 1) # For now
    n_part = {
        "-1": "Nl",
        "0": "",
        "1": "N",
        "2": "N Nl"
    }[str(n_balance)]
    s_part = {
        "-1": "Sl",
        "0": "",
        "1": "S",
        "2": "S Sl"
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

def simple_annealing_v1(infilename, num_pos, rounds):
    "Apply the simple annealing algorithm to the lazy measure and balanced type-gen."
    results = []
    fixed = {"nn": "N", "nns": "N"}
    replacements = random_replacements(num_pos, fixed)
    initial_heat = 10000000
    best_score = 10000000
    threshold = lambda x: initial_heat * pow(2, -10*(x/(1.0*rounds)))
    infile = open(DATA+infilename, "r")
    indata = infile.read()
    infile.close()
    for i in range(1, rounds):
        candidate_swaps = random_replacements(num_pos, fixed)
        next_replace = {}
        for key in replacements:
            next_replace[key] = replacements[key]
        rand_pos = random.choice(replacements.keys())
        next_replace[rand_pos] = candidate_swaps[rand_pos]
        score = 0
        for line in indata.splitlines():
            output = ""
            line_pos = line.strip().split(" ")
            for pos in line_pos:
                if pos in next_replace:
                    output += next_replace[pos] + " "
                else:
                    output += pos + " "
            score += lazy_measure_sentence(output)
        keep_change = (score < (best_score + threshold(i)))
        if keep_change:
            for key in replacements:
                replacements[key] = next_replace[key]
            replacements = next_replace
            best_score = min(score, best_score)
        results += [[score, keep_change, rand_pos, str(next_replace)]]
    return results

def example_sentences():
    "Pulls every 999th sentence from the data and evaluates it."
    example_pos = {'vb': 'Nl ', 'vbg': 'Nl ', 'cc': 'Sl', 'np$': 'Nl S', 'ppo': 'S', 'hvd': 'Sl', 'ppss': 'S', 'cd': 'Nl ', 'pps': 'N S', 'ap': 'Nl ', 'hvz': 'Sl', 'at': 'Nl S', 'in': 'Sl', 'cs': 'N ', 'nns': 'N', 'np-tl': 'Sl', 'rp': 'N ', 'nn': 'N', '*': 'Sl', 'abn': 'S', 'to': 'N ', 'rb': 'S', 'np': 'S', 'pn': 'N Sl', 'be': 'S', 'pp$': 'Nl ', 'nn-tl': 'N ', 'hv': 'S', 'wps': 'N S', 'jj': 'Nl S', 'bedz': 'Sl', 'wrb': 'N ', 'dt': 'S', 'md': 'Sl', 'dti': 'S', 'ben': 'Sl', 'vbd': 'Nl Sl', 'vbn': 'Nl ', 'bed': 'Sl', 'bez': 'Sl', 'wdt': 'N ', 'ber': 'Sl', 'vbz': 'Sl', 'jj-tl': 'N ', 'ql': 'Sl'}
    infile = open(DATA+"WORDS_AND_POS", "r")
    indata = infile.read()
    infile.close()
    output = ""
    for line in indata.splitlines()[::999]:
        words_and_pos = line.strip().split(" ")
        word_list = []
        pos_list = []
        if len(words_and_pos) > 2:
            output += "------\n"
            output += line + "\n"
            for word_pos_pair in words_and_pos:
                split = word_pos_pair.split("/")
                word_list += [split[0]]
                pos_list += [split[1]]
            replaced_pos = ""
            for pos in pos_list:
                if pos in example_pos:
                    replaced_pos += " " + example_pos[pos]
                else:
                    replaced_pos += " " + pos
            output += "Replaced: " + replaced_pos + "\n"
            output += "Score: " + str(lazy_measure_sentence(replaced_pos)) + "\n"


    return output
