#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 01:41:01 2018

@author: tharunngolthi
"""
from collections import Counter
import sys

def findError(sentenceTags1, sentenceTags2):
    errortags = 0
    for i in range(len(sentenceTags1)):
        if sentenceTags1[i][1] != sentenceTags2[i][1]:
            errortags +=1
    return (float(errortags)/float(len(sentenceTags1)))
    
def printHelp(sentenceTags):
    for i in sentenceTags:
        print (i[0]+"_"+i[1], end=" ")

def getBestInstance():
    Rules = Counter()
    FromTo_PrevWordsTags = {}
    count = 0
    for fromTag in Tags:
        for toTag in Tags:
            if fromTag == toTag:
                continue
            else:
                FromTo_PrevWordsTags[(fromTag,toTag)] = {T:0 for T in Tags}
                for pos in range(1,len(currentTags)):
                    if correctTags[pos][1] == toTag and currentTags[pos][1] == fromTag:
                        FromTo_PrevWordsTags[(fromTag,toTag)][currentTags[pos-1][1]] +=1
                    elif correctTags[pos][1] == fromTag and currentTags[pos][1] == fromTag:
                        FromTo_PrevWordsTags[(fromTag,toTag)][currentTags[pos-1][1]] -=1
                for prevTag in FromTo_PrevWordsTags[(fromTag,toTag)]:
                    if FromTo_PrevWordsTags[(fromTag,toTag)][prevTag] > 0:
                        count +=1
                        Rules[(fromTag,toTag,prevTag)] = FromTo_PrevWordsTags[(fromTag,toTag)][prevTag]
    return Rules

if __name__ == '__main__':
    fileInputPath = sys.argv[1]
    f = open(fileInputPath, 'r')
    data = f.read()
    word_tags = data.split()
    WordTagCount = {}
    Tags = set()
    CountPrevnCurrTags = {}
    CountTags = {}
    prev_Tag = None
    for word_tag in word_tags:
        word = word_tag.split("_")[0]
        tag = word_tag.split("_")[1]
        if len(Tags) < 50:
            Tags.add(tag)
        if word in WordTagCount:
            WordTagCount[word][tag] = WordTagCount[word].get(tag,0) + 1
        else:
            WordTagCount[word] = {}
            WordTagCount[word][tag] = 1
        if prev_Tag !=None:
            CountPrevnCurrTags[(prev_Tag,tag)] = CountPrevnCurrTags.get((prev_Tag,tag),0) + 1
        prev_Tag = tag
        CountTags[tag] = CountTags.get(tag,0)+1
   
    
    # Brills transformation based POS Tagging
    # Step-1 Initialize the tags to most probable.
    currentTags = []
    correctTags = []
    TotalTags = len(word_tags)
    wrongTags = 0
    for word_tag in word_tags:
        word = word_tag.split('_')[0]
        tag = word_tag.split('_')[1]
        max_value = max(WordTagCount[word].values())
        if max_value == 0:
            currentTag = "NN"
        else:
            for key in WordTagCount[word]:
                if WordTagCount[word][key] == max_value:
                    currentTag = key
        currentTags.append((word,currentTag))
        correctTags.append((word,tag))
        if tag != currentTag:
            wrongTags +=1
    error = float(wrongTags)*100/float(TotalTags)
    
    print("Initial Error after intitializing with most probable tags: %.2f" %error," %")
    
   
    # Rules -> ((FROM_TAG, TO_TAG, PREVIOUS_WORD_TAG), SCORE)
    Rules = getBestInstance().most_common()
    
    print ("Rules learnt from corpus, format:((FROM_TAG, TO_TAG, PREVIOUS_WORD_TAG), SCORE)",end="\n\n")
    
    RulesFile = open('Rules.txt', 'w')
    RulesFile.write(("Rules learnt from corpus, format:FROM_TAG, TO_TAG, PREVIOUS_WORD_TAG, SCORE \n"))
    for item in Rules:
        RulesFile.write((item[0][0] +"," +item[0][1]  +"," + item[0][2]+ "," +str(item[1])+"\n"))
    RulesFile.close()
    
    
    # Applying Brills and Naive Bayes Tagging to a given sentence.
    sentence = "The_DT president_NN wants_VBZ to_TO control_VB the_DT board_NN 's_POS control_NN"
    sentenceWords = sentence.split()
    sentenceWordTags = []
    Original_sentenceWordTags = []
    for word_tag in sentenceWords:
        word = word_tag.split('_')[0]
        tag = word_tag.split('_')[1]
        Original_sentenceWordTags.append((word,tag))
        max_value = max(WordTagCount[word].values())
        if max_value == 0:
            currentTag = "NN"
        else:
            for key in WordTagCount[word]:
                if WordTagCount[word][key] == max_value:
                    currentTag = key
        sentenceWordTags.append([word,currentTag])
 
    #Train on rules 5 times or until error is less than 0.1
    i = 0
    while(i<5 and findError(sentenceWordTags,Original_sentenceWordTags) > 0.1):
        for i in range(1,len(sentenceWordTags)):
            for rule in Rules:
                if rule[0][2] == sentenceWordTags[i-1][1]:
                    if rule[0][0] == sentenceWordTags[i][1]:
                        sentenceWordTags[i][1] = rule[0][1]
        i +=1
                    
    

    # Naive Bayes Based POS tagging.
    # Getting Tag transition probabilities counts and Word likelihood probabilities counts.
    NB_sentenceWordTags = []
    NB_sentenceTags = []
    for word_tag in sentenceWords:
        word = word_tag.split('_')[0]
        if word in WordTagCount:
            NB_sentenceTags.append(list(WordTagCount[word].keys()))
        else:
            NB_sentenceTags.append(list('NN'))
        NB_sentenceWordTags.append([word,None])
    combinations = [[]]
    for x in NB_sentenceTags:
        combinations = [ i + [y] for y in x for i in combinations ]
    
    # Calculating probabilities for all the different possible combinations of POS tags.
    comb_prob = []
    for i,j in enumerate(combinations):
        num = WordTagCount.get(sentenceWords[0].split('_')[0],0).get(j[0],0)
        den = CountTags.get(j[0],0)
        if num == 0 or den == 0:
            comb_prob.append(0)
        else:
            comb_prob.append(float(num)/float(den))

    for i,j in enumerate(combinations):
        totalprob = 1
        for t in range(1,len(j)):
            num1 = WordTagCount.get(sentenceWords[t].split('_')[0],0).get(j[t],0)
            den1 = CountTags.get(j[t],0)
            num2 = CountPrevnCurrTags.get((j[t-1],j[t]),0)
            den2 = CountTags.get(j[t],0)
            if num1 == 0 or num2 ==0 or den1 ==0 or den2==0:
                totalprob = 0
                break
            else:
                totalprob = totalprob * (float(num1)/float(den1)) *(float(num2)/float(den2))
        comb_prob[i] = comb_prob[i] * totalprob
    
    #Assigning the highest probable tags to the given sentence.
    m = 0
    max_index = 0
    for i in range(0,len(combinations)):
        if comb_prob[i] > m:
            m = comb_prob[i]
            max_index = i
    
    for i,j in enumerate(combinations[max_index]):
        NB_sentenceWordTags[i][1] = j
        
    print ("**************** Manual POS Tagged Sentence *************************")
    print()
    print (sentence, end="\n\n")
    print ("***************** Brills POS Tagged Sentence **************************")
    print()
    printHelp(sentenceWordTags)
    print(end="\n\n")
    print ("Error compared with Manual POS Tags : ",findError(sentenceWordTags,Original_sentenceWordTags),"%", end="\n\n")
    print ("************** Naive Bayes POS Tagged Sentence ************************")
    print()
    printHelp(NB_sentenceWordTags)
    print(end="\n\n")
    print ("Error compared with Manual POS Tags : ",findError(NB_sentenceWordTags,Original_sentenceWordTags),"%", end="\n\n")
    
    
    
        
    
    
    
    