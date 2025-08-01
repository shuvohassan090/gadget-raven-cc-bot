import logging
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, Timeout
from urllib3.exceptions import ProtocolError

# ডিবাগ লগ চালু
telebot.logger.setLevel(logging.DEBUG)

# .env লোড
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN মিসিং আছে। .env ফাইলে BOT_TOKEN=set করো.")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

def animated_reply(chat_id, text, delay=1.0):
    try:
        msg = bot.send_message(chat_id, f"<b>{text}</b>")
        time.sleep(delay)
        try:
            bot.delete_message(chat_id, msg.message_id)
        except Exception:
            pass
    except Exception:
        pass

@bot.message_handler(commands=['start'])
def start(message):
    name = (message.from_user.first_name or "User").upper()
    animated_reply(message.chat.id, "Loading Welcome Message...", 1)
    welcome = f"Hi <b>{name}</b>! This is a test bot. Only Update button below."
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Update", url="https://t.me/shuvogadgetbox"))
    bot.send_message(message.chat.id, welcome, reply_markup=markup)

def safe_polling():
    while True:
        try:
            print("🤖 পোলিং শুরু হচ্ছে...")
            bot.polling(non_stop=True, timeout=100, long_polling_timeout=90)
        except (ConnectionError, ProtocolError, Timeout) as e:
            print(f"[WARN] কানেকশন এরর: {e}. ৫ সেকেন্ড পরে রি-ট্রাই করছি...")
            time.sleep(5)
        except Exception as e:
            print(f"[ERROR] অজানা এরর: {e}. ১০ সেকেন্ড পরে রি-ট্রাই করছি...")
            time.sleep(10)

if __name__ == "__main__":
    safe_polling()
