## Descriptives

def pos_neg(entry):
    return entry

"Covid Qld: Latest case numbers revealed as authorities deal with scares in Cairns and Toowoomba"

1 negative and 2 positive

tester = "Lockdown exit at risk after record virus tally"
test = tokenize.word_tokenize(tester)

for i in range(len(test)):
    emotion = NRCLex(test[i])
    print('\n\n', test[i], ': ', emotion.top_emotions)
    print('\n\n', test[i], ': ', emotion.raw_emotion_scores)

x = list(NRCLex, test)

y = x.raw_emotion_scores

