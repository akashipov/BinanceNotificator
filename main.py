import asyncio

import telebot
from binance import AsyncClient

from config import load_config, write_config


class Notificator:
    def __init__(self):
        self.client = None
        self.counter = {"BTCUSDT": "<"}
        self.config = load_config()
        self.bot = telebot.TeleBot(self.config["token"])

    def process_condition(self, condition, sub_message, ticker):
        current_symbol = ticker["symbol"]
        if condition:
            subscribed_tickers = self.config["tickers"]
            self.bot.send_message(
                self.config["chat_id"],
                text=self.text(ticker, sub_message),
            )
            self.counter.pop(current_symbol)
            subscribed_tickers.pop(current_symbol)
            write_config(self.config)

    def text(self, ticker, x):
        subscribed_tickers = self.config["tickers"]
        current_symbol = ticker["symbol"]
        return (
            f"*****{current_symbol}*****\n{current_symbol} {x}"
            f" {subscribed_tickers[current_symbol]}.\n\n"
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
                        if current_symbol not in self.counter:
                            self.counter[current_symbol] = ""
                        if len(self.counter[current_symbol]) == 0:
                            if (
                                float(ticker["price"])
                                > subscribed_tickers[current_symbol]
                            ):
                                self.counter[current_symbol] = ">"
                            else:
                                self.counter[current_symbol] = "<"
                        if len(self.counter[current_symbol]) == 1:
                            self.process_condition(
                                float(ticker["price"])
                                > subscribed_tickers[current_symbol]
                                and self.counter[current_symbol] == "<",
                                "превысила отметку",
                                ticker,
                            )
                            self.process_condition(
                                float(ticker["price"])
                                < subscribed_tickers[current_symbol]
                                and self.counter[current_symbol] == ">",
                                "опустилась ниже отметки",
                                ticker,
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
