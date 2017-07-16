
###################################
# CS B551 Fall 2016, Assignment #3
#
# Your names and user ids:
# 1 . Vaishnavi Mukundhan -- vaismuku
# 2 . Bhavesh Reddy Merugureddy-- Bmerugur
# 3 . Yuanjie Li -- yuanli 
# (Based on skeleton code by D. Crandall)
#
#
#########################################################
## READ ME
##########################################################
# 1. Description of the problem formulation:
#  General Abstraction ::
#    1. O(0).....O(n)== Words of a sentence which requires pos tagging to be done
#    2. Q(0).....Q(n)== sequence of parts of speech ['x','noun','pron','adv','adj','prt','verb','num','.','adp','conj','det']
#    3. Goal State == Each word has a appropriate POS associated with it.
#    4. Probability of initial state Probability (Q(0))
#    5. Transition probability == Probability of going from one state to another .
#       i.e Probability of a verb following a noun.. etc. Probability(Q(n+1|Q(n)0
#    6. Emission Probability == Probability of a given Q producing a word.
#       i.e P(and|conj) where and is the word and POS is conjunction
#
# 2. How does the program work?
#    Part 1: Calculated the emission probability, Transition probability, Probability of states
#    Part 2: Calculated the parts of speech tag for each word in the sentence considering each word to be independent
#            of each other. Used the emission and Probability of states that was found in part 1 of the problem
#            for this calculation.
#    Part 3:  Using the probabilities that were calculated in Part 1, we use a viterbi table to store the previously
#            calculated probabilities for each and every state.
#            To calculate the probability of (w|s) we maximize the previous state probability and transmission probability
#               from that state to the current state. Thus every state depends on the probability of the previous state.
#    Part 4: Posterior probability of each algorithm is calculated different for each algorithm. 
#           Posterior probability is given to the base of 10.
#           For ground truth: when the word's probability is not trained set probability, it is taken as default 1.0.
#           (As ground truth probability is the correct prbability)
#           For the rest of the algorithms it's as per the calculated probability. ###P(s1,s2,s3|l1,l2,l3..)=P(s1)*P(s1|l1)*P(s2|s1)
#   Part 5: Complex module: Similar to hmm with an additional transition probability from P(si|si-2)along with P(si|si-1)
#
#
# 3.Discussion of any problems, assumptions, simplifications, and/or design decisions you made;
#   Problems: No problems
#   Assumptions: problem is well defined, didn't need to make any
#   Simplifications: problem is well defined, didn't need to make any
#
# 4. Results for bc.test
# So far scored 2000 sentences with 29442 words.
#                    Words correct:     Sentences correct:
#    0. Ground truth:      100.00%              100.00%
#      1. Simplified:       90%                 32%
#             2. HMM:       88%                 28%
#         3. Complex:       79%                 12%
#
##############################################################
from __future__ import division

import random
import math
import itertools

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
from collections import Counter



class Solver:

    def __init__(self):
        self.s1_probabilities={}
        self.probability_s2_given_si={}
        self.probability_wi_given_si={}
        self.count_s2 = ['x','noun','pron','adv','adj','prt','verb','num','.','adp','conj','det']

    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling
    def posterior(self, sentence, label, algo):
        posterior={}
        ##Posterior for simplified
        posterior_simplified=self.simplified(sentence)
        count=1.0
        if algo == "1. Simplified":
            for i in posterior_simplified[1][0]:
                count=count*i
            posterior[algo]=math.log(count,10)
        elif algo =="0. Ground truth":
            for j,s in itertools.izip(range(0,len(label)-1),range(0, len(sentence)-1)):
               count=self.s1_probabilities.get(label[s])*self.probability_wi_given_si.get((label[j],sentence[s]),1.0)*self.probability_s2_given_si.get((label[s-1],label[s]),1.0)
            posterior[algo]=math.log(count,10)
        elif algo =="2. HMM":
            for j,s in itertools.izip(range(0,len(label)-1),range(0, len(sentence)-1)):
                count=self.s1_probabilities.get(label[s])*self.probability_wi_given_si.get((label[j],sentence[s]),0.0000000001)*self.probability_s2_given_si.get((label[s-1],label[s]),0.00000000001)
            posterior[algo]=math.log(count,10)
        else:
            for j,s in itertools.izip(range(0,len(label)-1),range(0, len(sentence)-1)):
                count=self.s1_probabilities.get(label[s])*self.probability_wi_given_si.get((label[j],sentence[s]),0.0000000001)*self.probability_s2_given_si.get((label[s],label[s-1]),0.00000000001)*self.probability_s2_given_si.get((label[s],label[s-2]),0.00000000001)
            posterior[algo]=math.log(count,10)
        return posterior[algo]
       

    def calculate_s1_probabilities(self,data):
        count_s1=[]
        for i in range(0,len(data[1])): result=[test[1] for test in data]
        for i in result: count_s1.append(i[0])
        count_s1= dict(Counter(count_s1))##http://stackoverflow.com/questions/11068986/change-data-frame-from-counter-to-dict
        for key in count_s1: self.s1_probabilities[key]=(count_s1[key]/sum(count_s1.values()))
        return self.s1_probabilities

    def calc_probability_s2_given_si(self,data):
        count_si2_given_si1={}
        result={}
        temp=[]
        for i in range(0,len(data[1])): result=[test[1] for test in data]
        for j in range(0,len(result)-1 ):
            for i in range(0,len(result[j])-1):
                key=(result[j][i-1],result[j][i])
                if key not in count_si2_given_si1.keys(): count_si2_given_si1[(result[j][i-1],result[j][i])]=1
                else: count_si2_given_si1[(result[j][i-1],result[j][i])]+=1
        total_count=0
        for j in self.count_s2:
            for i in range (0,len((count_si2_given_si1))-1):
                if count_si2_given_si1.keys()[i][1]==j:temp.append(count_si2_given_si1.keys()[i])
                for n in range(0,len(temp)):
                     total_count=total_count+count_si2_given_si1.get(temp[n])
                     self.probability_s2_given_si[count_si2_given_si1.keys()[i]]=float(count_si2_given_si1.get(temp[n])/total_count)
            temp=[]
            total_count=0
        return self.probability_s2_given_si

    def calculate_probability_wi_given_si(self,data):
        wi_si=[]
        total_count=0
        temp=[]
        j=0
        for i in range(0,len(data)) :
            for k in range (0,len(data[i][j])):
                key=data[i][j][k],data[i][j+1][k]
                wi_si.append(key)
        count_wi_si=dict(Counter(wi_si))
        for j in self.count_s2:
            for i in count_wi_si:
                if i[1]==j:temp.append(i)
            for x in temp:
                 total_count=total_count+count_wi_si.get(x)
                 self.probability_wi_given_si[x]=float(count_wi_si.get(x)/total_count)
            temp=[]
            total_count=0
        return self.probability_wi_given_si

    # Do the training!
    #
    def train(self, data):
        temp=[]
        for i in range(0,len(data[1])): result=[test[1] for test in data]
        s1_probabilities= self.calculate_s1_probabilities(data)
        probability_s2_given_si=self.calc_probability_s2_given_si(data)
        probability_wi_given_si= self.calculate_probability_wi_given_si(data)
        return s1_probabilities,probability_s2_given_si,probability_wi_given_si

    # Functions for each algorithm. in
    #
    def simplified(self,sentence):
        max_si={}
        max_probability={}
        s_list=[]
        list=[]
        for w in sentence:
            for i in self.count_s2:
                max_si[w,i]= self.probability_wi_given_si.get((w,i),0.0000000001)*self.s1_probabilities[i]
            key, value = max(max_si.iteritems(), key=lambda x:x[1]) ####http://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
            (w,s)=key
            s_list.append(s)
            max_probability[key]=value
            max_si.clear()
        for i in s_list:list.append(i)
        return [ [list,], [max_probability.values(), ]]

    def hmm(self, sentence):
        viterbi={}
        temp={}
        max_probability={}
        word_probability_value={}
        state={}
        list=[]
        for w in range (0,len(sentence)):
            for i in range (0,len(self.count_s2)):
                if w==0:
                    viterbi[w,self.count_s2[i]]=self.probability_wi_given_si.get((sentence[w],self.count_s2[i]),0.0000000001)*self.s1_probabilities.get((self.count_s2[i]),0.0000000001)
                    max_probability[w,self.count_s2[i]]=viterbi[w,self.count_s2[i]]
                else:
                    for k in range (1,len(self.count_s2)):
                        temp[w,self.count_s2[i],self.count_s2[k]]=viterbi.get(((w-1),self.count_s2[k]),0.0000000001)*self.probability_s2_given_si.get((self.count_s2[i],self.count_s2[i-1]),0.0000000001)
                    key,value=max(temp.iteritems(), key=lambda x:x[1])
                    word,curr_state,previous_state=key
                    viterbi[word,curr_state]=value*self.probability_wi_given_si.get((sentence[w],self.count_s2[i]),0.0000000001)
                    max_probability[word,curr_state]=viterbi[word,curr_state]
                    temp.clear()
            key1,value1=max(max_probability.iteritems(), key=lambda x:x[1])
            (w,s)=key1
            state[w]=s
            word_probability_value[w]=value1
            max_probability.clear()
        for i in state.values(): list.append(i)
        return [ [ list, ], [] ]

    def complex(self, sentence):
        ve={}
        temp={}
        max_probability={}
        word_probability_value={}
        state={}
        list=[]
        for w in range (0,len(sentence)):
            for i in range (0,len(self.count_s2)):
                if w==0:
                    ve[w,self.count_s2[i]]=self.probability_wi_given_si.get((sentence[w],self.count_s2[i]),0.0000000001)*self.s1_probabilities.get((self.count_s2[i]),0.0000000001)
                    max_probability[w,self.count_s2[i]]=ve[w,self.count_s2[i]]
                else:
                    for k in range (1,len(self.count_s2)):
                        temp[w,self.count_s2[i],self.count_s2[k]]=ve.get(((w-1),self.count_s2[k]),0.0000000001)*self.probability_s2_given_si.get((self.count_s2[i],self.count_s2[i-1]),0.0000000001)*self.probability_s2_given_si.get((self.count_s2[i],self.count_s2[i-2]),0.0000000001)
                    key,value=max(temp.iteritems(), key=lambda x:x[1])
                    word,curr_state,previous_state=key
                    ve[word,curr_state]=value*self.probability_wi_given_si.get((sentence[w],self.count_s2[i]),0.0000000001)
                    max_probability[word,curr_state]=ve[word,curr_state]
                    temp.clear()
            key1,value1=max(max_probability.iteritems(), key=lambda x:x[1])
            (w,s)=key1
            state[w]=s
            word_probability_value[w]=value1
            max_probability.clear()
        for i in state.values(): list.append(i)
        return [ [ list, ], [] ]

    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It's supposed to return a list with two elements:
    #
    #  - The first element is a list of part-of-speech labelings of the sentence.
    #    Each of these is a list, one part of speech per word of the sentence.
    #
    #  - The second element is a list of probabilities, one per word. This is
    #    only needed for simplified() and complex() and is the marginal probability for each word.
    #
    def solve(self, algo, sentence):
        if algo == "Simplified":
            return self.simplified(sentence)
        elif algo == "HMM":
            return self.hmm(sentence)
        elif algo == "Complex":
            return self.complex(sentence)
        else:  print "Unknown algo!"
