##################################################################################################
## Doomsday Predictions Take 2
##################################################################################################

library(tidyverse)
library(xlsx)

rm(list = ls())

setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
#######################################################
## Import the Data

df <- read_csv("Modelling_Sentiment.csv") %>% rename("Index" = "...1")

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

x = table(df$pub)

## Split them into left, right and ABC
x <- data.frame(table(df$pub))

write_csv(x, file = "publications.csv")

owners <- read_csv('publications.csv')

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


#############################################################
## Cheap and nasty first estimate

est = lm(mean_sent ~ mean_title_sent, data = df)

summary(est)

ggplot(data = df) +
  geom_point(aes(x = mean_sent, y = mean_title_sent))

fest <- lm(mean_sent ~ mean_title_sent + Owner + catmodels, data = df)
summary(fest)

########################################################
## Proper analysis

pest = lm(mean_sent ~ Owner + catmodels + MWPS, data = df)

summary(pest)

mest = lm(mean_sent ~ catmodels + MWPS, data = df)
summary(mest)

## Just Fairfax
ddf = df %>% dplyr::filter(df$Owner == 'Fairfax')

xest = lm(mean_sent ~ catmodels + MWPS, data = ddf)
summary(xest)

##################################################################
## Another nasty estimate

df2 = df[,c('Index', 'mean_title_sent', 'MWPS')]
df2$Sentiment = df2$mean_title_sent
df2$Title_Text = 'Title'

df3 = df[,c('Index', 'mean_sent', 'MWPS')]
df3$Sentiment = df3$mean_sent
df3$Title_Text = 'Text'

dff = bind_rows(df2, df3)

y = glm(Sentiment ~ Title_Text, data = dff)

summary(y)

ggplot(data = df)+
  geom_histogram(aes(x="mean_sent"), stat = 'count')
  