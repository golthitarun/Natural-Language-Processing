#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 14:59:29 2018

@author: tharunngolthi
"""
import pandas
import sys

class Bigrams():
    def __init__(self,f):
        self.bigram_freq = {}
        self.word_freq = {}
        self.N_c = {}
        self.GT_count = {}
        self.smoothing = False
        prev_word = None
        
        for line in f:
            for word in line.split():
                if prev_word != None:
                    self.bigram_freq[(prev_word,word)] = self.bigram_freq.get((prev_word,word),0)+1
                self.word_freq[word] = self.word_freq.get(word,0)+1
                prev_word = word
        self.unique_bigrams_len = len(self.bigram_freq)
        self.unique_words_len = len(self.word_freq)
        self.total_sum_bigrams = sum(self.bigram_freq.values())
        self.N0 = (self.unique_words_len)**2 - self.unique_bigrams_len
        for bigram in self.bigram_freq:
            self.N_c[self.bigram_freq[bigram]] = self.N_c.get(self.bigram_freq[bigram],0)+1
        for i in self.N_c:
            if self.N_c[i] != 0:
                self.GT_count[i] = (i+1)*(self.N_c.get(i+1,0))/(self.N_c.get(i,0))
                
        self.GT_count[0] = self.N_c[1]/self.N0

    def bigram_probability(self,prev_word,word):
        numerator = self.bigram_freq.get((prev_word,word),0)
        denominator = self.word_freq.get(prev_word,0)
        if self.smoothing:
            numerator +=1
            denominator +=self.unique_words_len
        
            
        if numerator == 0 or denominator == 0:
            return 0.0
        else:
            return float(numerator)/float(denominator)
    
    def good_turing_probability(self,prev_word,word):
        
        numerator = self.GT_count.get(self.bigram_freq.get((prev_word,word),0),0)
        denominator = self.total_sum_bigrams
        if self.bigram_freq.get((prev_word,word),0) == 0:          
            denominator = sum(bigram_model.bigram_freq.values())
        if numerator == 0 or denominator == 0:
            return 0.0
        else:
            return float(numerator)/float(denominator)
        

def print_bigram_count(sentence,bigram_model,GT = False):
    words = sentence.split()
    header = ["Bigram ","Count"]
    rows = []

    prev_word = None
    for word in words:   
        if prev_word != None:
            if GT:
                rows.append([(prev_word,word),bigram_model.GT_count.get(bigram_model.bigram_freq.get((prev_word,word),0),0)])
            elif bigram_model.smoothing:
                rows.append([(prev_word,word),bigram_model.bigram_probability(prev_word,word)*bigram_model.word_freq.get(prev_word,0)])
            else:                
                rows.append([(prev_word,word),bigram_model.bigram_freq.get((prev_word,word),0)])
        prev_word = word
    print (pandas.DataFrame(rows,columns=header))
    
    
def print_bigram_probabilities(sentence,bigram_model,GT = False):
        header = [" "]
        words = sentence.split()   
        header = ["Bigram ","Probability"]
        rows = []
        prev_word = None
        for word in words:   
            if prev_word != None:
                if GT:
                    rows.append([(prev_word,word),"%.9f" %bigram_model.good_turing_probability(prev_word,word)])
                else:                    
                    rows.append([(prev_word,word),"%.4f" %bigram_model.bigram_probability(prev_word,word)])     
            prev_word = word
        '''for word1 in words:
            row = [word1]
            for word2 in words:  
                if GT:
                    row.append("%.4f" %bigram_model.good_turing_probability(word1,word2))
                else:                    
                    row.append("%.4f" %bigram_model.bigram_probability(word1,word2))                      
            rows.append(row)'''
        print (pandas.DataFrame(rows,columns=header))
        
def total_probability(sentence,bigram_model,GT=False):
    words = sentence.split()
    prev_word = None
    total_prob = 1
    for word in words:
        if prev_word !=None:
            if GT:
                total_prob *= bigram_model.good_turing_probability(prev_word,word)
            else:               
                total_prob *=bigram_model.bigram_probability(prev_word,word)
        prev_word = word
    print ("Total Probability: ",total_prob)
            

if __name__ == '__main__':
        filename = sys.argv[1]       
        f = open(filename, 'r')
        bigram_model = Bigrams(f)
        BigramFreq = open('BigramFrequencies.txt', 'w')
        
        for item in bigram_model.bigram_freq:
            BigramFreq.write((str(item)+" - "+str(bigram_model.bigram_freq[item])+"\n"))
        BigramFreq.close()
        print("*************************************************************",end="\n\n")
        print(" 1. Total Bigrams Count of Corpus = ", bigram_model.total_sum_bigrams,end="\n\n")
        print("    Unique Bigrams Count of Corpus = ", len(bigram_model.bigram_freq),end="\n\n")
        
        print("Enter the sentence for computation below")
        
        sentence = input()
   
        print("********************** No Smoothing *************************",end="\n\n")
        print ("==================== BIGRAMS COUNTS ==================")
        print_bigram_count(sentence,bigram_model)
        print ("==================== BIGRAMS PROBABILITIES ==================")      
        print_bigram_probabilities(sentence,bigram_model)
        print ("==================== SENTENCE PROBABILITY ==================") 
        total_probability(sentence,bigram_model)
        bigram_model.smoothing = True
        print (end ="\n\n")
        print("********************** Smoothing *************************",end="\n\n")
        print ("==================== BIGRAMS COUNTS ==================")
        print_bigram_count(sentence,bigram_model)
        print ("==================== BIGRAMS PROBABILITIES ==================")      
        print_bigram_probabilities(sentence,bigram_model)      
        print ("==================== SENTENCE PROBABILITY ==================") 
        total_probability(sentence,bigram_model)
        print (end ="\n\n")
        print("********************** Good Turning Smoothing *************************",end="\n\n")
        print ("==================== BIGRAMS COUNTS ==================")
        print_bigram_count(sentence,bigram_model,True)
        print ("==================== BIGRAMS PROBABILITIES ==================")      
        print_bigram_probabilities(sentence,bigram_model,True)      
        print ("==================== SENTENCE PROBABILITY ==================")        
        total_probability(sentence,bigram_model,True)

        
        
        
        
        