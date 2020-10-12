from binance.client import Client
import math
import smtplib

# Binance API
pub = ''
sec = ''
client = Client(pub, sec, tld='us')


def sell(market, amount_owned):
    price = check_price(market)
    amount_to_sell = get_amount_to_sell(price, amount_owned, market)
    buy_price = get_buy_price(market)
    profit = float(buy_price) / price

    print("About to place sell order at", amount_to_sell, "of", amount_to_sell, "for profit of", profit, "%")
    order_id = send_sell_order(market, amount_to_sell, profit)

    return order_id


def shorten_market(market):
    market = market.replace('USD', '')
    return market


def get_buy_price(market):
    buy_price = get_trades(market)

    return buy_price


def get_trades(market):
    trades = client.get_my_trades(symbol=market)

    for trade in trades:
        if trade['isBuyer']:
            return trade['price']

    return 0


def check_price(market):
    ticker = client.get_ticker(symbol=market)
    price = float(ticker['lastPrice'])

    return price


def get_amount_to_sell(price, balance, market):
    amount = balance / price
    amount_precisioned = adjust_precision(amount, market)

    return amount_precisioned


def adjust_precision(amount, market):
    if market == "XLMUSD":
        factor = 10 ** 1  # 1 is number of decimals
    elif market == "XRPUSD":
        factor = 10 ** 1  # 1 is number of decimals
    elif market == "BTCUSD":
        factor = 10 ** 5
    else:
        factor = 10 ** 2  # 2 is number of decimals

    result = math.floor(amount * factor) / factor

    return result


def send_sell_order(market, amount_to_sell, profit):
    try:
        order = client.order_market_sell(
            symbol=market,
            quantity=amount_to_sell)
        client_order_number = order['orderId']
        price = check_price(market)

        print("About to set up email")
        subject = "Selling " + market + " at " + str(price) + " for " + str(profit) + "% profit"
        print("About to send email")
        send_sell_email(subject, price)

        return client_order_number
    except:
        print("Error selling")


def send_sell_email(subject, text):
    """
    Purpose: send an email with argument as message warning there was an issue
    Called by: sell_position (when issue occurs with a sell)
    Arguments: email message
    Returns: none
    """
    msg = 'Subject: {}\n\n{}'.format(subject, text)

    # Email pwd
    user = 'ADD USERNAME'
    pwd = 'ADD PASSWORD'

    server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
    server.ehlo()
    server.starttls()

    # Next, log in to the server
    server.login(user, pwd)

    # Send the mail
    server.sendmail('ADD FROM EMAIL', 'ADD TO EMAIL', msg)
