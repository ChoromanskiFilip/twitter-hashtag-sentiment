# twitter-hashtag-sentiment

- [twitter-hashtag-sentiment](#twitter-hashtag-sentiment)
  - [Description](#description)
  - [Contributors](#contributors)
    - [Filip Choromański](#filip-choromański)
    - [Bartłomiej Królak](#bartłomiej-królak)
  - [Features](#features)
  - [Solution](#solution)
    - [Architecture](#architecture)
    - [Tech Stack](#tech-stack)
  - [TODO](#todo)


## Description
Aspect based sentiment analysis of hashtags used in twitter posts using Azure services.

## Contributors

### Filip Choromański
I am student of Computer science with Data Engineering speciality on Warsaw University of Technology on faculty of Electrical Engineering. I work as ServiceNow Developer. In the free time I like to watch Premier League and select my Fantasy Premier League squad.

***GitHub*** - https://github.com/ChoromanskiFilip

### Bartłomiej Królak
Same as my friend I study computer science on Warsaw University of Technology. At the same time I work part-time as Java Deloper.

***GitHub*** - https://github.com/btqr

## Features
**Minimum viable product (MVP):**
- Showing sentiment indicator for given hashtag
- Showing example tweets with given hashtag
- Showing sentiment over time for given hashtag
- Everything is available at hosted web page

## Solution
On the welcome "Analysis screen" of web application user will see dropdown menu where she/he can choose hashtag in order to see sentiment results over last few days. On the other "Manage hashtags screen " user can turn on/off collecting data for any existing hashtag or provide new hashtags for which sentiment is going to be determined. After user submits the hashtag, request to our backend microservice will be sent. Then we will add entry with new hashtag to our database and inform user that we have no data yet for this specific hashtag, but it will be gathered soon. Cron service in the background will repeatedly fetch tweets for hashtags that are in our database using twitter API https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets and compute their sentiment using aspect-based-sentiment-analysis library https://pypi.org/project/aspect-based-sentiment-analysis/ or Text Analytics API service available in Azure. These results will be continously saved to relational database that is also deployed to Azure as Azure SQL Server.
### Architecture
![Application Archtecture Diagram](pics/architecture-twitter-hashtag-sentiment.png)


### Tech Stack

Serivces:
- Cron service - used to fetch tweets and compute their sentiment (Python + Flask + Sqlalchemy)
- Sentiment API service - used to provide tweets data for frontend, deployed to Azure App Service (Python + Flask + Sqlalchemy)

Web Page:
- Web application deployed to Azure App Service (Web App) - used to present data for end user (React + HTML + CSS)

Database:
- Azure SQL Server - used to store sentiment results (MSSQL Server)

External Services:
- Azure Text Analytics API - used to compute sentiment
- Azure Translator API - used to translate tweets into english language
- Twitter API - used to fetch tweets for provided hashtags

## TODO
- [X] Prepare cron script
- [X] Prepare React boilerplate
- [X] Prepare Database boilerplate
- [X] Register developer account at twitter page and test their API
- [X] Connect to Text Analytics API
- [X] Prepare welcome page with input field for web app
- [X] Deploy React app ([Deploy from VS Code](https://azure.microsoft.com/pl-pl/resources/videos/build-and-deply-nodejs-and-react-apps-with-vscode-appservice-and-cosmosdb/))
- [X] Count sentiment for given hashtag
- [X] Prepare react component showing sentiment score
- [X] Prepare endpoint returning sentiment and example tweets for given hashtag
- [X] Integrate cron with database
- [X] Integrate backend with database
- [X] Integrate react frontend with python backend