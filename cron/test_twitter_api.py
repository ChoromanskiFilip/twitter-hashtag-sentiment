from configparser import RawConfigParser
import tweepy

config = RawConfigParser()
config.read("config.ini")

TWITTER_CONSUMER_KEY = config['TwitterAPI']['consumer_key']
TWITTER_CONSUMER_SECRET_KEY = config['TwitterAPI']['consumer_secret_key']
TWITTER_ACCESS_TOKEN = config['TwitterAPI']['access_token']
TWITTER_ACCESS_TOKEN_SECRET = config['TwitterAPI']['access_token_secret']
TWITTER_SEARCH_RECENT_URL_V1 = config['TwitterAPI']['serach_url_v1']
TWITTER_SEARCH_RECENT_URL_V2 = config['TwitterAPI']['serach_url_v2']
TWITTER_BEARER_TOKEN = config['TwitterAPI']['bearer_token']

auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET_KEY)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# def fetch_tweets_v3(hashtag, since_id=None, lang='pl', result_type='recent', count=100):
#     URL = f"{TWITTER_SEARCH_RECENT_URL_V1}"
#     URL += f"?q=%23{hashtag}&lang={lang}&result_type={result_type}&count={count}"
#     URL = URL if not since_id else URL + f"&since_id={since_id}"
#     r = requests.get(URL, headers={'Authorization': f'Bearer {TWITTER_BEARER_TOKEN}'})
#     if r.status_code == 200:
#         response_json = r.json()
#     else:
#         raise Exception("Twitter API is responding with an error: " + json.dumps(r.json()))
#     tweets = []
#     tweets.extend(response_json['statuses'])
#     iters = 100
#     while len(response_json['statuses']) == count and iters > 0:
#         iters -= 1
#         URL = f"{TWITTER_SEARCH_RECENT_URL_V1}{response_json['search_metadata']['next_results']}"
#         URL = URL if not since_id else URL + f"&since_id={since_id}"
#         r = requests.get(URL, headers={'Authorization': f'Bearer {TWITTER_BEARER_TOKEN}'})
#         if r.status_code == 200:
#             response_json = r.json()
#         else:
#             break
#         tweets.extend(response_json['statuses'])
#     return tweets

def collect_tweets(hashtags):
    collected_tweets = []
    for hashtag in hashtags:
        fetched_response = api.search(q=hashtag + " -filter:retweets", lang="pl", rpp=100, tweet_mode='extended')
        collected_tweets.append({
            'hashtag': hashtag,
            'tweets': list(map(lambda tw: {
                'twitter_id': tw.id,
                'text': tw.full_text,
                'twitter_created_at': tw.created_at
            }, fetched_response))
        })
    return collected_tweets

