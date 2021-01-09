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
