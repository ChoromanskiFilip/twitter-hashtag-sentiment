from flask import Flask, request, Response, jsonify
import models, json
from flask_sqlalchemy import SQLAlchemy
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")
server = config['Database']['server_url']
database = config['Database']['database_name']
username = config['Database']['username']
password = config['Database']['password']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route("/tweets", methods=['GET'])
def get_tweets():
    limit = request.args.get('limit')
    hashtag = request.args.get('hashtag')
    tweets = None
    query = models.Tweet.query.join(models.Tweet.hashtag)
    if hashtag is not None:
        query = query.filter(models.Hashtag.hashtag.like(hashtag))
    if limit is not None:
        query = query.limit(int(limit))
    tweets = query.all()
    tweets = list(map(lambda x: models.tweetToDict(x), tweets))
    return jsonify(tweets)

@app.route("/hashtags", methods=['GET'])
def get_hashtags():
    tweets = models.Tweet.query.all()
    tweets = list(map(lambda x: models.tweetToDict(x), tweets))
    return jsonify(tweets)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
