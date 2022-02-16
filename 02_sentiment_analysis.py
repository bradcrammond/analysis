#################################################################
## Sentiment Analysis of Infectious Disease Modelling in News Media

import os
import re
import pandas as pd
from nrclex import NRCLex
from pandas.core.frame import DataFrame
from nltk import tokenize
from nltk.corpus import stopwords
import numpy as np
import nltk

###############################################################
## Read in the text
with open('data/compile.txt', encoding="utf8") as f:
    lines = f.readlines()

strings = ''.join(lines)    ## convert to string

###############################################################
## 
##                 Extract the relevant fields
##
###############################################################

## Title
title = re.findall("Title:(.*)", strings)

## Extract Publication 
pub = re.findall("Publication title:(.*)", strings)

## Date
date = re.findall("Publication date:(.*)", strings)

## Extract full text
txt = re.findall("(?s)(Full text:.*?)(?:(?:\\r*\\n){2}|(?:IN OTHER NEWS)|(?:READ MORE:)|(?:^How today unfolded))", strings)

## Get rid of the 'Full text:' bit at the start
txtn = []
for string in txt:
    new_string = string.replace("Full text:", "")
    txtn.append(new_string)

txt = txtn

df = pd.DataFrame(title)
df = df.rename(columns={0:'title'})
df['publication'] = pub
df['date'] = date

####################################################################################
## Check the results          

## Make sure everything still includes the search terms
r = re.compile(".*(modelling).*", re.IGNORECASE)
ftxt = list(filter(r.search, txt))

check = list(set(txt) - set(ftxt))  ## which articles don't have 'modelling'

exclude = np.zeros([len(txt),1])    ## create an index of articles

for i in range(len(txt)):
    exclude[i] = txt[i] in check    ## now there is a list where '0' means keep
                                    ## and '1' means exclude.

df['exclude'] = exclude

####################################################################################
##
##                      Processing the Full Text
##
####################################################################################

## Separate into sentences
tk = []
for i in range(len(txt)):
    tk.insert(i, tokenize.sent_tokenize(txt[i]))

## Number of words per sentence
a = len(tk)
b = max(map(len, tk))
swd = np.zeros([a,b])

for i in range(len(tk)):                            ## Takes 3 minutes, relax
    for j in range(len(tk[i])):
        x = len(tokenize.word_tokenize(tk[i][j]))
        swd[i][j] = x

## Mean words per sentence per article

mwps = np.zeros([a,1])          ## storage

t = np.sum(swd, axis=1)         ## get number of words in article

for i in range(len(swd)):
    y = len(tk[i])             ## get the number of sentences
    mwps[i] = t[i] / y         ## get average words per sentence

df['MWPS'] = mwps


## Next is to remove stop words and then get a new count of the sentence
stopw = np.zeros([a,b])

for i in range(len(tk)):                            ## Takes another 3 mins
    for j in range(len(tk[i])):
        w = tokenize.word_tokenize(tk[i][j])
        sw = len([d for d in w if d in stopwords.words('english')])
        stopw[i][j] = sw

## Mean non-stop words per sentence per article

mstopwps = np.zeros([a,1])          ## storage

u = np.sum(stopw, axis=1)         ## get number of words in article

for i in range(len(swd)):
    y = len(tk[i])             ## get the number of sentences
    mstopwps[i] = u[i] / y         ## get average words per sentence

df['MStopWPS'] = mstopwps

## Number of sentence per article
sentence_per_article = np.zeros([a,1])

for i in range(len(tk)):
    sentence_per_article[i] = len(tk[i])

df['sentence_per_article'] = sentence_per_article

## So now we have:
#  the full text in one list (txt) 
# it split into sentences in another (tk)
# the count of the words in the sentence (swd)
# the count of stopwords per sentence (stopw)

## Check for mention of Burnet
bt = []
for i in range(len(txt)):
    bt.insert(i, re.findall('Burnet', txt[i]))

btdf = pd.DataFrame(bt)
bb = btdf.iloc[:, 0]
df['Burnet'] = bb

## Check for mention of Doherty
dy = []
for i in range(len(txt)):
    dy.insert(i, re.findall("Doherty", txt[i]))

dydf = pd.DataFrame(dy)
dd = dydf.iloc[:,0]
df['Doherty'] = dd

## Check for mention of Blakely | Thompson
bltm = []
for i in range(len(txt)):
    bltm.insert(i, re.findall("Blakely|Thompson", txt[i]))

bldf = pd.DataFrame(bltm)
bl = bldf.iloc[:,0]
df['BlakelyThompson'] = bl

df.to_csv('cleaned_text.csv')

#############################################################################
## Lemmatization

from nltk.corpus import wordnet as wn

sent_score = np.zeros([a,b])       ## positive - negative sentiment
fear_score = np.zeros([a,b])       ## count of fear words
emot_count = np.zeros([a,b])       ## count of words in the sentence that are actually used for the sentiment analysis

## Loop through the database, lemmatize and get sentiment scores
for i in range(len(tk)):
    for j in range(len(tk[i])):

        k = tokenize.word_tokenize(tk[i][j])
        c = []
        for l in range(len(k)):
            z = wn.morphy(k[l])
            c.insert(l, z)
            if pd.isna(c[l]):
                c[l] = k[l]
            
            d = ' '.join(c)
        
        sent = NRCLex(d)
        emo = sent.raw_emotion_scores           ## extract scores
        
        if 'fear' in emo:                       ## record fear (if there)
            fear_score[i][j] = emo['fear']
        else:
            fear_score[i][j] = 0
                                                ## record positive - negative
        if all(key in emo for key in ('positive', 'negative')): 
            sent_score[i][j] = emo['positive'] - emo['negative']
        elif 'positive' in emo:
            sent_score[i][j] = emo['positive']
        elif 'negative' in emo:
            sent_score[i][j] = 0 - emo['negative']
        else:
            sent_score[i][j] = 0

        emot_count[i][j] = len(sent.affect_dict) ## count number of senti words



np.savetxt('count of emotion words per sentence.csv', emot_count, delimiter=',')

np.savetxt('sentiment score per sentence.csv', sent_score, delimiter=',')

np.savetxt('fear score per sentence.csv', fear_score, delimiter=',')

## Last (maybe) I need the sentiment score divided by the number of words in the sentence (not including stop words)

sent_on_stop = np.zeros([a,b])

for i in range(len(tk)):
    for j in range(len(tk[i])):
        sent_on_stop[i][j] = sent_score[i][j] / (swd[i][j] - stopw[i][j])

ms = np.sum(sent_on_stop, axis=1)

mean_sent = np.zeros([a,1])

for i in range(len(tk)):
    mean_sent[i] = ms[i] / len(tk[i])


## Histogram to check the shape of it - looks quite nicely spread out.
# n, bins, patches = plt.hist(x=mean_sent, bins='auto', color='#0504aa',
#                             alpha=0.7, rwidth=0.85)
# plt.grid(axis='y', alpha=0.75)
# plt.xlabel('Value')
# plt.ylabel('Frequency')
# plt.title('Average Sentiment of Articles')
# maxfreq = n.max()

df['text_sentiment'] = mean_sent




##################################################################################################
## Now the titles

title_sent = np.zeros([a,1])       ## positive - negative sentiment
title_fear = np.zeros([a,1])
twd = np.zeros([a,1])   ## number of words in title
title_emot_count = np.zeros([a,1])       ## count of words in the sentence that are actually used for the sentiment analysis

for i in range(len(title)):

    k = tokenize.word_tokenize(title[i])
    twd[i] = len(k)

    c = []
    ## Lemmatize
    for l in range(len(k)):
        z = wn.morphy(k[l])
        c.insert(l, z)
        if pd.isna(c[l]):
            c[l] = k[l]
            
        d = ' '.join(c)

    ## Sentiments
    sent = NRCLex(d)
    emo = sent.raw_emotion_scores           ## extract scores
    
    if 'fear' in emo:                       ## record fear (if there)
        title_fear[i] = emo['fear']
    else:
        fear_score[i] = 0
                                            ## record positive - negative
    if all(key in emo for key in ('positive', 'negative')): 
        title_sent[i] = emo['positive'] - emo['negative']
    elif 'positive' in emo:
        title_sent[i] = emo['positive']
    elif 'negative' in emo:
        title_sent[i] = 0 - emo['negative']
    else:
        title_sent[i] = 0

        title_emot_count[i] = len(sent.affect_dict) ## count number of senti words


## Next is to remove stop words and then get a new count of the sentence
ttopw = np.zeros([a,1])

for i in range(len(title)):
    w = tokenize.word_tokenize(title[i])
    sw = len([d for d in w if d in stopwords.words('english')])
    ttopw[i] = sw

df['title_word_count'] = twd
df['title_stop_words'] = ttopw

df['title_sent'] = title_sent
df['title_fear'] = title_fear

nonstop = twd - ttopw

mean_title_sent = title_sent / nonstop

df['mean_title_sent'] = mean_title_sent

df.to_csv('data/Modelling_Sentiment.csv')