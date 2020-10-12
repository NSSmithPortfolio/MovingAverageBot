from binance.client import Client
import math
import smtplib

# Control variables
Each_Position_USD = 100

# Binance API
pub = 'ADD'
sec = 'ADD'
client = Client(pub, sec, tld='us')


def buy(market):
    price = check_price(market)
    amount_to_order = amount_to_buy(price)
    no_partial_fills = cancel_existing_orders(market, price)
    if no_partial_fills:
        order_id = send_buy_order(market, price, amount_to_order)
    else:
        print("Partially filled previous order or of same price, holding off on re-ordering")
        order_id = 0

    return order_id


def check_price(market):
    ticker = client.get_ticker(symbol=market)
    price = float(ticker['lastPrice'])

    return price


def amount_to_buy(price):
    amount = Each_Position_USD / price
    amount_precisioned = adjust_precision(amount)

    return amount_precisioned


def adjust_precision(amount):
    factor = 10 ** 2  # 2 is number of decimals

    return math.floor(amount * factor) / factor


def cancel_existing_orders(market, price):
    orders = client.get_open_orders(symbol=market)

    for order in orders:
        order_id = order['orderId']
        quantity_filled = float(order['executedQty'])
        order_price = float(order['price'])
        if quantity_filled == 0 and order_price != price:  # order tried with no fills, cancel and retry
            print("Cancelling previous unfilled order of different price")
            client.cancel_order(
                symbol=market,
                orderId=order_id)
        else:  # order partially filled
            print("Found an order partially filled or of same price")
            return False

    return True


def send_buy_order(market, price, amount_to_order):
    if amount_to_order == 0.0:
        if market == 'BTCUSD':
            amount_to_order = 0.007
        elif market == 'ETHUSD':
            amount_to_order = 0.1500
        else:
            print("amount to order is 0.0 and not BTC or ETH")
            return 0
    if market == 'XLMUSD':
        amount_to_order = 700

    if market == 'XRPUSD':
        amount_to_order = 200

    print("About to order", amount_to_order, "at", price, "of", market)
    try:
        # order = client.order_limit_buy(
        order = client.order_market_buy(
            symbol=market,
            quantity=amount_to_order)
        # price=price)
        client_order_number = order[
            'orderId']  # CASE SENSITIVE.  Find the rest here: https://github.com/binance-us/binance-official-api-docs/blob/master/rest-api.md#new-order--trade
        print("client_order_number: ", client_order_number)
        subject = "Buying " + str(market) + " at " + str(price)
        send_buy_email(subject, price)
        return client_order_number

    except:
        print("Error: low balance")
        return 0


def send_buy_email(subject, text):
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
