##################################################################################################
## Doomsday Analysis
##################################################################################################

setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

library(tidyverse)
library(scales)

date = read_csv('date_SA.csv', col_names = c('Index', 'Date'), skip = 1)
pub = read_csv('pub_SA.csv', col_names = c('Index', 'Publication'), skip = 1)
text = read_csv('text_SA.csv') %>% rename_with(~ paste0('FT_', .x)) %>% select(-c(FT_...1))
title = read_csv('title_SA.csv') %>% rename_with(~ paste0('Title_', .x)) %>% select(-c(Title_...1))
ac_title = read_csv('actual_title.csv', col_names = c('Index', 'Publication'), skip = 1)
burnet = read_csv('burnet.csv') %>% rename("Burnet" = "0")
doherty = read_csv('doherty.csv') %>% rename("Doherty"="0")
blakely = read_csv('blakely.csv')

doom_df = bind_cols(date$Date, pub$Publication, ac_title$Publication, title, text, burnet$Burnet, 
                    doherty$Doherty, blakely$`0`) %>% 
            rename(c(Date = ...1, Publication = ...2, Title = ...3, Burnet = ...24, 
                     Doherty = ...25, Blake_Thom = ...26)) %>% 
            distinct(Title, .keep_all = T)

doom_df$Burnet <- ifelse(is.na(doom_df$Burnet), 0, 1)

doom_df$Doherty <- ifelse(is.na(doom_df$Doherty), 0, 1)

doom_df$Blake_Thom <- ifelse(is.na(doom_df$Blake_Thom), 0, 1)

doom_df[is.na(doom_df)] <- 0

save(doom_df, file = 'doomsday.RData')

table(doom_df$Burnet, doom_df$Doherty)

x = colSums(doom_df[,c(4:13)], na.rm = T)

##################################################################################################
## Hacky way to reshape to stack the SA and create a column for Text/Title
titledf = doom_df[1:13]
titledf$TextTitle <- 'Title'
names(titledf) <- sub('^Title_', '', names(titledf))
titledf$total <- titledf$positive - titledf$negative
titledf$scotal <- rescale(titledf$total, to = c(0,10))


textdf = doom_df[,c(1:3,14:26)]
textdf$TextTitle <- 'Text'
names(textdf) <- sub('^FT_', '', names(textdf))
textdf$total <- textdf$positive - textdf$negative
textdf$scotal <- rescale(textdf$total, to = c(0,10))

long_doom <- bind_rows(titledf, textdf)

save(long_doom, file='longform doom.csv')
##################################################################################################

an = glm(fear ~ TextTitle, family=binomial, data = long_doom)
table(long_doom$fear)

long_doom$total = long_doom$positive - long_doom$negative

test = long_doom %>% filter(total < 50)

mean(long_doom$scotal)

an = lm(scotal ~ TextTitle, data = test)
summary(an)

x = summary(an)

ggplot(data=long_doom)+
  geom_histogram(aes(x=total), bins = 50)

u = median(long_doom$total)
table(test$scotal)
