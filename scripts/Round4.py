"""
Grouping together of Proper Nouns
"""
import conceptual_spaces

# Replace (multi-word) titles with "TL"
# See amendment for why this is commented out
# conceptual_spaces.group_runs(INPUT, TEMPOUT, r'^\w*-tl$', "TL")

# Replace (multi-word) proper nouns and plural proper nouns with "P"
conceptual_spaces.group_runs("Round3", "Round4", r'^nps?$', "P")

conceptual_spaces.bigram_data("Round4", "Round4_bigrams")
