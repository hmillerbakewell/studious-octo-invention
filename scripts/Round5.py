"""
Make POS replacements:
Possessives -> N Nl
"""

import conceptual_spaces

POSSESSIVES_REDUCE = {
    r"nn$" : "N Nl", # 	possessive singular noun
    r"nns$" : "N Nl", #  	possessive plural noun
    r"np$" : "N Nl", #  	possessive proper noun
    r"nps$" : "N Nl", #  	possessive plural proper noun
    r"pn$" : "N Nl", #  	possessive nominal pronoun
    r"pp$" : "N Nl", #  	possessive personal pronoun (my, our)
    r"pp$$" : "N Nl", #  	second (nominal) possessive pronoun (mine, ours)
    r"prp$" : "N Nl", # 	Possessive pronoun
    r"wp$" : "Nr N Sl" #  	possessive wh- pronoun (whose)
}

# Make the stated replacements
conceptual_spaces.pos_replace("Round4", "Round5", POSSESSIVES_REDUCE)
# Calculate new bigram data
conceptual_spaces.bigram_data("Round5", "Round5_bigrams")
