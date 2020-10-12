from binance.client import Client

# Binance API
pub = 'ADD'
sec = 'ADD'
client = Client(pub, sec, tld='us')


def check_amount_owned(market):
    shortened_coin = shorten_market(market)

    balance = get_balance(shortened_coin)
    value = check_usd_value(market, balance)

    if value > 10:
        return value
    return -1


def get_balance(coin):
    # print("Getting balance of", coin)
    balance = client.get_asset_balance(asset=coin, recvWindow=50000)
    free = float(balance['free'])
    return free


def check_usd_value(market, balance):
    price = client.get_ticker(symbol=market)
    value = float(price['lastPrice']) * balance
    return value


def shorten_market(market):
    market = market.replace('USD', '')
    return market
