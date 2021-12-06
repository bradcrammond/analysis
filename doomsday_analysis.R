##################################################################################################
## Doomsday Predictions Take 2
##################################################################################################

library(tidyverse)
library(xlsx)

rm(list = ls())

setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
#######################################################
## Import the Data

df <- read_csv("Modelling_Sentiment.csv") %>% rename("Index" = "X1")

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

table(df$pub)

## Split them into left, right and ABC
x <- data.frame(table(df$pub))

write_csv(x, file = "publications.csv")

murdoch <- read.xlsx("publications.xlsx", sheetName = "Murdoch")

x <- is.element(df$pub, murdoch)
table(x)
###############################################################
## The infectious disease models

##################################################################################################
## Cheap and nasty first estimate

est = lm(text_sentiment ~ mean_title_sent, data = df)

summary(est)

ggplot(data = df)+
  geom_point(aes(x=text_sentiment, y=mean_title_sent))

##################################################################################################
## Another nasty estimate

df2 = df[,c('Index', 'mean_title_sent')]
df2$Sentiment = df2$mean_title_sent
df2$Title_Text = 'Title'

df3 = df[,c('Index', 'text_sentiment')]
df3$Sentiment = df3$text_sentiment
df3$Title_Text = 'Text'

dff = bind_rows(df2, df3)

y = glm(Sentiment ~ Title_Text, data = dff)

summary(y)

ggplot(data = dff)
  geom_