import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import time
from dotenv import load_dotenv

# 🔄 Load .env variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

bot = telebot.TeleBot(BOT_TOKEN)

# 🎉 /start command
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

# 💳 /gen command
@bot.message_handler(commands=['gen'])
def gen_cc(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1.5)

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
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔁 Re-generate", callback_data=f"regen:{args}"))
    bot.send_message(message.chat.id, reply, reply_markup=markup)

# 🔁 Re-generate button
@bot.callback_query_handler(func=lambda call: call.data.startswith('regen:'))
def re_generate(call):
    bin_input = call.data.split(':')[1]
    fake_message = type('msg', (), {'chat': call.message.chat, 'text': f"/gen {bin_input}", 'from_user': call.from_user})
    gen_cc(fake_message)

# 🏠 /fake command
@bot.message_handler(commands=['fake'])
def fake_address(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1.5)
    postal = str(random.randint(10000, 99999))
    address = f"""🏠 Generate Fake Address...
━━━━━━━━━━━━━━━━
Street: 123 Raven Lane
City: Gotham
Country: USA
Postal Code: {postal}"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📋 Copy Postal Code", callback_data=f"copy:{postal}"))
    bot.send_message(message.chat.id, address, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('copy:'))
def copy_postal(call):
    postal = call.data.split(':')[1]
    bot.answer_callback_query(call.id, f"Copied: {postal}")

# 👤 /info command
@bot.message_handler(commands=['info'])
def user_info(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1.5)
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

@bot.callback_query_handler(func=lambda call: call.data.startswith('uid:'))
def copy_uid(call):
    uid = call.data.split(':')[1]
    bot.answer_callback_query(call.id, f"Copied: {uid}")

# 📜 menu command (inline)
@bot.message_handler(func=lambda m: m.text.lower() == "menu")
def show_menu(message):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("/gen", callback_data="menu_gen"),
        InlineKeyboardButton("/fake", callback_data="menu_fake"),
        InlineKeyboardButton("/info", callback_data="menu_info")
    )
    bot.send_message(message.chat.id, "📜 Choose a command:", reply_markup=markup)

# 🚀 Run bot
bot.polling()

