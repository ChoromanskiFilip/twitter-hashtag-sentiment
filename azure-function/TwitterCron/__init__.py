import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import datetime
import logging
import azure.functions as func
import requests
from configparser import RawConfigParser
import aspect_based_sentiment_analysis as absa
import pyodbc

config = RawConfigParser()
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
logging.info(f"Config file path: {config_path}")
config.read(config_path)

logging.info(f"Config file content: {config.get('Database', 'server_url', fallback='No such things as config[Database][server_url]')}")
server = 'tcp:' + config['Database']['server_url']
database = config['Database']['database_name']
username = config['Database']['username']
password = config['Database']['password']
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
nlp = absa.load()

def main(mytimer: func.TimerRequest) -> None:
    logging.info(f"Function triggered...")
    logging.info(f"Config file path: {config_path}")
    logging.info(f"Config file content: {config.get('Database', 'server_url', fallback='No such things as config[Database][server_url]')}")
    
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    
    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    active_hashtags = get_active_hashtags()
    collected_tweets_from_API = {
        'hashtag': '#AndrzejDuda',
        'tweets': ['Nowy tweet o #AndrzejDuda', 'Jeszcze nowszy tweet o #AndrzejDuda']
    }
    hashtag = collected_tweets_from_API['hashtag']
    unprocessed_tweets = extract_unprocessed_tweets(collected_tweets_from_API['tweets'])
    analysed_tweets = []
    for tweet in unprocessed_tweets:
        sentiment = process(tweet, hashtag)
        analysed_tweets.append({
            'tweet': tweet,
            'sentiment_result': sentiment['sentiment_result'],
            'positive_value': sentiment['positive_value'],
            'negative_value': sentiment['negative_value']
        })
    save_tweets_with_sentiment(hashtag, analysed_tweets)


def extract_unprocessed_tweets(tweets):
    cursor = conn.cursor()
    aggregated_tweets = list(map(lambda x: "'" + x + "'", tweets))
    aggregated_tweets = '(' + ', '.join(aggregated_tweets) + ')'
    cursor.execute(f'SELECT * from Tweets t where t.tweet in {aggregated_tweets}')
    for row in cursor:
        tweet = row[2]
        tweets.remove(tweet)
    return tweets


def get_tweets_with_sentiment(hashtag):
    cursor = conn.cursor()
    cursor.execute('SELECT * from Tweets t ' +
                   'join Hashtags AS h ON (t.hashtag_id = h.id)' +
                   f"where h.hashtag = '{hashtag}'")
    results = []
    for row in cursor:
        tweet = row[2]
        sentiment_result = row[3]
        positive_value = row[4]
        negative_value = row[5]
        results.append({
            'tweet': tweet,
            'sentiment_result': sentiment_result,
            'positive_value': positive_value,
            'negative_value': negative_value
        })
    return results


def save_tweets_with_sentiment(hashtag, tweets):
    hashtag_id = find_hashtag_id(hashtag)
    if hashtag_id == None:
        save_hashtag(hashtag)
        hashtag_id = find_hashtag_id(hashtag)
    for entry in tweets:
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO Tweets(hashtag_id, tweet, sentiment_result, positive_value, negative_value) 
                        VALUES (?, ?, ?, ?, ?)""",
                       hashtag_id, entry['tweet'], entry['sentiment_result'], entry['positive_value'],
                       entry['negative_value'])
        conn.commit()


def find_hashtag_id(hashtag):
    cursor = conn.cursor()
    cursor.execute(f"SELECT h.id FROM Hashtags AS h WHERE h.hashtag = '{hashtag}'")
    row = cursor.fetchone()
    if row is not None:
        return row.id
    else:
        return None


def save_hashtag(hashtag, active=True):
    if active:
        active = 1
    else:
        active = 0
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO Hashtags(hashtag, active) VALUES (?, ?)""", hashtag, active)
    conn.commit()


def get_active_hashtags():
    cursor = conn.cursor()
    cursor.execute("SELECT h.hashtag FROM Hashtags AS h")
    rows = cursor.fetchall()
    return list(map(lambda x: x.hashtag, rows))

def process(polish_tweet, aspect):
    english_tweet = translate_to_english(polish_tweet)
    return analyze_sentiment(english_tweet, aspect)


def analyze_sentiment(text, aspect):
    sentiment_azure = analyze_sentiment_azure(text, aspect)
    if sentiment_azure is None:
        return analyze_sentiment_absa(text, aspect)
    else:
        return sentiment_azure


def analyze_sentiment_absa(text, aspect):
    aspect_sentiment = nlp(text, aspects=[aspect])
    return {
        'sentiment_result': aspect_sentiment.subtasks[aspect].sentiment.name,
        'positive_value': aspect_sentiment.subtasks[aspect].scores[2].item(),
        'negative_value': aspect_sentiment.subtasks[aspect].scores[1].item()
    }


def analyze_sentiment_azure(text, aspect):
    subscription_key = config['TextAnalyticsAPI']['key']
    sentiment_url = config['TextAnalyticsAPI']['endpoint'] + config['TextAnalyticsAPI']['sentiment_url']
    body = {"documents": [
        {"id": "1", "language": "en", "text": text}
    ]}
    location = config['TextAnalyticsAPI']['location']
    response = make_request(sentiment_url, body, subscription_key, location)
    # print(f'Text analytics respone: {response}')

    for sentence in response['documents'][0]['sentences']:
        for found_aspect in sentence['aspects']:
            if found_aspect['text'] == aspect:
                return {
                    'result': found_aspect['sentiment'],
                    'positive': found_aspect['confidenceScores']['positive'],
                    'negative': found_aspect['confidenceScores']['negative']
                }
    return None


def translate_to_english(text):
    translator_key = config['Translator']['key']
    translate_url = config['Translator']['endpoint'] + config['Translator']['translate_url']
    location = config['Translator']['location']
    body = [{'Text': text}]
    response = make_request(translate_url, body, translator_key, location)
    #print(f'Translator respone: {response}')
    return response[0]['translations'][0]['text']


def make_request(url, body, key, location):
    headers = {"Ocp-Apim-Subscription-Key": key,
               "Ocp-Apim-Subscription-Region": location,
               "Content-Type": "application/json"}
    return requests.post(url, headers=headers, json=body).json()


def fetch_tweets(hashtag, since_id=None, lang='pl', result_type='recent', count=100):
    """
    hashtag : string
    since_id : int  - by default None - fetch all tweets that are available,
                        should be used for historical tweet aggregation
                    - if not None - fetch tweets that have id older than provided 
                        should be used for periodic tweet aggregation - eg. daily
    """
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
            #something went wrong - idk how to handle
            break
        tweets.extend(response_json['statuses'])
    return tweets

def map_tweets(tweets):
    mapped_tweets = []
    for tweet in tweets:
        if tweet['truncated']: # skip truncated tweets - idk if this is sufficiant
            continue
        if tweet.get('retweeted_status'): # skip retweets
            continue
        mapped_tweets.append({
            "text": tweet['text'],
            "created_at": datetime.datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S %z %Y"),
            "id": tweet['id']
        })
    
    return mapped_tweets