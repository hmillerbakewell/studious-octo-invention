"""
Make POS replacements:
nn, nns -> N
jj, at -> N Nl
"""

import conceptual_spaces

NN_JJ_AT_REDUCE = {
    "nn" : "N",
    "nns": "N",
    "jj" : "N Nl",
    "at" : "N Nl"
}

# Make the stated replacements
conceptual_spaces.pos_replace("POS_ONLY", "Round3", NN_JJ_AT_REDUCE)
# Calculate new bigram data
conceptual_spaces.bigram_data("Round3", "Round3_bigrams")
