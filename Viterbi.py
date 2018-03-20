#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 14:32:30 2018

@author: tharunngolthi
"""
import sys
def Viterbi(Obs,states,start_prob,trans_prob,emit_prob):
    viterbi = [[0]*len(Obs) for _ in range(len(states))]
    backpointer = {}
    for state in range(0,len(states)):
        viterbi[state][0] = start_prob[states[state]] * emit_prob[states[state]][Obs[0]]
        backpointer[state] = [state]
    for t in range(1, len(Obs)):
        p = {}        
        for s in range(0,len(states)):
            (viterbi[s][t],state) = max((viterbi[s2][t-1]*trans_prob[states[s2]][states[s]]*emit_prob[states[s]][Obs[t]],s2) for s2 in range(0,len(states)))
            p[s] = backpointer[state]+[s]
        backpointer = p
    final_probability,final_state = max((viterbi[s][t], s) for s in range(0,len(states)))
    return (final_probability,backpointer[final_state])
    

if __name__ == '__main__':
    states = ('Hot', 'Cold')
    observations = sys.argv[1]
    start_probability = {'Hot': 0.8, 'Cold': 0.2}
    transition_probability = {
       'Hot' : {'Hot': 0.7, 'Cold': 0.3},
       'Cold' : {'Cold': 0.6, 'Hot': 0.4}
       }
    emission_probability = {
       'Hot' : {'1': 0.2, '2': 0.4, '3': 0.4},
       'Cold' : {'1': 0.5, '2': 0.4, '3': 0.1}
       }
    prob, prob_states = Viterbi(observations,states,start_probability,transition_probability,emission_probability)
    print ("Final probability =",prob)
    print ("states",end=" = ")
    for i in prob_states:
        print(states[i],end=",")
    print()