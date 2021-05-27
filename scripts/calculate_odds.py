#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 18:23:49 2020

@author: nils
"""



import argparse
import progressbar
import csv
import codecs
import sys
from LogOddsRatio.CorpusDictionary import CorpusDictionary
from LogOddsRatio.LogOddsRatio import LogOddsRatio
from LogOddsRatio.CorpusDictionary import create_from_csv
from LogOddsRatio.CorpusDictionary import strip
csv.field_size_limit(sys.maxsize)



def write_odds(writer, document_name, corpus_dictionary, document_dictionary, log_odds):
                    
    odds = log_odds.calculate_from_dictionary(document_dictionary)
    for term, log_odds in sorted(odds.items(), key=lambda x: x[1], reverse=True):
        
        writer.writerow([document_name, term, corpus_dictionary.get_term_count(term), document_dictionary.get_term_count(term), log_odds])



parser = argparse.ArgumentParser(description="create dictionary with word frequencies")
parser.add_argument("--dictionary", help="dictionary csv", required=True)
parser.add_argument("--input", help="input csv and columns", action="append", nargs='+', metavar="N", required=True)
parser.add_argument("--output", help="dictionary csv with log odd ratios", required=True)
parser.add_argument("--poor_mans_stemming", default = None, type = int, help="whether to employ poor man's stemming (cut term length to n characters)", required=False)
parser.add_argument("--dont_lowercase", default = False, dest="dont_lowercase", action='store_true', help="whether to turn off lowercasing")
args = parser.parse_args()

file_out = args.output
stemming = args.poor_mans_stemming
if stemming < 0: raise Exception("stemming must be larger than 0")
lowercase = not args.dont_lowercase
file_dictionary = args.dictionary

inputs = args.input
for inp in inputs:
    if len(inp) < 3:
        raise Exception("each input needs at least 3 arguments: first the file name followed by the name of the document, then names of each column to use")

print("reading dictionary")

n_rows = 0
bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)        

def update_bar(i):
    global n_rows
    n_rows += 1
    bar.update(n_rows)

corpus_dictionary = create_from_csv(file_dictionary, "term", "n", stemming = stemming, lowercase = lowercase, callback = update_bar)
log_odds = LogOddsRatio(corpus_dictionary)

print("\n")

print("processing files")

n_rows = 0
bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)        

with codecs.open(file_out, "w", "utf-8") as f_out:
    writer = csv.writer(f_out, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["document", "term", "n_corpus", "n_document", "log_odds"])
    
    for inp in inputs:
        with codecs.open(inp[0], "r", "utf-8") as f_in:
            reader = csv.reader(f_in, quoting=csv.QUOTE_ALL)
            
            name_column = inp[1]
                
            columns = inp[2:len(inp)]
            
            index_name = None
            indexes = []
            
            for i, row in enumerate(reader):
                if i == 0:
                    for j, col in enumerate(row):
                        if strip(col) in columns:
                            indexes.append(j)
                        if strip(col) == name_column:
                            index_name = j
                            
                    if len(indexes) != len(columns):
                        raise Exception("columns for "+filename+" are incorrect")                            
                            
                    continue
                
                document_dictionary = CorpusDictionary(stemming = stemming, lowercase = lowercase)
                
                for j in indexes:
                    document_dictionary.add_terms_in_text(row[j])
                    
                write_odds(writer, row[index_name], corpus_dictionary, document_dictionary, log_odds)
                   
                n_rows += 1
                bar.update(n_rows)
        
