import streamlit as st
import tweepy
import csv
import re
import emoji_data_python

default_accounts = ['RubinReport', 
  'DouglasKMurray', 
  'StefanMolyneux', 
  'BasedPoland', 
  'V_of_Europe', 
  'libertytarian', 
  'MrAndyNgo', 
  'RealDonaldTrump',
  'AnnCoulter',
  'MarkSteynOnline',
  'ezralevant',
  'nntaleb',
  'Lauren_Southern',
  'RealJamesWoods',
  'RandPaul',
  'tedcruz',
  'IngrahamAngle',
  'benshapiro',
  'charliekirk11',
  'PressSec',
  'jihadwatchRS',
  'scrowder',
  'Nigel_Farage',
  'michellemalkin',
  'PrisonPlanet',
  'ScottAdamsSays',
  'andrewklavan',
  'TuckerCarlson',
  'SheriffClarke',
  'mitchellvii',
  'newtgingrich',
  'DineshDSouza',
  'JamesOKeefeIII',
  'DanaPerino',
  'DLoesch',
  'BuckSexton',
  'KatiePavlich',
  'marklevinshow',
  'guypbenson',
  'dbongino',
  'AllenWest',
  'greggutfeld',
  'JimDeMint',
  'jasoninthehouse',
  'BrentBozell',
  'KarlRove',
  'larryelder',
  'BillOReilly',
  'nickgillespie',
  'CaidenCowger',
  'SPMorrison_']
accounts = default_accounts + ['']


@st.cache
def get_tweets(account):
    return api.user_timeline(screen_name=account, count=200, tweet_mode='extended')


st.title('Get Tweets')
st.markdown('A [simple demonstration](https://github.com/CaliberAI/streamlit-get-tweets) of using [Streamlit](https://streamlit.io/) with [Tweepy](https://www.tweepy.org/) to get Tweets from Twitter Accounts.')
api_key = st.text_input('Twitter API Key', '')
api_secret_key = st.text_input('Twitter API Secret Key', '')
access_token = st.text_input('Twitter Access Token', '')
access_token_secret = st.text_input('Twitter Access Token Secret', '')
included_accounts = st.multiselect('Accounts', accounts, default_accounts)
go = st.button('Get Tweets')

if go:
    try:
        auth = tweepy.OAuthHandler(api_key, api_secret_key)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        tweets = []
        for account in included_accounts:
            st.write(account)
            api_response = get_tweets(account)
            for tweet in api_response:
                if tweet.retweeted:
                    text = tweet.retweeted_status.full_text
                else:
                    text = tweet.full_text
                if tweet.lang == 'en':
                    text = re.sub('http://\S+|https://\S+', ' ', text)
                    text = re.sub(emoji_data_python.get_emoji_regex(), ' ', text)
                    text = re.sub('\n', ' ', text)
                    text = re.sub('&amp;', '&', text)
                    text = re.sub('@', '', text)
                    text = re.sub('  ', ' ', text)
                
                    tweets += [[tweet.user.screen_name, text, tweet.id_str]]
        st.subheader('Tweets')
        st.dataframe(tweets)
        with open('tweets.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerows(tweets)
    except ApiException as e:
        st.exception("Exception: %s\n" % e)

st.markdown('___')
st.markdown('by [CaliberAI](https://github.com/CaliberAI/)')
