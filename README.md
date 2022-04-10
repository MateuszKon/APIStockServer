# APIStockServer

## Intro

APIStockServer currently checks current precious metals ETF prices and compares them with spot prices of metals. 
Calculates discount of ETF and when discount threshold is exceeded, email alerts are sent to subscribed users 
(current server version stores subscribed users emails in txt files).
APIStockServer uses [Finnhub](https://finnhub.io/) API, [GoldAPI](https://goldapi.io/) API, so proper API keys are necessary for running server.

APIStockServer will be developed to work with sepearte client project [APIStock](https://github.com/MateuszKon/APIStock) and SQL database.
 In the future APIStockServer will:
- handle users alerts generated on web-server (alerts, users etc., stored in database)
- answer to API requests (REST API)

## SQL Database

SQL Database of APIStockServer can be presented by this diagram
![APIStock.png](https://github.com/MateuszKon/APIStockServer/blob/master/data/APIStock.png "APIStock.png")

## What do you need to do to start your own server?

- install requirements specified by requirements.txt
- get authentication-key from [finnhub](https://finnhub.io/dashboard) and  [GoldAPI](https://goldapi.io/) (you need to register accounts) and put them into separate files (as a plain text).
- in config.ini select path for authentication-key files (section 'API Keys' keys 'finnhub' and 'goldapi')
- subscribed users email should be stored in txt file (each email in separate line) 
- in config.ini select path for file with emails (section 'Email Sender' key 'receiver_emails_path')
- in config.ini other keys of section 'Email Sender' might be used without changing (email account created for this project) 

## Running server

To start APIStockServer run file APIStockServer/APIStockServer/server.py
For proper modules import run server using PyCharm or using command line (tested on Ubuntu and Windows7): cd to project folder (APIStockServer not APIStockServer/APIStockServer) and run:

*~/APIStockServer$ python -m APIStockServer.server*

## Used frameworks/modules

- API requests (requests)
- web scraping (BeautifulSoup)
- scheduler (schedule)





