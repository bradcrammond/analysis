##################################################################################################
## Analysis of the modelling articles in Australia
##################################################################################################

library(tm)
library(tidyverse)
library(rlist)
library(stringi)
library(stringr)

setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

## Read in the text

no1 <- VCorpus(DirSource('newsstream', encoding = 'UTF-8'),
               readerControl = list(language = 'en'))

inspect(no1)




##################################################################################################
## Try and tidy up the files

test = readLines('newsstream/1-100.txt')

titles = str_extract_all(test, "Title:(.*)")

tt = t(as.data.frame(titles %>% 
  flatten() %>% 
  keep(~all(. != 0))))

## publication
pub = str_extract_all(test, "Publication title:(.*)")

pt = t(as.data.frame(pub %>% 
  flatten() %>% 
  keep(~all(. != 0))))

## date
date = str_extract_all(test, "Publication date:(.*)")

dt = t(as.data.frame(date %>% 
                       flatten %>% 
                       keep(~all(. != 0))))

## text

xt <- read_lines('newsstream/list100.txt')

               


x = bind_cols(tt, pt, dt, xt)
