#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 13:14:10 2018

@author: tharunngolthi
"""
from nltk.corpus import wordnet as wn
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

def SimplifiedLesk(word, sentence):
    best_sense = None
    max_overlap = 0
    word = wn.morphy(word)
    senses = wn.synsets(word)
    for sense in senses:
        overlap = ComputeOverlap(sense,sentence)
        for hyponyms in sense.hyponyms():
            overlap += ComputeOverlap(hyponyms,sentence)
        
        if overlap > max_overlap:
                max_overlap = overlap
                best_sense = sense  
    return best_sense

def ComputeOverlap(synset, sentence):
    gloss = synset.definition()
    gloss = set(tokenizer.tokenize(gloss))
    for example in synset.examples():
        gloss=gloss.union(example)
    gloss = gloss.difference(stopwordset)
    
    sentence = set(sentence.split(" "))
    gloss=gloss.intersection(sentence)
    return len(gloss)

    
    
tokenizer = RegexpTokenizer('\w+')
stopwordset = set(stopwords.words('english'))

if __name__ == '__main__':
    sentence = input("Enter sentence:")
    word = input("Enter word:")
    lesk = SimplifiedLesk(word,sentence)
    print ("**************************", end = "\n")
    print("Final Chosen Sense:", end=" ")
    if lesk is not None:
        print (lesk)
        print ("Definition: ",lesk.definition(), end = "\n")
        print ("Examples:")
        for i in lesk.examples():
            print ("=> ",i)