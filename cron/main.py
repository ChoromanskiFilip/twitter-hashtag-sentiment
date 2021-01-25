import sys
import os
import logging
import logging.config

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
logging.basicConfig(level=logging.INFO)

from database_api import extract_unprocessed_tweets
from database_api import save_tweets_with_sentiment
from database_api import get_active_hashtags
from test_twitter_api import collect_tweets
from text_analytics import process



def main():
    logging.info('Fetching active hashtags...')
    active_hashtags = get_active_hashtags()
    logging.info(f'Collecting tweets for hashtags: {active_hashtags}')
    collected_tweets_from_API = collect_tweets(active_hashtags)
    unprocessed_tweets = extract_unprocessed_tweets(collected_tweets_from_API)
    analysed_tweets = []
    logging.info(f'Unprocessed tweets: {unprocessed_tweets}')
    for tweets_for_hashtag in unprocessed_tweets:
        hashtag = tweets_for_hashtag['hashtag']
        analysed_tweets_for_hashtag = []
        for tweet in tweets_for_hashtag['tweets']:
            try:
                logging.info(f'Computing sentiment of tweet: {tweet}')
                sentiment = process(tweet['text'], hashtag)
                analysed_tweets_for_hashtag.append({
                    'text': tweet['text'],
                    'twitter_id': tweet['twitter_id'],
                    'twitter_created_at': tweet['twitter_created_at'],
                    'sentiment_result': sentiment['sentiment_result'],
                    'positive_value': sentiment['positive_value'],
                    'negative_value': sentiment['negative_value']
                })
            except Exception as ex:
                logging.warning(f'Exception {ex} during processing tweet: {tweet}')
        analysed_tweets.append({
            'hashtag': hashtag,
            'tweets': analysed_tweets_for_hashtag
        })
    logging.info(f'Saving tweets with computed sentiment to the database')
    save_tweets_with_sentiment(analysed_tweets)

main()
