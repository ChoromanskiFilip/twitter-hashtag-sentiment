import requests
from configparser import RawConfigParser
import json 

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
    # print(URL)
    r = requests.get(URL, headers={'Authorization': f'Bearer {TWITTER_BEARER_TOKEN}'})
    return r

# def fetch_historical_tweets(hashtag, lang='pl', result_type='recent', count=100):
#     URL = f"{TWITTER_SEARCH_RECENT_URL_V1}"
#     URL += f"?q=%23{hashtag}&lang={lang}&result_type={result_type}&count={count}"
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
#         r = requests.get(URL, headers={'Authorization': f'Bearer {TWITTER_BEARER_TOKEN}'})
#         if r.status_code == 200:
#             response_json = r.json()
#         else:
#             #something went wrong - idk how to handle
#             break
#         tweets.extend(response_json['statuses'])
#     return tweets

def fetch_tweets_v3(hashtag, since_id=None, lang='pl', result_type='recent', count=100):
    URL = f"{TWITTER_SEARCH_RECENT_URL_V1}"
    URL += f"?q=%23{hashtag}&lang={lang}&result_type={result_type}&count={count}"
    URL = URL if not since_id else URL + f"&since_id={since_id}"
    r = requests.get(URL, headers={'Authorization': f'Bearer {TWITTER_BEARER_TOKEN}'})
    if r.status_code == 200:
        response_json = r.json()
    else:
        raise Exception("Twitter API is responding with an error: " + json.dumps(r.json()))
    tweets = []
    tweets.extend(response_json['statuses'])
    iters = 100
    while len(response_json['statuses']) == count and iters > 0:
        iters -= 1
        URL = f"{TWITTER_SEARCH_RECENT_URL_V1}{response_json['search_metadata']['next_results']}"
        URL = URL if not since_id else URL + f"&since_id={since_id}"
        r = requests.get(URL, headers={'Authorization': f'Bearer {TWITTER_BEARER_TOKEN}'})
        if r.status_code == 200:
            response_json = r.json()
        else:
            break
        tweets.extend(response_json['statuses'])
    return tweets

def collect_tweets(hashtags):
    collected_tweets = []
    for hashtag in hashtags:
        fetched_response = fetch_tweets_v3(hashtag)
        collected_tweets.append({
            'hashtag': hashtag,
            'tweets': list(map(lambda tw: {
                'twitter_id': tw['id'],
                'text': tw['text'],
                'twitter_created_at': tw['created_at']
            }, fetched_response))
        })
    return collected_tweets
        


if __name__ == "__main__":
    # tweets = fetch_tweets('IgaŚwiątek', lang='pl', result_type='recent', count=10)
    # print(tweets)
    # print(tweets.json())
    # collected_tweets = collect_tweets(['IgaŚwiątek', 'AndrzejDuda'])

    with open('response_cout2_since-1348018862315466755.json', 'w', encoding='utf-8') as f:
        # resp = fetch_tweets_v2('IgaŚwiątek', count=100, result_type='recent').json()
        # json.dump(resp, f, ensure_ascii=False, indent=2)
        resp = fetch_tweets_v3('IgaŚwiątek', since_id=1348018862315466755 + 1, count=2)
        json.dump(resp, f, ensure_ascii=False, indent=2)
        

    # print(TWITTER_BEARER_TOKEN)
    # print(TWITTER_SEARCH_RECENT_URL)

