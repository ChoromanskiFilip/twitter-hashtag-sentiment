# twitter-hashtag-sentiment

1. [Description](#Description)
1. [Contributors](#Contributors)
    1. [Filip Choromański](#Filip-Choromański)
    1. [Bartłomiej Królak](#Bartłomiej-Królak)
1. [Features](#Features)
1. [Solution](#Solution)
    1. [Architecture](#Architecture)
    1. [Tech Stack](#Tech-Stack)
1. [TODO](#TODO)


## Description
Aspect based sentiment analysis of hashtags used in twitter posts using Azure services.

## Contributors

### Filip Choromański
I am student of Computer science with Data Engineering speciality on Warsaw University of Technology on facoulty of Electrical Engineering. I work as ServiceNow Developer. In the free time I like to watch Premier League and select my Fantasy Premier League squad.

***GitHub*** - https://github.com/ChoromanskiFilip

### Bartłomiej Królak

***GitHub*** - 

## Features
**Minimum viable product (MVP):**
- Showing sentiment indicator for given hashtag
- Showing example tweets with given hashtag
- Showing popularity over time for given hashtag
- Everything available from hosted web page

Additional features:
- Showing sentiment over time

## Solution
As a welcome screen user will see input field where he/she should provide hashtag for which sentiment will be determined. After user submits the hashtag, request to web API will be send. API will count sentiment using Text Analytics API service available in Azure.  Then it will respond with a JSON object containing sentiment score, and few example tweets for given input. Additionally user can request more detailed information for the hashtag e.g. popularity and sentiment over time.

### Architecture


### Tech Stack

Web API:
- Deployed to Azure Function
- Python
- Text Analytics API

Web Page:
- Deployed to Azure App Service (Web App)
- React

## TODO
- [ ] Prepare Python Azure Function boilerplate
- [ ] Prepare React boilerplate
- [ ] Connect to Twitter API
- [ ] Connect to Text Analytics API
- [ ] Prepare welcome page with input field for web app
- [ ] Deploy React app ([Deploy from VS Code](https://azure.microsoft.com/pl-pl/resources/videos/build-and-deply-nodejs-and-react-apps-with-vscode-appservice-and-cosmosdb/))
- [ ] Count sentiment for given hashtag
- [ ] Prepare react component showing sentiment score
- [ ] Prepare endpoint returning sentiment and example tweets for given hashtag