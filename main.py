import asyncio

import telebot
from binance import AsyncClient

from config import load_config


async def get_tickers():
    client = AsyncClient()
    while True:
        try:
            config = load_config()
            bot = telebot.TeleBot(config['token'])
            subscribed_tickers = config['tickers']
            tickers = await client.get_all_tickers()
            if config['print_all_tickers']:
                print(tickers)
                raise Exception("Printed")
            for ticker in tickers:
                if ticker['symbol'] in subscribed_tickers:
                    if float(ticker['price']) > subscribed_tickers[ticker['symbol']]:
                        bot.send_message(config['chat_id'], text=f'*****{ticker["symbol"]}*****\n{ticker["symbol"]} превысила отметку '
                                                                 f'{subscribed_tickers[ticker["symbol"]]}.\n\n'
                                                                 f'Текущая цена {float(ticker["price"])}!'
                                                                 f'\n**********')
            await asyncio.sleep(1)
        except BaseException as ex:
            print(ex)
            break
    await client.close_connection()


def main():
    asyncio.run(get_tickers())


if __name__ == '__main__':
    main()
