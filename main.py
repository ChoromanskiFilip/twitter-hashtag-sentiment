import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database_api import extract_unprocessed_tweets
from database_api import save_tweets_with_sentiment
from text_analytics import process


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
