import os
import logging
from dotenv import load_dotenv
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
from getpass import getpass

# Load environment variables from .env file (optional)
load_dotenv()

# Setup logging
logger = logging.getLogger("BinanceBot")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("binance_bot.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Basic trading bot class
class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.API_URL = "https://testnet.binancefuture.com/fapi"

        try:
            self.client.futures_account()
            logger.info(" API credentials verified.")
        except BinanceAPIException as e:
            logger.error(f"API verification failed: {e}")
            print(" API Key/Secret invalid or testnet access issue.")
            exit()

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            if order_type == "MARKET":
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=ORDER_TYPE_MARKET,
                    quantity=quantity
                )
            elif order_type == "LIMIT":
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=ORDER_TYPE_LIMIT,
                    timeInForce=TIME_IN_FORCE_GTC,
                    quantity=quantity,
                    price=price
                )
            else:
                raise ValueError("Unsupported order type")

            logger.info(f"Order placed: {order}")
            return order

        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e}")
            print("API Error:", e)
        except Exception as e:
            logger.error(f"Unexpected Error: {e}")
            print(" Unexpected Error:", e)

# CLI Interface
def main():
    print(" Binance Futures Testnet Trading Bot ")

    api_key = os.getenv("API_KEY") or input("Enter your Binance API Key: ")
    api_secret = os.getenv("API_SECRET") or getpass("Enter your Binance Secret Key: ")

    bot = BasicBot(api_key, api_secret)

    while True:
        symbol = input("Enter Symbol (e.g., BTCUSDT): ").upper()
        side = input("Enter Side (BUY or SELL): ").upper()
        order_type = input("Order Type (MARKET or LIMIT): ").upper()
        quantity = float(input("Enter Quantity: "))
        price = None

        if order_type == "LIMIT":
            price = input("Enter Limit Price: ")

        result = bot.place_order(
            symbol=symbol,
            side=SIDE_BUY if side == "BUY" else SIDE_SELL,
            order_type=order_type,
            quantity=quantity,
            price=price
        )

        print(" Order Result:", result)
        again = input("Place another order? (y/n): ")
        if again.lower() != "y":
            break

if __name__ == "__main__":
    main()
