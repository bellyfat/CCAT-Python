# coincap usage

## usage

@coincap
[coincap api](https://coincap.io/)

## examples

### 1. get date from coincap to json files

```bash
curl --request GET   --url 'https://api.coincap.io/v2/candles?exchange=okex&interval=m1&baseId=bitcoin&quoteId=tether&start=1538323200000&end=1541001600000' > coincap_candles_okex_bitcoin_m1_201810.json
```
