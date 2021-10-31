import asyncio

import telebot
from binance import AsyncClient

from config import load_config, write_config
import time
import traceback


class Notificator:
    def __init__(self):
        self.client = None
        self.counter = {}
        self.config = load_config()
        self.bot = telebot.TeleBot(self.config["token"])
        self.interval = self.config['interval']

    def process_condition(
        self, condition, sup_condition, sub_message, ticker, price
    ):
        current_symbol = ticker["symbol"]
        if condition:
            self.counter[(current_symbol, price)][0] = (
                "<" if self.counter[(current_symbol, price)][0] == ">" else ">"
            )
            if sup_condition:
                self.bot.send_message(
                    self.config["chat_id"],
                    text=self.text(ticker, price, sub_message),
                )
                self.counter[(current_symbol, price)][1] = time.time()
                # subscribed_tickers[current_symbol].remove(price)
                # if len(subscribed_tickers[current_symbol]) == 0:
                #     subscribed_tickers.pop(current_symbol)
                # write_config(self.config)

    @staticmethod
    def text(ticker, price, x):
        current_symbol = ticker["symbol"]
        return (
            f"*****{current_symbol}*****\n{current_symbol} {x}"
            f" {price}.\n\n"
            f'Текущая цена {float(ticker["price"])}!'
            f"\n**********"
        )

    async def run_notificator(self):
        self.client = AsyncClient()
        while True:
            try:
                subscribed_tickers = self.config["tickers"]
                tickers = await self.client.get_all_tickers()
                if self.config["print_all_tickers"]:
                    print(tickers)
                    raise Exception("Printed")
                for ticker in tickers:
                    current_symbol = ticker["symbol"]
                    if current_symbol in subscribed_tickers:
                        prices = subscribed_tickers[current_symbol]
                        for price in prices:
                            if (current_symbol, price) not in self.counter:
                                self.counter[(current_symbol, price)] = [
                                    "",
                                    None,
                                ]
                            if (
                                len(self.counter[(current_symbol, price)][0])
                                == 0
                            ):
                                if float(ticker["price"]) > price:
                                    self.counter[(current_symbol, price)][
                                        0
                                    ] = ">"
                                else:
                                    self.counter[(current_symbol, price)][
                                        0
                                    ] = "<"
                            if (
                                len(self.counter[(current_symbol, price)][0])
                                == 1
                            ):
                                self.process_condition(
                                    float(ticker["price"]) > price
                                    and self.counter[(current_symbol, price)][0]
                                    == "<",
                                    self.counter[(current_symbol, price)][1]
                                    is None
                                    or time.time()
                                    - self.counter[(current_symbol, price)][1]
                                    > self.interval,
                                    "превысила отметку",
                                    ticker,
                                    price,
                                )
                                self.process_condition(
                                    float(ticker["price"]) < price
                                    and self.counter[(current_symbol, price)][0]
                                    == ">",
                                    self.counter[(current_symbol, price)][1]
                                    is None
                                    or time.time()
                                    - self.counter[(current_symbol, price)][1]
                                    > self.interval,
                                    "опустилась ниже отметки",
                                    ticker,
                                    price,
                                )
                await asyncio.sleep(1)
            except BaseException as ex:
                traceback.print_exc()
                break
        await self.client.close_connection()


def main():
    notificator = Notificator()
    asyncio.run(notificator.run_notificator())


if __name__ == "__main__":
    main()
