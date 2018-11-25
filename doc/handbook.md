# CCAT Handbook


## Binance API Rate Limit
At the current time Binance rate limits are:
- 1200 requests per minute
- 10 orders per second
- 100,000 orders per 24hrs

## Exception Tables

- okexException, code = -1001, message = err
- binanceException, code = -1002, message = err
- huobiException, code = -1003, message = err
- gateException, code = -1004, message = err
- DBException, code = -2000, message = err
- EngineException, code = -3000, message = err
- ApplicationException, code = -4000, message = err

SELECT *
FROM VIEW_MARKET_TICKER_CURRENT V1
LEFT JOIN VIEW_MARKET_TICKER_CURRENT V2 ON V1.server <> V2.server AND V1.fSymbol = V2.fSymbol AND V1.tSymbol = V2.tSymbol
WHERE abs(V1.timeStamp - V2.timeStamp) < 30*1000 AND (max(V1.bid_one_price, V1.ask_one_price, V2.bid_one_price, V2.ask_one_price)
	-min(V1.bid_one_price, V1.ask_one_price, V2.bid_one_price, V2.ask_one_price)) > (abs(V1.bid_one_price-V1.ask_one_price)+abs(V2.bid_one_price-V2.ask_one_price))
ORDER BY V1.fSymbol
