import pandas as pd
import numpy as np
import tweepy # to use Twitter’s API
from textblob import TextBlob # for doing sentimental analysis
import re # regex for cleaning the tweets
import string
import matplotlib.pylab as plt
consumer_key ="Enter your key"
consumer_secret = "Enter your key"
access_token = "Enter your key"
access_token_secret = "Enter your key"

def twitter():
    # Creating the authentication object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # Setting your access token and secret
    token = auth.set_access_token(access_token, access_token_secret)
    # Creating the API object while passing in auth information
    api = tweepy.API(auth, wait_on_rate_limit = True)
    return api

# Creating tw object
tw = twitter()
# Extracting Ellen DeGeneres tweets
#search = tw.user_timeline(screen_name="TheEllenShow", count = 200, lang ="en")
search=tw.search(q="Coronavirus",count=100,lang="en")
#  Printing last 10 tweets
print("10 recent tweets:\n")
for tweets in search[:10]:
    print(tweets.text + '\n')

# Converting into dataframe (Column name Tweets)
df = pd.DataFrame([tweets.text for tweets in search], columns=['Tweets'])

# Cleaning the tweets
# Creating a function called clean. removing hyperlink, #, RT, @mentions
def clean(x):
 x = re.sub('^RT[\s]+', '', x)
 x = re.sub('https?:\/\/.*[\r\n]*', '', x)
 x = re.sub('#', '', x)
 x = re.sub('@[A-Za-z0–9]+', '', x)
 x="".join([ch for ch in x if ch not in string.punctuation])
 return x

df['Tweets'] = df['Tweets'].apply(clean)
polarity = lambda x: TextBlob(x).sentiment.polarity
subjectivity = lambda x: TextBlob(x).sentiment.subjectivity
df['polarity'] = df['Tweets'].apply(polarity)
df['subjectivity'] = df['Tweets'].apply(subjectivity)
df.to_csv("twitter.csv")
print(df)
labels=["nutral","positive","negative"]
positive=df[df.polarity>0]
negative=df[df.polarity<0]
neutral=df[df.polarity==0]
labels=["Negative","Neutral","Positive"]
colors = ['red', 'yellow', 'green']
values=[len(negative.polarity), len(neutral.polarity), len(positive.polarity)]
plt.pie(values, colors=colors,autopct='%1.2f%%')
plt.title("Sentimental Analysis of Tweets about Coronavirus")
plt.legend(["Negative","Neutral","Positive"])
plt.show()
