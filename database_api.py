import pyodbc
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")
server = 'tcp:' + config['Database']['server_url']
database = config['Database']['database_name']
username = config['Database']['username']
password = config['Database']['password']
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)


def extract_unprocessed_tweets(all_tweets):
    twitter_ids = []
    for tweets_for_hashtag in all_tweets:
        for tweet in tweets_for_hashtag['tweets']:
            twitter_ids.append(tweet['twitter_id'])
    twitter_ids = list(map(str, twitter_ids))
    twitter_ids = "(" + ", ".join(twitter_ids) + ")"
    cursor = conn.cursor()
    cursor.execute(f'SELECT * from Tweets t where t.twitter_id in {twitter_ids}')
    for row in cursor:
        twitter_id = row[6]
        for tweets_for_hashtag in all_tweets:
            for tweet in tweets_for_hashtag['tweets']:
                if tweet['twitter_id'] == twitter_id:
                    tweets_for_hashtag['tweets'].remove(tweet)
    return all_tweets


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


def save_tweets_with_sentiment(all_tweets):
    for tweets_for_hashtag in all_tweets:
        hashtag = tweets_for_hashtag['hashtag']
        for tweet in tweets_for_hashtag['tweets']:
            hashtag_id = find_hashtag_id(hashtag)
            if hashtag_id == None:
                save_hashtag(hashtag)
                hashtag_id = find_hashtag_id(hashtag)
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO Tweets(hashtag_id, tweet, sentiment_result, positive_value, negative_value,
                              twitter_id, twitter_created_at) 
                            VALUES (?, ?, ?, ?, ?, ?, ?)""",
                           hashtag_id, tweet['text'], tweet['sentiment_result'], tweet['positive_value'],
                           tweet['negative_value'], tweet['twitter_id'], tweet['twitter_created_at'])
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


# print(get_active_hashtags())
# print(extract_unprocessed_tweets(['asd', 'Słabo #AndrzejDuda']))
# print(get_tweets_with_sentiment('#AndrzejDuda'))
# print(find_hashtag_id('#AndrzejDuda'))
# save_hashtag('new', True)
# save_tweets_with_sentiment('#AndrzejDuda', [
#     {
#         'tweet': 'New tweet about #AndrzejDuda',
#         'sentiment_result': 'positive',
#         'positive_value': 0.7,
#         'negative_value': 0.3
#     }
# ])
# save_tweets_with_sentiment('#NewHashTag', [
#     {
#         'tweet': 'New tweet about #NewHashTag',
#         'sentiment_result': 'positive',
#         'positive_value': 0.6,
#         'negative_value': 0.4
#     }
# ])
