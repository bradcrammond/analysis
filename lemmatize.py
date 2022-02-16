

sent_score = np.zeros([a,b])       ## positive - negative sentiment
fear_score = np.zeros([a,b])       ## count of fear words
emot_count = np.zeros([a,b])       ## count of words in the sentence that are actually used for the sentiment analysis

for i in range(len(tk)):
    for j in range(len(tk[i])):

        k = tokenize.word_tokenize(tk[i][j])
        c = []
        for l in range(len(k)):
            z = wn.morphy(k[l])
            c.insert(l, z)
            if pd.isna(c[l]):
                c[l] = k[l]
            
            d = ' '.join(c)
        
        sent = NRCLex(d)
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
