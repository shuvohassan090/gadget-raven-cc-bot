import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import time
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, Timeout
from urllib3.exceptions import ProtocolError

# Load environment
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")  # Future use if needed

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN মিসিং আছে। .env এ BOT_TOKEN সেট করো।")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# Safe animated reply with simple retry/backoff
def animated_reply(chat_id, text, delay=1.2, max_attempts=2):
    msg = None
    for attempt in range(1, max_attempts + 1):
        try:
            msg = bot.send_message(chat_id, f"<b>{text}</b>")
            break
        except Exception as e:
            print(f"[animated_reply send attempt {attempt}] failed: {e}")
            time.sleep(0.3 * attempt)
    if not msg:
        return
    time.sleep(delay)
    for attempt in range(1, max_attempts + 1):
        try:
            bot.delete_message(chat_id, msg.message_id)
            break
        except Exception as e:
            print(f"[animated_reply delete attempt {attempt}] failed: {e}")
            time.sleep(0.3 * attempt)

# Helper to generate CC list
def generate_cc_list(bin_code, month, year, count=10):
    cc_list = []
    for _ in range(count):
        cc = bin_code + ''.join(str(random.randint(0, 9)) for _ in range(16 - len(bin_code)))
        cvc = str(random.randint(100, 999))
        cc_list.append(f"<code>{cc}|{month}|{year}|{cvc}</code>")
    return cc_list

# /start command
@bot.message_handler(commands=['start'])
def start(message):
    first_name = (message.from_user.first_name or "User").upper()
    animated_reply(message.chat.id, "Loading Welcome Message...", 1)
    welcome = (
        f"Hi <b>{first_name}</b>! Welcome to this bot\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "GADGET CC GENERATOR BOT is your ultimate toolkit on Telegram, packed with CC generators, educational resources, downloaders, temp mail, crypto utilities, and more. Simplify your tasks with cardin ease!\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Don't forget to JoinNow for updates!"
    )
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🆕 Update", url="https://t.me/shuvogadgetbox"))
    bot.send_message(message.chat.id, welcome, reply_markup=markup)

# Re-generate button helper
def cc_markup(args):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔁 Re-generate", callback_data=f"regen:{args}"))
    return markup

# /gen command
@bot.message_handler(commands=['gen'])
def gen_cc(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(0.5)
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, "❌ Format: /gen BIN or /gen BIN|MM|YY")
        return

    args = parts[1]
    try:
        sub = args.split('|')
        bin_code = sub[0]
        month = sub[1] if len(sub) > 1 and sub[1].isdigit() else str(random.randint(1, 12)).zfill(2)
        year = sub[2] if len(sub) > 2 and sub[2].isdigit() else str(random.randint(25, 30))
    except Exception as e:
        print(f"Error parsing /gen args: {e}")
        bot.reply_to(message, "❌ Format error. Use /gen BIN or /gen BIN|MM|YY")
        return

    cc_list = generate_cc_list(bin_code, month, year)
    reply = "⚙️ Generating Credit Cards...\n━━━━━━━━━━━━━━━━\n" + "\n".join(cc_list)
    markup = cc_markup(args)
    bot.send_message(message.chat.id, reply, reply_markup=markup)

# Re-generate callback
@bot.callback_query_handler(func=lambda call: call.data.startswith('regen:'))
def re_generate(call):
    args = call.data.split(':', 1)[1]
    try:
        sub = args.split('|')
        bin_code = sub[0]
        month = sub[1] if len(sub) > 1 and sub[1].isdigit() else str(random.randint(1, 12)).zfill(2)
        year = sub[2] if len(sub) > 2 and sub[2].isdigit() else str(random.randint(25, 30))
        cc_list = generate_cc_list(bin_code, month, year)
        reply = "⚙️ Re-generating Credit Cards...\n━━━━━━━━━━━━━━━━\n" + "\n".join(cc_list)
        markup = cc_markup(args)
        bot.edit_message_text(
            reply,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )
        bot.answer_callback_query(call.id, "Re-generated!")
    except Exception as e:
        print(f"Error in regen callback: {e}")
        bot.answer_callback_query(call.id, "❌ Error occurred while re-generating.")

# Full country info mapping
country_info = {
    "usa": ("123 Raven Lane", "New York", "USA"),
    "us": ("123 Raven Lane", "New York", "USA"),
    "bangladesh": ("22 Shapla Road", "Dhaka", "Bangladesh"),
    "bd": ("22 Shapla Road", "Dhaka", "Bangladesh"),
    "india": ("11 Lotus Street", "Delhi", "India"),
    "in": ("11 Lotus Street", "Delhi", "India"),
    "uk": ("7 Queen Ave", "London", "UK"),
    "canada": ("88 Maple St", "Toronto", "Canada"),
    "ca": ("88 Maple St", "Toronto", "Canada"),
    "germany": ("5 Berlin Strasse", "Berlin", "Germany"),
    "de": ("5 Berlin Strasse", "Berlin", "Germany"),
    "france": ("3 Paris Rue", "Paris", "France"),
    "fr": ("3 Paris Rue", "Paris", "France"),
    "japan": ("9 Sakura Lane", "Tokyo", "Japan"),
    "jp": ("9 Sakura Lane", "Tokyo", "Japan"),
    "australia": ("6 Koala Road", "Sydney", "Australia"),
    "au": ("6 Koala Road", "Sydney", "Australia"),
    "brazil": ("77 Samba Ave", "Rio de Janeiro", "Brazil"),
    "br": ("77 Samba Ave", "Rio de Janeiro", "Brazil"),
    "russia": ("55 Red Square", "Moscow", "Russia"),
    "ru": ("55 Red Square", "Moscow", "Russia"),
    "china": ("88 Dragon Road", "Beijing", "China"),
    "cn": ("88 Dragon Road", "Beijing", "China"),
    "italy": ("12 Roma Street", "Rome", "Italy"),
    "it": ("12 Roma Street", "Rome", "Italy"),
    "spain": ("34 Madrid Ave", "Madrid", "Spain"),
    "es": ("34 Madrid Ave", "Madrid", "Spain"),
    "turkey": ("21 Istanbul Cadde", "Istanbul", "Turkey"),
    "tr": ("21 Istanbul Cadde", "Istanbul", "Turkey"),
    "saudi": ("99 Riyadh Road", "Riyadh", "Saudi Arabia"),
    "sa": ("99 Riyadh Road", "Riyadh", "Saudi Arabia"),
    "uae": ("77 Dubai Lane", "Dubai", "UAE"),
    "ae": ("77 Dubai Lane", "Dubai", "UAE"),
    "pakistan": ("44 Lahore Road", "Lahore", "Pakistan"),
    "pk": ("44 Lahore Road", "Lahore", "Pakistan"),
    "nepal": ("18 Kathmandu Marg", "Kathmandu", "Nepal"),
    "np": ("18 Kathmandu Marg", "Kathmandu", "Nepal"),
    "south africa": ("66 Cape Town St", "Cape Town", "South Africa"),
    "za": ("66 Cape Town St", "Cape Town", "South Africa"),
    "nigeria": ("33 Lagos Ave", "Lagos", "Nigeria"),
    "ng": ("33 Lagos Ave", "Lagos", "Nigeria")
}

# /fake command
@bot.message_handler(commands=['fake'])
def fake_info(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "❌ Format: /fake country_name or code (e.g. /fake bd)")
        return

    country_key = args[1].lower()
    info = country_info.get(country_key)
    if info:
        address, city, country = info
        message_text = f"🏠 Address: {address}\n🏙️ City: {city}\n🌍 Country: {country}"
    else:
        message_text = "❌ Country info not found. Please check the country code."
    bot.reply_to(message, message_text)

# Fallback handler
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.reply_to(message, "❓ Unknown command. Try /start, /gen BIN, or /fake country")

# Resilient polling loop
def safe_polling():
    backoff = 1
    while True:
        try:
            print("✅ Bot is running...")
            bot.polling(non_stop=True, timeout=100, long_polling_timeout=90)
            backoff = 1
        except (ConnectionError, ProtocolError, Timeout) as e:
            print(f"[WARN] কানেকশন এরর: {e}. {backoff}s পরে রি-ট্রাই করছি...")
            time.sleep(backoff)
            backoff = min(backoff * 2, 30)
        except Exception as e:
            print(f"[ERROR] অজানা এরর: {e}. ১০ সেকেন্ড পরে রি-ট্রাই করছি...")
            time.sleep(10)
            backoff = 1

if __name__ == "__main__":
    safe_polling()
