#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 14:25:45 2020

@author: aarav
"""
#ham count on 0 index
#spam count on 1 index

import math

"""---------------------------------------------------------------------------"""
fname = input("Enter the name of the train file:\n" ) 
s_w = input("Enter the Stop Words File name: \n")
stop_words = []
# s_w = "StopWords.txt"
f_h = open(s_w,'r')
text = f_h.readline()
while (text != ""):
    stop_words.append(text.strip())
    text = f_h.readline()
# for removing the 
stop_words = [x for x in stop_words if x!='']
stop_words = set(stop_words)

f_h.close()

"""---------------------------------------------------------------------------"""
def cleantext(text):
    text = text.lower()
    text = text.strip()
    for letters in text:
        if (letters in """[]!.,"-!—@;':#$%^&*()+/?"""):
            text = text.replace(letters, " ")
    return text

"""---------------------------------------------------------------------------"""
def countwords(text, is_spam, counted):
    for each_word in words:
        if each_word in counted:
            if is_spam == 1:
                counted[each_word][1]=counted[each_word][1] + 1
            else:
                counted[each_word][0]=counted[each_word][0] + 1
        else:
            if is_spam == 1:
                counted[each_word] = [0,1]
            else:
                counted[each_word] = [1,0]
    return counted

"""---------------------------------------------------------------------------"""
def make_percent_list(k, theCount, spams, hams): 
    for each_key in theCount:
        theCount[each_key][0] = (theCount[each_key][0] + k)/(2*k+hams)
        theCount[each_key][1] = (theCount[each_key][1] + k)/(2*k+spams) 
    return theCount

"""---------------------------------------------------------------------------"""
def test(s,v,s_w,n_s,n_h):
    
    total = n_s + n_h
    
    ps = n_s/total
    pns = 1-ps
    
    s = cleantext(s) 
    ws = s.split()
    ws = set(ws)
    ws = ws.difference(s_w)
    sp,nt_sp = 0,0
    
    for i in v:
        if i in ws:
            sp = sp + math.log(v[i][1])
            nt_sp = nt_sp + math.log(v[i][0])
        else:
            sp = sp + math.log(1-v[i][1])
            nt_sp = nt_sp + math.log(1-v[i][0])
            
    nr = sp + math.log(ps)
    nr = math.exp(nr)
    
    dr = nt_sp + math.log(pns)
    dr = math.exp(dr)  

    return(nr/(nr+dr))         
        
"""---------------------------------------------------------------------------"""
# Training step to get the Vocabulary Dictionary
spam = 0
ham = 0
counted = dict()

# fname = "SHTrain.txt"
fin = open(fname, encoding='utf-8-sig')
textline = fin.readline()
while (textline != ""):
    is_spam = int(textline[:1])
    if is_spam == 1:
        spam = spam + 1
    else :
        ham = ham + 1
    textline = cleantext(textline[1:])
    words = textline.split()
    words = set(words)
    words = words.difference(stop_words)
    counted = countwords(words, is_spam, counted) 
    textline = fin.readline()
vocab_train = make_percent_list(0.1, counted, spam, ham)
fin.close()
print(f"\nVocabulary Created using the Training File\n")

"""---------------------------------------------------------------------------"""
# Testing Step
fname = input("Enter the Test File name: \n")
# fname = "SHTest.txt"
fin = open(fname, encoding='utf-8-sig')
textline = fin.readline()
tp, tn, fp, fn = 0, 0, 0, 0
spam_test, ham_test = 0, 0
# Checking the end of the file
while textline != "":
    is_spam = int(textline[:1])
    if is_spam == 1:
        spam_test = spam_test + 1
    else :
        ham_test = ham_test + 1
    temp = textline[1:]
    res = test(temp,vocab_train,stop_words,spam,ham)
    if (res > 0.5): 
        res = 1
    else:
        res = 0

    if(res==1 and is_spam==1):
        tp+=1
    elif(res==0 and is_spam==0):
        tn+=1
    elif(res==1 and is_spam==0):
        fp+=1
    else:
        fn+=1
    textline = fin.readline()
    
fin.close()

print(f"\nTotal number of Spam emails in the test file: {spam_test}")
print(f"\nTotal number of Ham emails in the test file: {ham_test}\n")
print(f"\nTrue Positive = {tp}\nTrue Negative = {tn}\nFalse Positive = {fp}\nFalse Negative = {fn}")
    
accuracy,precision,recall,f1 = 0.,0.,0.,0.

accuracy = (tp+tn)/(tp+tn+fp+fn)
precision = (tp)/(tp+fp) 
recall = (tp)/(tp+fn)
f1 = 2/((1/precision)+(1/recall))

print(f"\nAccuracy = {accuracy}\nPrecision = {precision}\nRecall = {recall}\nF1 Score = {f1}")

print ("\t\t\t\tPredicted Class")
print ("\t\t\t -------------------------")
print("\t\t\t |\t |N \t |Y\t|")
print ("\t\t\t -------------------------")
print(f"\tActual Class\t |N\t |{tn}\t |{fp}\t|")
print ("\t\t\t -------------------------")
print(f"\t\t\t |Y\t |{fn}\t |{tp}\t|")
print ("\t\t\t -------------------------")


"""---------------------------------------------------------------------------"""