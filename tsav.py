import tweepy
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import string
from deep_translator import GoogleTranslator

auth = tweepy.OAuthHandler("your data", "your data")
auth.set_access_token("your data", "your data")
api = tweepy.API(auth)

msgs = []
cleanmsgs = []

searched_tweets = tweepy.Cursor(api.search_tweets, q='Spaten', lang='pt', tweet_mode="extended").items(1000)
for tweet in searched_tweets:
    msgs.append(tweet.full_text.lower())

for text in msgs:
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
    text = re.sub(r'\@\w+|\#', '', text)
    for letter in text:
        if letter in string.punctuation:
            text = text.replace(letter, " ")

    tweet = " ".join(text.split())
    if(tweet[0]=='r' and tweet[1]=='t'):
        continue
    cleanmsgs.append(tweet)

bom = 0
ruim = 0

tam = len(cleanmsgs)

vader = SentimentIntensityAnalyzer()

for text in cleanmsgs:
    trad = GoogleTranslator(source="portuguese", target="english").translate(text)
    res = vader.polarity_scores(trad)
    if(res['compound']<=-0.05):
        ruim+=1
    else:
        bom+=1

print("Porcetagem de tweets positivos e neutros:")
print(int((bom/tam)*100), "%")
print("Porcetagem de tweets negativos:")
print(int((ruim/tam)*100), "%")
