# %%
#
# COSC2671 Social Media and Network Analytics
# @author Aidan Cowie, 2019
#

import re
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import string
import nltk
import warnings 
import sys
import json
from collections import Counter
from wordcloud import WordCloud
import codecs
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from colorama import Fore, Back, Style
from urllib.parse import urlparse
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.decomposition import NMF
warnings.filterwarnings("ignore", category=DeprecationWarning)
%matplotlib inline
from os import listdir
# %%
# Get list of json files in directory

repos_to_query = [
    # ['torvalds', 'linux'], # no issues enabled on github
    # ['apache', 'spark'], # no issues enabled on github
    # ['django', 'django'], # no issues enabled on github
    
    ['ipython', 'ipython'],
    ['nodejs', 'node'],
    ['keras-team', 'keras'], # GOT IT
    ['tensorflow', 'tensorflow'], # GOT IT
    ['pandas-dev', 'pandas'],
    ['scikit-learn', 'scikit-learn'],
    ['tidyverse', 'ggplot2'],
    ['tidyverse', 'tidyverse'],
]

FILENAME = '/Users/phil/code/data-science-next/uni/social-media/ass02_datascience_social_network_analysis/packages/server/data/processed/data-merged-issues.json'

# %%
# Put all json data into dictionary
data = {}
tmp = json.loads(open(FILENAME, encoding="utf-8").read())

type(tmp)

[k for k in tmp.keys()]

for key, value in tmp.items():
    # print(value)
    print(key)
    print(type(value))

for k in tmp.keys(): #reaching the keys of dict
    for x in tmp[k]: #reaching every element in tuples
        try:
            print(x)
            print(type(x))
        except:
            pass


for key, value in tmp.items():
    print(key)
    print(value['data'])
    # value['data']['repository']['issues']['edges'][1]['node']['title']
    
    value['ipython']
    
    foo = value.get('tensorflow')
    print(foo)


tmp.items()

tmp['ipython']['data']['repository']['issues']['edges'][1]['node']['title']

tmp.key()

for ix in repos_to_query:
    ix[0]
    print(ix[0])
    print(tmp[ix])
    # print(repos_to_query[ix][0])
    # data[ix] = tmp[ix]
    # ['repository']['ref']['target']['history']['edges']
    # tmp = json.loads(open(file, encoding="utf-8").read())
    # data[file_names[ix]] = tmp['data']['repository']['ref']['target']['history']['edges']
# %%
df= pd.DataFrame(columns=['Repo',
                          'Message Headline', 
                          'Message',
                          'Date'])
for repo in data:
    ix = 0
    while ix < len(data[repo]):
        try:
#             print(data[repo][ix]['node']['messageHeadline'])
            df = df.append({'Repo': repo,
                            'Message Headline': data[repo][ix]['node']['messageHeadline'], 
                            'Message': data[repo][ix]['node']['message'], 
                            'Date': data[repo][ix]['node']['author']['date']} , ignore_index=True)
        except:
            pass
        ix += 1
# %%
df['Date'] = pd.DatetimeIndex(pd.to_datetime(df['Date'], utc=True))
# .dt.strftime('%Y-%m-%d %H:%M:%S')
df.head()
# %%
df['Message'][0]
# %%
# Creating a time series for the amount of tweets per hour
time_count = pd.DataFrame(columns=['datetime'])
time_count['datetime'] = df['Date']
time_count_resize = time_count.resample('d', on='datetime').count()
ax = time_count_resize.plot()
ax.set_xlabel("Date Time")
ax.set_ylabel("Count")
ax.legend(["Commits"])
# %%
for repo in data:
    print(repo)
# %%
#burst technieque ?
topic0 = df['Repo']=='django'
dftopic0 = df[topic0]
topic1 = df['Repo']=='ggplot2'
dftopic1 = df[topic1]
topic2 = df['Repo']=='ipython'
dftopic2 = df[topic2]
topic3 = df['Repo']=='keras'
dftopic3 = df[topic3]
topic4 = df['Repo']=='linux'
dftopic4 = df[topic4]
topic5 = df['Repo']=='node'
dftopic5 = df[topic5]
topic6 = df['Repo']=='pandas'
dftopic6 = df[topic6]
topic7 = df['Repo']=='scikit-learn'
dftopic7 = df[topic7]
topic8 = df['Repo']=='spark'
dftopic8 = df[topic8]
topic9 = df['Repo']=='tensorflow'
dftopic9 = df[topic9]
topic10 = df['Repo']=='tidyverse'
dftopic10 = df[topic10]



resize_dftopic0 = dftopic0.resample('d', on='Date').count()
resize_dftopic1 = dftopic1.resample('d', on='Date').count()
resize_dftopic2 = dftopic2.resample('d', on='Date').count()
resize_dftopic3 = dftopic3.resample('d', on='Date').count()
resize_dftopic4 = dftopic4.resample('d', on='Date').count()
resize_dftopic5 = dftopic5.resample('d', on='Date').count()
resize_dftopic6 = dftopic6.resample('d', on='Date').count()
resize_dftopic7 = dftopic7.resample('d', on='Date').count()
resize_dftopic8 = dftopic8.resample('d', on='Date').count()
resize_dftopic9 = dftopic9.resample('d', on='Date').count()
resize_dftopic10 = dftopic10.resample('d', on='Date').count()



ax = resize_dftopic0.plot()
ax.set_xlabel("Date Time")
ax.set_ylabel("Count")

az =resize_dftopic1.plot()
az.set_xlabel("Date Time")
az.set_ylabel("Count")

aw = resize_dftopic2.plot()
aw.set_xlabel("Date Time")
aw.set_ylabel("Count")

ay =resize_dftopic3.plot()
ay.set_xlabel("Date Time")
ay.set_ylabel("Count")

av =resize_dftopic4.plot()
av.set_xlabel("Date Time")
av.set_ylabel("Count")

ax = resize_dftopic5.plot()
ax.set_xlabel("Date Time")
ax.set_ylabel("Count")

az =resize_dftopic6.plot()
az.set_xlabel("Date Time")
az.set_ylabel("Count")

aw = resize_dftopic7.plot()
aw.set_xlabel("Date Time")
aw.set_ylabel("Count")

ay =resize_dftopic8.plot()
ay.set_xlabel("Date Time")
ay.set_ylabel("Count")

av =resize_dftopic9.plot()
av.set_xlabel("Date Time")
av.set_ylabel("Count")

av =resize_dftopic10.plot()
av.set_xlabel("Date Time")
av.set_ylabel("Count")

plt.show()
# %%
dftopic7
# %%
df['Message'] = df['Message'].replace(regex=['_'], value=' ')
df['Message'] = df['Message'].replace(regex=['-'], value=' ')
# %%
def preprocess(text):
    no_punct = "".join([c for c in text if c not in string.punctuation])
    return no_punct
# %%
df
# %%
df['Message'] = df['Message'].apply(lambda x: preprocess(x))
df['Message'].head()
# %%
tokenizer = RegexpTokenizer(r'\w+')
df['Message'] = df['Message'].apply(lambda x: tokenizer.tokenize(x.lower()))
df['Message'].head(20)
# %%
def remove_stopwords(text):
    words = [w for w in text if w not in stopwords.words('english')]
    return words
# %%
df['Message'] = df['Message'].apply(lambda x: remove_stopwords(x))
df['Message'].head(20)
# %%
lemmatizer = WordNetLemmatizer()

def word_lemmatizer(text):
#     lem_text = [lemmatizer.lemmatize(i) for i in text]
    lem_text = " ".join([lemmatizer.lemmatize(i) for i in text])
    return lem_text
# %%
# nltk.download('wordnet')

df['Message'].apply(lambda x: word_lemmatizer(x))
# %%
stemmer = PorterStemmer()

def word_stemmer(text):
    stem_text= [stemmer.stem(i) for i in text]
    return stem_text
# %%
df['Message'].apply(lambda x: word_stemmer(x))
# %%
df['Message'] = df['Message'].apply(lambda x: word_lemmatizer(x))
df['Message'].head(20)
# %%
# nltk.download('vader_lexicon')
sentAnalyser = SentimentIntensityAnalyzer()
sentiment = df['Message'].apply(lambda x: sentAnalyser.polarity_scores(x))
df = pd.concat([df,sentiment.apply(pd.Series)],1)
df
# %%
# resampling the datetime columns to hourly bins
sentiment_count = pd.DataFrame(columns=['datetime','sentiment'])
sentiment_count['datetime'] = df['Date']
sentiment_count['sentiment']= df['compound']
resize = sentiment_count.resample('H', on='datetime').mean()
newSeries = sentiment_count.resample('H', on='datetime').sum()

# Ploting the avg sentiment per hour
ax = resize.plot()
ax.set_xlabel("Date Time")
ax.set_ylabel("Sentiment Count")
ax.legend(["Avg Sentiment"])

# Ploting the total sentiment per hour
az =newSeries.plot()
az.set_xlabel("Date Time")
az.set_ylabel("Sentiment Count")
az.legend(["Tot Sentiment"])
plt.show()
# %%
# Printing out the top 50 words in a word cloud
all_words = ' '.join([text for text in df['Message Headline']])
wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(all_words)

plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()
# %%
# Printing out the top 50 words in a word cloud
all_words = ' '.join([text for text in df['Message']])
wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(all_words)

plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()
# %%
# LDA Topic Analysis
count_vect = CountVectorizer(max_df=0.8, min_df=2, stop_words='english')
doc_term_matrix = count_vect.fit_transform(df['Message'].values.astype('U'))

# Fitting the LDA Method with 5 topics
LDA = LatentDirichletAllocation(n_components=5, random_state=42)
LDA.fit(doc_term_matrix)

# NMF Topic Analysis
tfidf_vect = TfidfVectorizer(max_df=0.8, min_df=2, stop_words='english')
doc_term_matrix = tfidf_vect.fit_transform(df['Message'].values.astype('U'))

# Fitting the NMF Method with 5 topics
nmf = NMF(n_components=5, random_state=42)
nmf.fit(doc_term_matrix )
# %%
# Printing the LDA Key Words For Each Topic
for i,topic in enumerate(LDA.components_):
    print(f'Top 10 LDA words for topic {i}:')
    print([count_vect.get_feature_names()[i] for i in topic.argsort()[-10:]])
    print('\n')
# %%
# Printing the NMF Key Words For Each Topic
for i,topic in enumerate(nmf.components_):
    print(f'Top 10 words NMF for topic {i}:')
    print([tfidf_vect.get_feature_names()[i] for i in topic.argsort()[-10:]])
    print('\n')
# %%
df['Message'][0]
# %%

# %%
