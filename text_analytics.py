import requests
from configparser import ConfigParser
import aspect_based_sentiment_analysis as absa

config = ConfigParser()
config.read("config.ini")
nlp = absa.load()


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


polish_tweet = 'Niestety, bardzo słaby występ #IgaSwiatek, ale trzeba przyznać, że organizacja zawodów była idealna.'
aspect = '#IgaSwiatek'
print(process(polish_tweet, aspect))
