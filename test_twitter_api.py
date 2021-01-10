import requests
from configparser import RawConfigParser

config = RawConfigParser()
config.read("config.ini")

TWITTER_SEARCH_RECENT_URL_V1 = config['TwitterAPI']['serach_url_v1']
TWITTER_SEARCH_RECENT_URL_V2 = config['TwitterAPI']['serach_url_v2']
TWITTER_BEARER_TOKEN = config['TwitterAPI']['bearer_token']

def fetch_tweets(query, version='1', **kwargs):
    # Endpoint docs: https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent
    if version == '1':
        URL = f"{TWITTER_SEARCH_RECENT_URL_V1}?q={query}"
    elif version == '2':
        URL = f"{TWITTER_SEARCH_RECENT_URL_V2}?query={query}"
    else:
        raise Exception("Only version '1' and '2' are allowed.")
    URL = URL if not kwargs else URL + '&' + '&'.join([f'{k}={v}' for k, v in kwargs.items()])
    print(URL)
    r = requests.get(URL, headers={'Authorization': f'Bearer {TWITTER_BEARER_TOKEN}'})
    return r

def fetch_tweets_v2(hashtag, lang='pl', **kwargs):
    URL = f"{TWITTER_SEARCH_RECENT_URL_V1}?q=%23{hashtag}&lang={lang}"
    URL = URL if not kwargs else URL + '&' + '&'.join([f'{k}={v}' for k, v in kwargs.items()])
    print(URL)
    r = requests.get(URL, headers={'Authorization': f'Bearer {TWITTER_BEARER_TOKEN}'})
    return r
    

if __name__ == "__main__":
    # tweets = fetch_tweets('IgaŚwiątek', lang='pl', result_type='recent', count=10)
    # print(tweets)
    # print(tweets.json())

    
    print(fetch_tweets_v2('IgaŚwiątek').json())

    # print(TWITTER_BEARER_TOKEN)
    # print(TWITTER_SEARCH_RECENT_URL)

