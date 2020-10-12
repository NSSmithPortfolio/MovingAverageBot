import logging
import time
from scraper import *
from check_account import *
from buy import *
from sell import *
from datetime import datetime

logging.basicConfig(filename='operations.log', format='%(asctime)s - %(message)s', level=logging.INFO)
logging.info('Starting up')


def main():
    """
    Purpose: main section of application, a few settings at top that run the app
    Arguments: none
    Returns: none
    """

    loop = 0

    while 1 == 1:
        loop += 1
        print("Loop Number:", loop)

        now = datetime.now()
        dt_string = now.strftime("%m/%d %H:%M:%S")
        print("date and time =", dt_string)

        coins = get_currently_trading()
        for coin in coins:
            prices_df = get_ma_data(coin)
            if prices_df['success']:
                short_ma = prices_df['5-DayMA']
                long_ma = prices_df['20-DayMA']
                percent = ((short_ma / long_ma) * 100) - 100
                percent = round(percent, 1)
                rsi = prices_df['9-DayRSI']
                current_price = check_price(coin)

                if (short_ma > long_ma) and (rsi > 30):
                    print("Detected", coin, "is above golden cross - CP:", current_price, "|  5D:", short_ma, "above 20D", long_ma, "by", percent,
                          "% and 9 day RSI is above 30:", rsi)
                    amount_owned = check_amount_owned(coin)
                    if amount_owned > 0:  # don't buy
                        print("Already own $", amount_owned, "holding for now")
                    else:  # buy
                        print("Account balance:", amount_owned, "so buying")
                        logging.info('Buying ' + coin)
                        buy(coin)
                elif short_ma < long_ma:
                    print("Detected", coin, "is below death cross - CP:", current_price, "|  5D:", short_ma, "below 20D:", long_ma, "by", percent,
                          "% and 9 day RSI:", rsi)
                    amount_owned = check_amount_owned(coin)
                    if amount_owned > 0:  # sell
                        print("Selling", amount_owned, "of", coin)
                        logging.info('Selling ' + coin)
                        sell(coin, amount_owned)
                    else:
                        print("Don't own, doing nothing")
                elif rsi < 50:
                    print("Detected", coin, "is below 9 day RSI of 30 - CP:", current_price, "|  5D:", short_ma, "below 20D:", long_ma, "by", percent,
                          "% and 9 day RSI:", rsi)
                    amount_owned = check_amount_owned(coin)
                    if amount_owned > 0:  # sell
                        print("Selling", amount_owned, "of", coin)
                        logging.info('Selling ' + coin)
                        sell(coin, amount_owned)
                    else:
                        print("Don't own, doing nothing")
                else:
                    print("Detected", coin, "is HODL.  5D:", short_ma, "20D:", long_ma, "by", percent,
                          "% and 9 day RSI:", prices_df['9-DayRSI'])
            else:
                print("Issue scraping prices for", coin)

            time.sleep(2)  # pause for 2 seconds

        now = datetime.now()
        dt_string = now.strftime("%m/%d %H:%M:%S")
        print("date and time =", dt_string)

        print("Pausing for 5 minutes")
        time.sleep(300)  # Pause for 300 seconds/5 minutes


def get_currently_trading():
    """
    Purpose: return list of things we are currently trading
    Called by: calculate_trends_and_return_buys, download_binance
    Arguments: none
    Returns: array of current coins
    """

    # Testing list
    results = [
        "ADAUSD",
        "BCHUSD",
        "BTCUSD",
        "DASHUSD",
        "EOSUSD",
        "ETCUSD",
        "ETHUSD",
        "IOTAUSD",
        "LTCUSD",
        "NEOUSD",
        "OMGUSD",
        "QTUMUSD",
        "XLMUSD",
        "XRPUSD",
        "ZECUSD"
    ]

    return results


main()
