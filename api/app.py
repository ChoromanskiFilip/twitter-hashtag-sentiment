from flask import Flask, request, Response, jsonify
import models, json
from flask_sqlalchemy import SQLAlchemy
from configparser import ConfigParser
from sqlalchemy.sql import func, extract, asc, cast
from sqlalchemy import Date

config = ConfigParser()
config.read("config.ini")
server = config['Database']['server_url']
database = config['Database']['database_name']
username = config['Database']['username']
password = config['Database']['password']

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route("/tweets", methods=['GET'])
def get_tweets():
    limit = request.args.get('limit')
    hashtag = request.args.get('hashtag')
    return jsonify(get_tweets(limit, hashtag))


def get_tweets(limit, hashtag):
    tweets = None
    query = models.Tweet.query.join(models.Tweet.hashtag)
    if hashtag is not None:
        query = query.filter(models.Hashtag.hashtag.like(hashtag))
    if limit is not None:
        query = query.limit(int(limit))
    tweets = query.all()
    tweets = list(map(lambda x: models.tweetToDict(x), tweets))
    return tweets


@app.route("/hashtags", methods=['GET'])
def get_hashtags():
    hashtags = models.Hashtag.query.all()
    hashtags = list(map(lambda x: models.hashtagToDict(x), hashtags))
    return jsonify(hashtags)


@app.route("/daily_statistics", methods=['GET'])
def get_daily_statistics():
    hashtag = request.args.get('hashtag')
    return jsonify(get_daily_statistics(hashtag))


def get_daily_statistics(hashtag):
    daily_sentiment = []
    dates = db.session.query(cast(models.Tweet.twitter_created_at, Date)).distinct().all()
    for date in dates:
        tweets_from_date = models.Tweet.query \
            .join(models.Tweet.hashtag) \
            .filter(models.Hashtag.hashtag.like(hashtag)) \
            .filter(cast(models.Tweet.twitter_created_at, Date) == date[0]) \
            .all()
        positive_percent = None
        if len(tweets_from_date) is not 0:
            positive_percent = len(list(filter(lambda x: x.sentiment_result == 'positive', tweets_from_date))) / len(
                tweets_from_date)
        daily_sentiment.append({
            'date': date[0],
            'positive_percent': positive_percent,
            'tweets': len(tweets_from_date)
        })
    return daily_sentiment


@app.route("/overall_statistics", methods=['GET'])
def get_overall_statistics():
    hashtag = request.args.get('hashtag')
    return jsonify(get_overall_statistics(hashtag))


def get_overall_statistics(hashtag):
    tweets_positive = len(models.Tweet.query
                          .join(models.Tweet.hashtag)
                          .filter(models.Hashtag.hashtag.like(hashtag))
                          .filter(models.Tweet.sentiment_result.like('positive'))
                          .all())
    tweets_neutral = len(models.Tweet.query
                         .join(models.Tweet.hashtag)
                         .filter(models.Hashtag.hashtag.like(hashtag))
                         .filter(models.Tweet.sentiment_result.like('neutral'))
                         .all())
    tweets_negative = len(models.Tweet.query
                          .join(models.Tweet.hashtag)
                          .filter(models.Hashtag.hashtag.like(hashtag))
                          .filter(models.Tweet.sentiment_result.like('negative'))
                          .all())
    all = tweets_positive + tweets_neutral + tweets_negative
    return {
        'tweets_positive': tweets_positive,
        'tweets_positive_percent': tweets_positive / all,
        'tweets_neutral': tweets_neutral,
        'tweets_neutral_percent': tweets_neutral / all,
        'tweets_negative': tweets_negative,
        'tweets_negative_percent': tweets_negative / all,
    }

@app.route("/hashtag_summary", methods=['GET'])
def get_hashtag_summary():
    hashtag = request.args.get('hashtag')
    return jsonify({
        'hashtag': hashtag,
        'daily_statistics': get_daily_statistics(hashtag),
        'overall_statistics': get_overall_statistics(hashtag),
        'sample_tweets': get_tweets(5, hashtag)
    })



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
