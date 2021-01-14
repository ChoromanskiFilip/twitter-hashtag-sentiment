from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import db

class Hashtag(db.Model):
    __tablename__ = 'hashtags'
    id = db.Column(db.BigInteger, primary_key=True)
    hashtag = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, nullable=False)


class Tweet(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.BigInteger, primary_key=True)
    hashtag_id = db.Column(db.BigInteger, ForeignKey('hashtags.id'), nullable=False)
    tweet = db.Column(db.String(1000), nullable=False)
    sentiment_result = db.Column(db.String(50), nullable=False)
    positive_value = db.Column(db.Float, nullable=False)
    negative_value = db.Column(db.Float, nullable=False)
    twitter_id = db.Column(db.BigInteger)
    twitter_created_at = db.Column(db.DateTime)
    hashtag = relationship("Hashtag")



def tweetToDict(tweet):
    return {
        'id': tweet.id,
        'hashtag':tweet.hashtag.hashtag,
        'tweet':tweet.tweet,
        'sentiment_result':tweet.sentiment_result,
        'positive_value':tweet.positive_value,
        'negative_value':tweet.negative_value,
        'twitter_id':tweet.twitter_id,
        'twitter_created_at': tweet.twitter_created_at
    }