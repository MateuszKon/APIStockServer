# APIStockServer

## Intro

APIStockServer uses [Finnhub](https://finnhub.io/) API for controlling configured stock allerts, (including asking Finnhub for current stock prices for that matter). Server is also used as wrapper for listing all stocks from Finnhub, as Finnhub API does not allow limitting requested data (using limit and page parameters).
Server also is used for fetching data from [GoldAPI](https://goldapi.io/) for tracking current prices of precious metals (in comparasion with coresponding ETF from Finhub)

## What do you need to do to start your own server?

- get authentication-key from [finnhub](https://finnhub.io/dashboard) (you need to register an account) and put it into a file (as a text).
- set environment variable APISTOCK_KEY_FILE with path to created file containing authentication-key (absolut path or relative to project working directory)

