"""
Get frequency data on 2-grams
"""
#!/usr/bin/env python
# Python 2.7
# Round 2


import Round2

INPUT = open("../data_files/Round3_repl", "r")
OUTPUT = open("../data_files/Round3_2grams", "w")

Round2.bigram_data(INPUT, OUTPUT)
