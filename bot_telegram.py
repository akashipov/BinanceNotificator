import telebot
from config import load_config

config = load_config()
bot = telebot.TeleBot(config["token"])


@bot.message_handler()
def return_message_self(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == "__main__":
    bot.infinity_polling()
