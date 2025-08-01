import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")  # Placeholder for future admin features

bot = telebot.TeleBot(BOT_TOKEN)

# Helper function to generate CCs
def generate_cc_list(bin_code, month, year, count=10):
    cc_list = []
    for _ in range(count):
        cc = bin_code + ''.join([str(random.randint(0, 9)) for _ in range(16 - len(bin_code))])
        cvc = str(random.randint(100, 999))
        cc_list.append(f"{cc}|{month}|{year}|{cvc}")
    return cc_list

# /start command
@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name.upper()
    welcome = f"""Hi {name}! Welcome to this bot
━━━━━━━━━━━━━━━━━━━━━━
GADGET CC GENERATOR BOT is your ultimate toolkit on Telegram, packed with CC generators, educational resources, downloaders, temp mail, crypto utilities, and more. Simplify your tasks with cardin ease!
━━━━━━━━━━━━━━━━━━━━━━
Don't forget to JoinNow for updates!"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🆕 Update", url="https://t.me/shuvogadgetbox"))
    bot.send_message(message.chat.id, welcome, reply_markup=markup)

# Function to create Re-generate button
def cc_markup(args):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔁 Re-generate", callback_data=f"regen:{args}"))
    return markup

# /gen command
@bot.message_handler(commands=['gen'])
def gen_cc(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1)  # Slight delay for typing effect

    args_list = message.text.split()
    if len(args_list) < 2:
        bot.reply_to(message, "❌ Format: /gen BIN or /gen BIN|MM|YY")
        return

    try:
        args = args_list[1]
        parts = args.split('|')
        bin_code = parts[0]
        month = parts[1] if len(parts) > 1 else str(random.randint(1, 12)).zfill(2)
        year = parts[2] if len(parts) > 2 else str(random.randint(25, 30))
    except Exception as e:
        print(f"Error in /gen command: {e}")
        bot.reply_to(message, "❌ Format error. Use /gen BIN or /gen BIN|MM|YY")
        return

    cc_list = generate_cc_list(bin_code, month, year)
    reply = "⚙️ Generating Credit Cards...\n━━━━━━━━━━━━━━━━\n" + "\n".join(cc_list)
    markup = cc_markup(args)
    bot.send_message(message.chat.id, reply, reply_markup=markup)

# Callback for re-generation
@bot.callback_query_handler(func=lambda call: call.data.startswith('regen:'))
def re_generate(call):
    args = call.data.split(':')[1]
    try:
        parts = args.split('|')
        bin_code = parts[0]
        month = parts[1] if len(parts) > 1 else str(random.randint(1, 12)).zfill(2)
        year = parts[2] if len(parts) > 2 else str(random.randint(25, 30))
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
        print(f"Error in callback: {e}")
        bot.answer_callback_query(call.id, "❌ Error occurred while re-generating.")

# /fake command
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

# Optional fallback handler
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.reply_to(message, "❓ Unknown command. Try /start, /gen BIN, or /fake country")

# Run bot
if __name__ == "__main__":
    print("✅ Bot is running...")
    safe_polling()
