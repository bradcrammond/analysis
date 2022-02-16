#############################################################
## Cheap and nasty first estimate

load("doomsday.RData")

########################################################

est = lm(text_sentiment ~ mean_title_sent, data = df)

summary(est)

ggplot(data = df) +
  geom_point(aes(x = text_sentiment, y = mean_title_sent))

fest <- lm(text_sentiment ~ mean_title_sent + owner + catmodels, data = df)
summary(fest)

########################################################
## Proper analysis

pest = lm(text_sentiment ~ Owner + catmodels + MWPS, data = df)

summary(pest)

mest = lm(text_sentiment ~ catmodels + MWPS, data = df)
summary(mest)

## Just Fairfax
ddf = df %>% dplyr::filter(df$Owner == 'Fairfax')

xest = lm(text_sentiment ~ catmodels + MWPS, data = ddf)
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
  geom_histogram(aes(x="text_sentiment"), stat = 'count')
