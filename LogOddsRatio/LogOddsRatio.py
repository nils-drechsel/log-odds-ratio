#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 21:07:32 2020

@author: nils
"""


from LogOddsRatio.CorpusDictionary import CorpusDictionary
import math

class LogOddsRatio:
    """
    Calculates the log odds ratio using an uninformative prior
    Monroe et al. http://languagelog.ldc.upenn.edu/myl/Monroe.pdf
    """
             
    
    def __init__(self, dictionary):
        if not isinstance(dictionary, CorpusDictionary):
            raise TypeError("dictionary must be of type CorpusDictionary")
        self.dictionary = dictionary
    
                
    def calculate_from_dictionary(self, document_dictionary):
        """

        Parameters
        ----------
        document_dictionary : CorpusDictionary

        Returns
        -------
            A python dict of terms and log odd ratios.

        """
        
        res = {}
    
        n_corpus = self.dictionary.get_total_term_count()
        n_doc = document_dictionary.get_total_term_count()
        
        for term in document_dictionary.get_terms():
            
            
            if not self.dictionary.contains(term):
                continue
            
            word, corpus_freq = self.dictionary.get_dictionary_entry(term)
            doc_freq = document_dictionary.get_term_count(term)
            
            not_term = n_corpus - n_doc
            term_ratio = (doc_freq + corpus_freq) / ((n_corpus + n_doc) - (doc_freq + corpus_freq))
            not_term_ratio = (not_term + corpus_freq) / ((not_term + n_corpus) - (not_term + corpus_freq))
            sigma2 = 1.0/(doc_freq + corpus_freq) + 1.0/(not_term + corpus_freq)
            log_odds = (math.log(term_ratio) - math.log(not_term_ratio)) / math.sqrt(sigma2)
            res[word] = log_odds
        
        return res
        
        
    
    
    
    