"""
Get frequency data on 2-grams
"""
#!/usr/bin/env python
# Python 2.7
# Round 4


import Round2

INPUT = open("../data_files/Round4", "r")
OUTPUT = open("../data_files/Round4_2grams", "w")

Round2.bigram_data(INPUT, OUTPUT)
