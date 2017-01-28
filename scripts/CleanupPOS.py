"""
Create a file containing only the POS tags from the corpus
"""
#!/usr/bin/env python
# Python 2.7


import re # Regular expressions


manb = open("../data_files/WORDS_AND_POS","r")
outfile = open("../data_files/POS_ONLY","w")
output = ""

for line in manb.readlines():
    all_pos = re.findall(r'[^\s]*\/([^\s]*)', line)
    just_pos = " ".join(all_pos)
    split_plus = re.sub(r"\+", " ", just_pos) # Split up joined tags, e.g. "wanna"
    move_asterisk = re.sub(r"(^|[^\s])\*", " *", split_plus)
    output += move_asterisk + "\n"

outfile.write(output)