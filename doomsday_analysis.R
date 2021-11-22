##################################################################################################
## Doomsday Predictions Take 2
##################################################################################################

library(tidyverse)

rm(list = ls())

##################################################################################################
## Import the Data

df = read_csv('Modelling_Sentiment.csv') %>% rename('Index'='...1') %>% distinct(title, .keep_all = T)

mean(df$mean_title_sent)
mean(df$text_sentiment)

table(df$publication)

## Remove New Zealand newspapers

df = df %>% filter(!str_detect(publication, 'New Zealand | Timaru | Taranaki'))

## Tidy up the publication names
 # I have manually fixed some of the typos. This isn't ideal if I have to download new articles

df$pub = gsub('(.*);.*', '\\1', df$publication)

table(df$pub)

## Split them into left and right




##################################################################################################
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