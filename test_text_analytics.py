from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import requests
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")
print(config['TextAnalyticsAPI']['endpoint'] + config['TextAnalyticsAPI']['sentiment_url'])
print(config)

# key = config['TextAnalyticsAPI']['key']
# endpoint = config['TextAnalyticsAPI']['endpoint']

subscription_key = config['TextAnalyticsAPI']['key']
sentiment_url = config['TextAnalyticsAPI']['endpoint'] + config['TextAnalyticsAPI']['sentiment_url']
print(subscription_key)
print(sentiment_url)

def analyze_sentiment_myimplement(text):
    documents = {"documents": [
        {"id": "1", "language": "pl", "text": text}
    ]}
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    response = requests.post(sentiment_url, headers=headers, json=documents)
    sentiments = response.json()
    print(sentiments)

print("Sentyment pozytywny:\n")
analyze_sentiment_myimplement("#IgaŚwiątek świetna gra. Gratuluje wygranej!")
print("\nSentyment negatywny:\n")
analyze_sentiment_myimplement("Słaby występ #IgaŚwiątek")

# def authenticate_client():
#     ta_credential = AzureKeyCredential(key)
#     text_analytics_client = TextAnalyticsClient(
#             endpoint=endpoint, 
#             credential=ta_credential)
#     return text_analytics_client

# textanalytics_client = authenticate_client()

# def sentiment_analysis(text):
#     response = textanalytics_client.analyze_sentiment(documents=[text], language='pl')
#     # print(response)
#     return response
#     # sentiment = response.sentiment

# for result in sentiment_analysis("#IgaŚwiątek świetna gra. Gratuluje wygranej!"):
#     print(result)