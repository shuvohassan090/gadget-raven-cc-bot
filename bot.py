import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import time
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

bot = telebot.TeleBot(BOT_TOKEN)

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

# /gen command
def cc_markup(args):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔁 Re-generate", callback_data=f"regen:{args}"))
    return markup

@bot.message_handler(commands=['gen'])
def gen_cc(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1.2)
    try:
        args = message.text.split()[1]
        parts = args.split('|')
        bin_code = parts[0]
        month = parts[1] if len(parts) > 1 else str(random.randint(1, 12)).zfill(2)
        year = parts[2] if len(parts) > 2 else str(random.randint(25, 30))
    except:
        bot.reply_to(message, "❌ Format: /gen BIN or /gen BIN|MM|YY")
        return

    cc_list = []
    for _ in range(10):
        cc = bin_code + ''.join([str(random.randint(0, 9)) for _ in range(16 - len(bin_code))])
        cvc = str(random.randint(100, 999))
        cc_list.append(f"{cc}|{month}|{year}|{cvc}")

    reply = "⚙️ Generating Credit Cards...\n━━━━━━━━━━━━━━━━\n" + "\n".join(cc_list)
    markup = cc_markup(args)
    bot.send_message(message.chat.id, reply, reply_markup=markup)

# Re-generate button (edit message, no new message)
@bot.callback_query_handler(func=lambda call: call.data.startswith('regen:'))
def re_generate(call):
    args = call.data.split(':')[1]
    parts = args.split('|')
    bin_code = parts[0]
    month = parts[1] if len(parts) > 1 else str(random.randint(1, 12)).zfill(2)
    year = parts[2] if len(parts) > 2 else str(random.randint(25, 30))

    cc_list = []
    for _ in range(10):
        cc = bin_code + ''.join([str(random.randint(0, 9)) for _ in range(16 - len(bin_code))])
        cvc = str(random.randint(100, 999))
        cc_list.append(f"{cc}|{month}|{year}|{cvc}")

    reply = "⚙️ Generating Credit Cards...\n━━━━━━━━━━━━━━━━\n" + "\n".join(cc_list)
    markup = cc_markup(args)
    bot.edit_message_text(
        reply,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )
    bot.answer_callback_query(call.id, "Re-generated!")

# /fake command (All country support)
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
    "ng": ("33 Lagos Ave", "Lagos", "Nigeria"),
    "mexico": ("25 Mexico City Blvd", "Mexico City", "Mexico"),
    "mx": ("25 Mexico City Blvd", "Mexico City", "Mexico"),
    "argentina": ("19 Buenos Aires St", "Buenos Aires", "Argentina"),
    "ar": ("19 Buenos Aires St", "Buenos Aires", "Argentina"),
    "indonesia": ("77 Jakarta Road", "Jakarta", "Indonesia"),
    "id": ("77 Jakarta Road", "Jakarta", "Indonesia"),
    "thailand": ("88 Bangkok Lane", "Bangkok", "Thailand"),
    "th": ("88 Bangkok Lane", "Bangkok", "Thailand"),
    "malaysia": ("55 Kuala Lumpur St", "Kuala Lumpur", "Malaysia"),
    "my": ("55 Kuala Lumpur St", "Kuala Lumpur", "Malaysia"),
    "philippines": ("22 Manila Ave", "Manila", "Philippines"),
    "ph": ("22 Manila Ave", "Manila", "Philippines"),
    "vietnam": ("33 Hanoi Road", "Hanoi", "Vietnam"),
    "vn": ("33 Hanoi Road", "Hanoi", "Vietnam"),
    "south korea": ("44 Seoul St", "Seoul", "South Korea"),
    "kr": ("44 Seoul St", "Seoul", "South Korea"),
    "egypt": ("77 Cairo Lane", "Cairo", "Egypt"),
    "eg": ("77 Cairo Lane", "Cairo", "Egypt"),
    "morocco": ("88 Casablanca Ave", "Casablanca", "Morocco"),
    "ma": ("88 Casablanca Ave", "Casablanca", "Morocco"),
    # আরও shortcut/দেশ চাইলে এখানে যোগ করতে পারো
}

def fake_markup(postal):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📋 Copy Postal Code", callback_data=f"copy:{postal}"))
    return markup

@bot.message_handler(commands=['fake'])
def fake_address(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1.2)
    try:
        country_arg = message.text.split(maxsplit=1)[1].strip().lower()
        street, city, country = country_info.get(country_arg, country_info["usa"])
    except Exception:
        street, city, country = country_info["usa"]

    postal = str(random.randint(10000, 99999))
    address = f"""🏠 Generate Fake Address...
━━━━━━━━━━━━━━━━
Street: {street}
City: {city}
Country: {country}
Postal Code: {postal}"""
    markup = fake_markup(postal)
    bot.send_message(message.chat.id, address, reply_markup=markup)

# Copy Postal Code (alert only)
@bot.callback_query_handler(func=lambda call: call.data.startswith('copy:'))
def copy_postal(call):
    postal = call.data.split(':')[1]
    bot.answer_callback_query(call.id, f"Copied: {postal}")

# /info command
@bot.message_handler(commands=['info'])
def user_info(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1.2)
    user = message.from_user
    info = f"""🔍 Showing User's Profile Info 📋
━━━━━━━━━━━━━━━━
• Full Name: {user.first_name}
• Username: @{user.username}
• User ID: {user.id}
• Chat ID: {message.chat.id}
• Premium User: Yes
• Data Center: SIN, Singapore, SG
• Created On: June 22, 2023
• Account Age: 2 years, 1 months, 9 days
━━━━━━━━━━━━━━━━
👁 Thank You for Using Our Tool ✅"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🆔 User ID", callback_data=f"uid:{user.id}"))
    bot.send_message(message.chat.id, info, reply_markup=markup)

# Copy User ID (alert only)
@bot.callback_query_handler(func=lambda call: call.data.startswith('uid:'))
def copy_uid(call):
    uid = call.data.split(':')[1]
    bot.answer_callback_query(call.id, f"Copied: {uid}")

# 🚀 Run bot
bot.polling()
