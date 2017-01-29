"""
Assess a randomized type assigment
"""

import conceptual_spaces

def append_new_random_score(infilename, outfilename, count):
    "Append score information for a random type assignment"
    replacements = conceptual_spaces.random_replacements(count)
    conceptual_spaces.pos_replace(infilename, "TEMP", replacements)
    score = conceptual_spaces.lazy_measure("TEMP")
    output = str(score) + ", "
    for pos in replacements:
        output += replacements[pos] + ", "
    outfile = open(conceptual_spaces.DATA+outfilename, "a")
    outfile.write(output+"\n")
    outfile.close()

append_new_random_score("POS_ONLY", "Round6", 2)
