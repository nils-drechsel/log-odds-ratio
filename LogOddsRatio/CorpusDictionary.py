#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 15:26:18 2020

@author: nils
"""

import re
import codecs
import csv

import string



class CorpusDictionary:
    """
        Represents a dictionary of terms within a corpus of text
    """
    
    def __init__(self, stemming = None, lowercase = True, min_term_length = None):
        """
        Parameters
        ----------
        stemming : int
            If 0, no stemming is performed. Otherwise poor man's
                stemming is performed by only keeping n characters of the word.
        lowercase : bool
            whether to lowercase the terms.
        min_term_length : int
            If 0, no restriction is applied. Otherwise specifies
                the minimum number of characters necessary to be included in the
                count.

        Returns
        -------
        None.

        """
        self.terms = {}
        self.stemming = stemming
        self.lowercase = lowercase
        self.min_term_length = min_term_length
        self.n = 0
        
        
    def stem_term(self, term):
        if self.stemming is not None:
            term = term[0: self.stemming]
        return term
        
    def lowercase_term(self, term):
        if self.lowercase:
            term = term.lower()
        return term
    
    def process_term(self, term):
        term = self.lowercase_term(term)
        term = self.stem_term(term)
        return term
            
        
    def add_term(self, term, count = 1):
        
        if self.min_term_length is None or len(term) >= self.min_term_length:        
            
            term = self.lowercase_term(term)
        
            unstemmed_term = term
            
            term = self.stem_term(term)
                
            if term not in self.terms:
                self.terms[term] = [unstemmed_term, count]
            else:
                self.terms[term][1] += count
                
            self.n += count


    def add_terms_in_text(self, text):
        """
        Adds words found in text into the dictionary

        Parameters
        ----------
        text : string
            A text, document, etc.

        Returns
        -------
        None.

        """
        
        document = re.findall(r'[a-zA-Z]+', text)
        for term in document:
            self.add_term(term)
            
    def add_terms_in_csv(self, filename, columns, quoting=csv.QUOTE_ALL, callback = None):
        with codecs.open(filename, "r", "utf-8") as f:
            reader = csv.reader(f, quoting = quoting)
            
            indexes = []
            print("columns: "+str(columns))
            for i, row in enumerate(reader):
                if i == 0:
                    for j, col in enumerate(row):
                        
                        if strip(col.strip()) in columns:
                            indexes.append(j)
                            
                    if len(indexes) != len(columns):
                        raise Exception("columns for "+filename+" are incorrect")
                    continue
                
                for j in indexes:
                    self.add_terms_in_text(row[j])
                    
                if callback is not None:
                    callback(i)
                    
    def write_to_dictionary_csv(self, filename):
        with codecs.open(filename, "w", "utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["stem", "term", "n"])
            for stem, info in sorted(self.terms.items(), key=lambda x: x[1][1], reverse=True):
                writer.writerow([stem, info[0], info[1]])
         
    def get_term_count(self, term):
        term = self.process_term(term)
        
        if term not in self.terms:
            return None
        
        return self.terms[term][1]
    
    def get_dictionary_term(self, term):
        term = self.process_term(term)
        
        if term not in self.terms:
            return None
        
        return self.terms[term][0]
    
    
    def get_dictionary_entry(self, term):
        term = self.process_term(term)
        
        if term not in self.terms:
            return None
        
        return (self.terms[term][0], self.terms[term][1])
        
    def contains(self, term):
        term = self.process_term(term)
        return term in self.terms


    def get_terms(self):
        return self.terms.keys()
        
    def get_total_term_count(self):
        return self.n
    
    
    
def create_from_csv(file_name, column_term, column_n, stemming = None, lowercase = True, min_term_length = None, callback = None):

    dictionary = CorpusDictionary(stemming, lowercase, min_term_length)
    
    with codecs.open(file_name, "r", "utf-8") as f:
        reader = csv.reader(f, quoting=csv.QUOTE_MINIMAL)
        
        index_term = None
        index_n = None
        
        for i, row in enumerate(reader):
            if i == 0:
                for j, col in enumerate(row):
                    if col == column_term:
                        index_term = j
                    if col == column_n:
                        index_n = j
                        
                if index_term is None or index_n is None:
                    raise Exception("term or count columns were not found")
                        
                continue
            
            dictionary.add_term(row[index_term], int(row[index_n]))
                
            if callback is not None:
                callback(i)
    
    return dictionary
    
    
    
    
def strip(s):
    return ''.join(filter(lambda c: c in string.printable, s))