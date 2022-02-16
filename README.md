## Sentiment Analysis of Australian Newspaper Articles on Infectious Disease Modelling of COVID-19;

1. Need all the relevant articles in `/newsstream`
2. Run `01_files.py` to put everything into one file (`data/compile.txt`)

3. Then run `02_sentiment_analysis.py.`
 - This outputs `Modelling_Sentiment.csv` to `data`

4. There is some data cleaning to do before the stats can be run
 - `03_data_prep.R` cleans up the publication names and adds the publication owners

5. The statistical analysis is performed in R.
 - work through `04_statistical_analysis.R`

5. And that's it!