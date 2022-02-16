##################################################################################################
## Doomsday Predictions Take 2
##################################################################################################

library(tidyverse)
library(xlsx)

rm(list = ls())

setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
#######################################################
## Import the Data

df <- read_csv("data/Modelling_Sentiment.csv") %>% rename("Index" = "X1")

## Drop everything that isn't about modelling

df <- df %>% dplyr::filter(exclude == 0)

df <- df %>% distinct(title, .keep_all = T)


table(df$publication)

## Remove New Zealand newspapers
nz = c("New Zealand", "Timaru", "Taranaki")
df <- df %>% filter(!str_detect(publication, paste(nz, collapse = "|")))

## Tidy up the publication names
 # I have manually fixed some of the typos.
 # This isn't ideal if I have to download new articles

## Remove the trailing place of publication
df$pub <- gsub("(.*);.*", "\\1", df$publication)

## Also drop the 'Online'
df$pub <- gsub("( \\(Online\\))", "", df$pub)
df$pub <- gsub("( \\(Onli ne\\))", "", df$pub)

table(df$pub)

## Split them into left, right and ABC
x <- data.frame(table(df$pub))

write_csv(x, file = "publications.csv")

owners <- read_csv('csv/publications.csv')

hope = dplyr::left_join(df, owners, by = 'pub')
hope$Owner <- NULL

df = hope

table(df$owner)

## Number of mastheads per outlet
nc <- df %>% dplyr::filter(owner == "Murdoch")
n <- table(nc$pub)

acm <- df %>% dplyr::filter(owner == "ACM")
a <- table(acm$pub)

ffx <- df %>% dplyr::filter(owner == "Fairfax")
f <- table(ffx$pub)
####################################################################################
save(df, file = "doomsday.RData")

load("doomsday.RData")

###############################################################
## The infectious disease models

# 3 models: Burnet, Doherty, Blakely

# Categories are:
  # 0 Doherty only
  # 1 Burnet only
  # 2 Blakely only
  # 3 Doherty + Burnet
  # 4 Doherty + Blakely
  # 5 Burnet + Blakely
  # 6 All 3

df$Doherty = if_else(is.na(df$Doherty), 0, 1)
df$Burnet = if_else(is.na(df$Burnet), 0, 1)
df$BlakelyThompson = if_else(is.na(df$BlakelyThompson), 0, 1)


df$models[df$Doherty == 1 & df$Burnet == 0 & df$BlakelyThompson == 0] <- 0
df$models[df$Doherty == 0 & df$Burnet == 1 & df$BlakelyThompson == 0] <- 1
df$models[df$Doherty == 0 & df$Burnet == 0 & df$BlakelyThompson == 1] <- 2
df$models[df$Doherty == 1 & df$Burnet == 1 & df$BlakelyThompson == 0] <- 3
df$models[df$Doherty == 1 & df$Burnet == 0 & df$BlakelyThompson == 1] <- 4
df$models[df$Doherty == 0 & df$Burnet == 1 & df$BlakelyThompson == 1] <- 5
df$models[df$Doherty == 1 & df$Burnet == 1 & df$BlakelyThompson == 1] <- 6

table(df$models)

df$catmodels <- factor(df$models)

save(df, file = "doomsday.RData")
