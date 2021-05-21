import tweepy
from textblob import TextBlob
import pandas as pd
import re
from wordcloud import WordCloud
#regex for string data
import matplotlib.pyplot as plt


plt.style.use('fivethirtyeight')
#for gird form
#for live tweeter data
#twitter api credential
apikey ="RQebZmzAPBg9o8WAMdGqKASza"
apiSecreat ="HvGeDFzqmqNPWQPz5U3a7W6QUGThtKfXnJavXmHTANxlMq0hBE"
accessToken ="1391626744440885250-AheGZ4iqp5JUWmIkq2QmzopbrwmoKG"
accessTokenSecreat ="j23jwXbSevqPv2lAnDn5YzGki0KAwixabBNqcB7sLLRZS"

#create the authenticate object
aunthenticate =tweepy.OAuthHandler(apikey,apiSecreat)
aunthenticate.set_access_token(accessToken,accessTokenSecreat)
api=tweepy.API(aunthenticate)

posts=api.user_timeline(screen_name='trump',count=100,lang="en",tweet_mode='extended')
i=1
#To print the tweets we get
for tweet in posts[:10]:
    print(str(i)+')' + tweet.full_text + '\n')
    i=i+1


#create data frame with a column called tweets
df=pd.DataFrame([tweet.full_text for tweet in posts],columns=['Tweets'])


# make a function to clean tweets
def cleanTxt(text):
    text= re.sub('@[A-Za-z0-9]+','',text ) #removing mentions
    text= re.sub("#",'',text) #removing #
    text= re.sub('RT[\s]+','',text) # removing Retweets
    text= re.sub('https?:\/\/\S+','',text) #removing links
    return text
df['Tweets']= df['Tweets'].apply(cleanTxt)
print(df)


#to find sentiments
#textblob

#0.0<p  positive
#if p<0.0 its negative
#subjectivity -more the value more the opion
#0.75 public opinion

#create fun to get tje subjectivety of the tweets
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity
def getpolarity(text):
    return TextBlob(text).sentiment.polarity

#create two column subjectivity and polarity
df['Subjectivity']=df['Tweets'].apply(getSubjectivity)
df['Polarity']=df['Tweets'].apply(getpolarity)
print(df)

#word cloud visualization
allword=''.join([i for i in df['Tweets']])
cloud=WordCloud(width=500,height=300,random_state=0,max_font_size=50).generate(allword)
plt.imshow(cloud)
plt.show()


# create another data frame another column as anaysis
def getAnalysis(score):
    if score<0:
        return 'negative'
    elif score==0:
        return 'Neutral'
    else:
        return 'Positive'

df['Analysis']=df['Polarity'].apply(getAnalysis)
print(df)
print(df['Analysis'].value_counts())

#plotting scatter plot
plt.figure(figsize=(8,6))
for i in range(0,df.shape[0]):
    plt.scatter(df['Polarity'][i],df['Subjectivity'][i],color='Green')
plt.title("Sentiment Analysis")
plt.xlim(-1,1)
plt.xlabel('Polarity')
plt.ylabel('Subjectivity')
plt.show()

#getting bar graph
df['Analysis'].value_counts().plot(kind='bar')
plt.title('Sentiment Analysis')
plt.xlabel('Polarity')
plt.ylabel('Count')
plt.show()





