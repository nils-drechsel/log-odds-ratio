#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 15:07:25 2020

@author: nils
"""


import argparse
import progressbar
import csv
import sys
from LogOddsRatio.CorpusDictionary import CorpusDictionary
from LogOddsRatio.CorpusDictionary import create_from_csv

csv.field_size_limit(sys.maxsize)



parser = argparse.ArgumentParser(description="create dictionary with word frequencies")
parser.add_argument("--input", help="input csv and columns", action="append", nargs='+', metavar="N", required=True)
parser.add_argument("--dictionary", default = None, help="dictionary csv which will be used as a base", required=False)
parser.add_argument("--output", help="dictionary csv", required=True)
parser.add_argument("--poor_mans_stemming", default = None, type = int, help="whether to employ poor man's stemming (cut term length to n characters)", required=False)
parser.add_argument("--min_term_length", default = None, type = int, help="only include terms with at least that many characters", required=False)
parser.add_argument("--dont_lowercase", default = False, dest="dont_lowercase", action='store_true', help="whether to turn off lowercasing")
args = parser.parse_args()

file_out = args.output
stemming = args.poor_mans_stemming
if stemming < 0: raise Exception("stemming must be larger than 0")
min_term_length = args.min_term_length
lowercase = not args.dont_lowercase
file_dictionary = args.dictionary

inputs = args.input
for inp in inputs:
    if len(inp) < 2:
        raise Exception("each input needs at least 2 arguments: first the file name, then names of each column to use")



n_rows = 0
bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)        

def update_bar(i):
    global n_rows
    n_rows += 1
    bar.update(n_rows)


if file_dictionary is not None:
    dictionary = create_from_csv(file_dictionary, "term", "n", stemming = stemming, lowercase = lowercase, callback = update_bar)
else:
    dictionary = CorpusDictionary(stemming, lowercase, min_term_length)


n_rows = 0
bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)     

for inp in inputs:
    columns = inp[1:len(inp)]
    dictionary.add_terms_in_csv(inp[0], columns, quoting=csv.QUOTE_MINIMAL, callback = update_bar)
        
dictionary.write_to_dictionary_csv(file_out)
    