##################################################################################
## Let's try regex in python

import os
import re
import pandas as pd
from nrclex import NRCLex
from pandas.core.frame import DataFrame
from nltk import tokenize
from nltk.corpus import stopwords
import numpy as np
import nltk

##################################################################################
## Read in the text
with open('compile.txt', encoding="utf8") as f:
    lines = f.readlines()

strings = ''.join(lines)    ## convert to string


## Extract full text
txt = re.findall("(?s)(Full text:.*?)(?:(?:\\r*\\n){2}|(?:IN OTHER NEWS:)|(?:READ MORE:)|(?:^How today unfolded))", strings)

## txt = [(a) for (a,b,c,d) in txt] 
## Needed this before I figured out how to stop at in other news.

txtn = []
for string in txt:
    new_string = string.replace("Full text:", "")
    txtn.append(new_string)

txt = txtn


## Separate into sentences
tk = []
for i in range(len(txt)):
    tk.insert(i, tokenize.sent_tokenize(txt[i]))

## Number of words per sentence
a = len(tk)
b = max(map(len, tk))
swd = np.zeros([a,b])

for i in range(len(tk)):
    for j in range(len(tk[i])):
        x = len(tokenize.word_tokenize(tk[i][j]))
        swd[i][j] = x

## Next is to remove stop words and then get a new count of the sentence
stopw = np.zeros([a,b])

for i in range(len(tk)):
    for j in range(len(tk[i])):
        w = tokenize.word_tokenize(tk[i][j])
        sw = len([d for d in w if d in stopwords.words('english')])
        stopw[i][j] = sw

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
bb.to_csv('burnet.csv')

## Check for mention of Doherty
dy = []
for i in range(len(txt)):
    dy.insert(i, re.findall("Doherty", txt[i]))

dydf = pd.DataFrame(dy)
dd = dydf.iloc[:, 0]
dd.to_csv('doherty.csv')

## Check for mention of Blakely | Thompson
bltm = []
for i in range(len(txt)):
    bltm.insert(i, re.findall("Blakely|Thompson", txt[i]))

bltmdf = pd.DataFrame(bltm)
bl = bltmdf.iloc[:,0]
bl.to_csv('blakely.csv')


## Extract Title
title = re.findall("Title:(.*)", strings)


## Extract Publication 
pub = re.findall("Publication title:(.*)", strings)

## Date
date = re.findall("Publication date:(.*)", strings)

#############################################################################################
## Using NRC

# Run the sentiment analysis on the full text
txt_output = list(map(NRCLex, txt))
# empty list
txt_emotion = []
# Pull the raw emotion scores into their own list
for i in range(len(txt_output)):
    txt_emotion.insert(i, txt_output[i].raw_emotion_scores)

## This is fine, but it gives a total score for each article, when what I need is the score for each sentence.

sent_score = np.zeros([a,b])       ## positive - negative sentiment
fear_score = np.zeros([a,b])       ## count of fear words
emot_count = np.zeros([a,b])       ## count of words in the sentence that are actually used for the sentiment analysis

for i in range(len(tk)):
    for j in range(len(tk[i])):
        sent = NRCLex(tk[i][j])                 ## get the sentiment
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


##################################################################################################
## Now the titles
title_output = list(map(NRCLex, title))

title_emotion = []

for i in range(len(title_output)):
    title_emotion.insert(i, title_output[i].raw_emotion_scores)

## Put it all together for analysis
actual_title = pd.DataFrame(title)
title_df = pd.DataFrame(title_emotion)
text_df = pd.DataFrame(txt_emotion)
date_df = pd.DataFrame(date)
pub_df = pd.DataFrame(pub)

actual_title.to_csv('actual_title.csv')
title_df.to_csv('title_SA.csv')
text_df.to_csv('text_SA.csv')
date_df.to_csv('date_SA.csv')
pub_df.to_csv('pub_SA.csv')