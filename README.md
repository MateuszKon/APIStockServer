# APIStockServer

## Intro

APIStockServer currently checks current precious metals ETF prices and compares them with spot prices of metals. 
Calculates discount of ETF and when discount threshold is exceeded, email alerts are send to subscribed users 
(current server version stores subscribed users emails in txt files).
APIStockServer uses [Finnhub](https://finnhub.io/) API, [GoldAPI](https://goldapi.io/) API, so propper API keys are necessary for running server.

APIStockServer will be developed to work with sepearte web-server project (APIStock proejct) and SQL database. In the future web-server 

## What do you need to do to start your own server?

- install requirements specified by requirements.txt
- get authentication-key from [finnhub](https://finnhub.io/dashboard) and  [GoldAPI](https://goldapi.io/) (you need to register accounts) and put them into seperate files (as a plain text).
- in config.ini select path for authentication-key files (section 'API Keys' keys 'finnhub' and 'goldapi')
- subscribed users email should be stored in txt file (each email in sepearte line) 
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





