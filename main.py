import asyncio

import telebot
from binance import AsyncClient

from config import load_config, write_config


class Notificator:
    def __init__(self):
        self.client = None
        self.counter = {}
        self.config = load_config()
        self.bot = telebot.TeleBot(self.config["token"])

    def process_condition(self, condition, sub_message, ticker, price):
        current_symbol = ticker["symbol"]
        if condition:
            subscribed_tickers = self.config["tickers"]
            self.bot.send_message(
                self.config["chat_id"],
                text=self.text(ticker, price, sub_message),
            )
            self.counter.pop((current_symbol, price))
            subscribed_tickers[current_symbol].remove(price)
            if len(subscribed_tickers[current_symbol]) == 0:
                subscribed_tickers.pop(current_symbol)
            write_config(self.config)

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
                                self.counter[(current_symbol, price)] = ""
                            if len(self.counter[(current_symbol, price)]) == 0:
                                if float(ticker["price"]) > price:
                                    self.counter[(current_symbol, price)] = ">"
                                else:
                                    self.counter[(current_symbol, price)] = "<"
                            if len(self.counter[(current_symbol, price)]) == 1:
                                self.process_condition(
                                    float(ticker["price"]) > price
                                    and self.counter[(current_symbol, price)]
                                    == "<",
                                    "превысила отметку",
                                    ticker,
                                    price,
                                )
                                self.process_condition(
                                    float(ticker["price"]) < price
                                    and self.counter[(current_symbol, price)]
                                    == ">",
                                    "опустилась ниже отметки",
                                    ticker,
                                    price,
                                )

                await asyncio.sleep(1)
            except BaseException as ex:
                print(ex)
                break
        await self.client.close_connection()

    async def f(self):
        c = AsyncClient()
        tickers = await c.get_all_tickers()
        print(tickers)


def main():
    notificator = Notificator()
    asyncio.run(notificator.run_notificator())


if __name__ == "__main__":
    main()
