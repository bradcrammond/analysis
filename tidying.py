##################################################################################
## Let's try regex in python
#%%
import os
import re
import pandas as pd
from nrclex import NRCLex

## Set and change directory
os.getcwd()
#%%
## Mac
os.chdir("/Users/bradleycrammond/Dropbox/Work Projects/HTL/Writing/doomsday/analysis/newsstream")
#%%
## Windows
os.chdir("/Users/bradc/Dropbox/Work Projects/HTL/Writing/doomsday/analysis/newsstream")

##################################################################################
## Read in the text
with open('1-100.txt', encoding="utf8") as f:
    lines = f.readlines()

strings = ''.join(lines)    ## convert to string

#%%
## Extract full text and don't convert to df anymore
txt = re.findall("(?s)(Full text:.*?)(?:(?:\\r*\\n){2})", strings)
## df = pd.DataFrame (txt, columns = ['text'])

## Extract Title and covert to df
title = re.findall("Title:(.*)", strings)
tdf = pd.DataFrame (title, columns = ['title'])

## Extract Publication 
pub = re.findall("Publication title:(.*)", strings)
pdf = pd.DataFrame (pub, columns = ['publication'])

## Date

date = re.findall("Publication date:(.*)", strings)
ddf = pd.DataFrame (date, columns = ['date'])

## Put together

combined_df = pd.concat([tdf, pdf, ddf, df], axis=1, ignore_index=True)

combined_df.to_csv('py_test.csv')

combined_df.style


ddf.head(5)



with open('100.txt', 'w') as f:
    f.writelines(txt)

import json
with open('list100.txt', 'w') as f:
    json.dump(txt, f)

print(txt)
type(txt)
