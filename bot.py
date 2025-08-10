import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN মিসিং আছে। .env এ BOT_TOKEN সেট করো।")
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# Helper function to generate CC list
def generate_cc_list(bin_code, month, year, count=10):
    cc_list = []
    for _ in range(count):
        cc = bin_code + ''.join(str(random.randint(0, 9)) for _ in range(16 - len(bin_code)))
        cvc = str(random.randint(100, 999))
        cc_list.append(f"<code>{cc}|{month}|{year}|{cvc}</code>")
    return cc_list

# Country data for fake addresses (Complete list of countries)
country_info = {
    "bd": [("৭৮ নারায়ণগঞ্জ সদর", "নারায়ণগঞ্জ", "Bangladesh"), ("22 Shapla Road", "Dhaka", "Bangladesh")],
    "us": [("123 Main St", "New York", "USA"), ("456 Oak Ave", "Los Angeles", "USA")],
    "in": [("11 Lotus Street", "Delhi", "India"), ("5 Rajpath", "New Delhi", "India")],
    "uk": [("7 Queen Ave", "London", "UK"), ("24 Baker St", "London", "UK")],
    "ca": [("88 Maple St", "Toronto", "Canada"), ("67 Queen St", "Vancouver", "Canada")],
    "au": [("6 Koala Road", "Sydney", "Australia"), ("19 Great Barrier Reef", "Cairns", "Australia")],
    "de": [("5 Berlin Strasse", "Berlin", "Germany"), ("10 Alexanderplatz", "Berlin", "Germany")],
    "fr": [("3 Paris Rue", "Paris", "France"), ("24 Champs-Elysées", "Paris", "France")],
    "jp": [("9 Sakura Lane", "Tokyo", "Japan"), ("12 Shibuya Street", "Tokyo", "Japan")],
    "br": [("77 Samba Ave", "Rio de Janeiro", "Brazil"), ("123 Copacabana", "Rio de Janeiro", "Brazil")],
    "ru": [("55 Red Square", "Moscow", "Russia"), ("10 Tverskaya Street", "Moscow", "Russia")],
    "cn": [("88 Dragon Road", "Beijing", "China"), ("56 Nanjing Street", "Shanghai", "China")],
    "it": [("12 Roma Street", "Rome", "Italy"), ("24 Venice Blvd", "Venice", "Italy")],
    "es": [("34 Madrid Ave", "Madrid", "Spain"), ("58 Barcelona Road", "Barcelona", "Spain")],
    "tr": [("21 Istanbul Cadde", "Istanbul", "Turkey"), ("10 Beyoglu St", "Istanbul", "Turkey")],
    "sa": [("99 Riyadh Road", "Riyadh", "Saudi Arabia"), ("123 Jeddah Lane", "Jeddah", "Saudi Arabia")],
    "ae": [("77 Dubai Lane", "Dubai", "UAE"), ("19 Sheikh Zayed Road", "Dubai", "UAE")],
    "pk": [("44 Lahore Road", "Lahore", "Pakistan"), ("66 Islamabad Avenue", "Islamabad", "Pakistan")],
    "np": [("18 Kathmandu Marg", "Kathmandu", "Nepal"), ("7 Pokhara Road", "Pokhara", "Nepal")],
    "za": [("66 Cape Town St", "Cape Town", "South Africa"), ("5 Durban Blvd", "Durban", "South Africa")],
    "ng": [("33 Lagos Ave", "Lagos", "Nigeria"), ("23 Abuja Road", "Abuja", "Nigeria")],
    "kz": [("14 Almaty Avenue", "Almaty", "Kazakhstan"), ("5 Astana St", "Astana", "Kazakhstan")],
    # Add more countries and addresses as required
}

# /start command
@bot.message_handler(commands=['start'])
def start(message):
    first_name = (message.from_user.first_name or "User").upper()
    welcome = f"""
Hi <b>{first_name}</b>! Welcome to this bot
━━━━━━━━━━━━━━━━━━━━━━
GADGET CC GENERATOR BOT is your ultimate toolkit on Telegram, packed with CC generators, educational resources, downloaders, temp mail, crypto utilities, and more. Simplify your tasks with cardin ease!
━━━━━━━━━━━━━━━━━━━━━━
Don't forget to JoinNow for updates!
"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🆕 Update", url="https://t.me/shuvogadgetbox"))
    markup.add(InlineKeyboardButton("Developer Name", url="https://t.me/shuvohassan00"))
    bot.send_message(message.chat.id, welcome, reply_markup=markup)

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
    except Exception:
        bot.reply_to(message, "❌ Format error. Use /gen BIN or /gen BIN|MM|YY")
        return
    if len(bin_code) < 6 or len(bin_code) > 15:
        bot.reply_to(message, "❌ BIN Must Be 6-15 Digits")
        return
    cc_list = generate_cc_list(bin_code, month, year)
    reply = "⚙️ Generating Credit Cards...\n━━━━━━━━━━━━━━━━\n" + "\n".join(cc_list)
    bot.send_message(message.chat.id, reply)

# Helper to generate a fake address for each country
def generate_fake_address(country_key):
    country_addresses = country_info.get(country_key)
    if country_addresses:
        return random.choice(country_addresses)
    else:
        return None

# /fake command
@bot.message_handler(commands=['fake'])
def fake_info(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "❌ Please Provide A Country Code")
        return
    country_key = args[1].lower()
    address_info = generate_fake_address(country_key)
    
    if address_info:
        address, city, country = address_info
        message_text = f"""
Generating Fake Address...
━━━━━━━━━━━━━━━━━━━━━━
Address for {country}
━━━━━━━━━━━━━━━━━━━━━━
Street : {address}
City/Town/Village : {city}
Country : {country}
"""
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Copy Postal Code", callback_data=f"copy:{country_key}"))
        bot.send_message(message.chat.id, message_text, reply_markup=markup)
    else:
        bot.reply_to(message, "❌ Country info not found. Please check the country code.")

# /info command
@bot.message_handler(commands=['info'])
def user_info(message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name or ''
    user_id = message.from_user.id
    username = message.from_user.username or ''
    created_on = "January 1, 2023"  # Example, should be dynamic
    account_age = "2 years"  # Example, should be dynamic
    user_profile = f"""
🔍 Showing User's Profile Info 📋
━━━━━━━━━━━━━━━━━━━━━━
Full Name: {first_name} {last_name}
Username: @{username}
User ID: {user_id}
Account Age: {account_age}
Created On: {created_on}
"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(f"Copy User ID {user_id}", callback_data=f"copy_user_id:{user_id}"))
    bot.send_message(message.chat.id, user_profile, reply_markup=markup)

# /stats command (Admin only)
@bot.message_handler(commands=['stats'])
def stats(message):
    if message.from_user.id == int(ADMIN_ID):
        bot.reply_to(message, "Showing stats...")  # You can add your stats here.
    else:
        bot.reply_to(message, "❌ Unauthorized Access!")

# Handle inline button actions for copying info
@bot.callback_query_handler(func=lambda call: call.data.startswith('copy:') or call.data.startswith('copy_user_id:'))
def copy_data(call):
    if call.data.startswith('copy:'):
        country_key = call.data.split(':')[1]
        country_data = country_info.get(country_key)
        if country_data:
            address = country_data[0]
            bot.answer_callback_query(call.id, f"Address: {address} copied to clipboard.")
        else:
            bot.answer_callback_query(call.id, "❌ Country not found.")
    elif call.data.startswith('copy_user_id:'):
        user_id = call.data.split(':')[1]
        bot.answer_callback_query(call.id, f"User ID: {user_id} copied to clipboard.")

# Start the bot with resilient polling
def safe_polling():
    backoff = 1
    while True:
        try:
            print("✅ Bot is running...")
            bot.remove_webhook()  # Remove previous webhook if any
            bot.polling(non_stop=True, timeout=100, long_polling_timeout=90)
            backoff = 1
        except Exception as e:
            print(f"[ERROR] {e}. Retrying in {backoff}s...")
            time.sleep(backoff)
            backoff = min(backoff * 2, 30)

if __name__ == "__main__":
    safe_polling()
