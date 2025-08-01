import logging
telebot.logger.setLevel(logging.DEBUG)
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import time
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# Helper: animation style reply
def animated_reply(chat_id, text, delay=1.2):
    msg = bot.send_message(chat_id, f"<b>{text}</b>")
    time.sleep(delay)
    bot.delete_message(chat_id, msg.message_id)

# /start command
@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name or "User"
    name = f"<b>{name.upper()}</b>"
    animated_reply(message.chat.id, "Loading Welcome Message...", 1)
    welcome = (
        f"Hi {name}! Welcome to this bot\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "GADGET CC GENERATOR BOT is your ultimate toolkit on Telegram, packed with CC generators, educational resources, downloaders, temp mail, crypto utilities, and more. Simplify your tasks with cardin ease!\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "Don't forget to JoinNow for updates!"
    )
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Update", url="https://t.me/shuvogadgetbox"))
    markup.add(InlineKeyboardButton("Menu", callback_data="menu"))
    bot.send_message(message.chat.id, welcome, reply_markup=markup)

# /gen command
@bot.message_handler(commands=['gen'])
def gen_cc(message):
    animated_reply(message.chat.id, "⚙️ Generating Credit Cards...", 1.2)
    try:
        args = message.text.split(maxsplit=1)[1]
        parts = args.split('|')
        bin_code = parts[0]
        month = parts[1] if len(parts) > 1 else str(random.randint(1, 12)).zfill(2)
        year = parts[2] if len(parts) > 2 else str(random.randint(25, 30))
    except Exception:
        bot.reply_to(message, "❌ Format: /gen BIN or /gen BIN|MM|YY")
        return

    cc_list = []
    for _ in range(10):
        cc = bin_code + ''.join([str(random.randint(0, 9)) for _ in range(16 - len(bin_code))])
        cvc = str(random.randint(100, 999))
        cc_list.append(f"<code>{cc}|{month}|{year}|{cvc}</code>")

    reply = (
        "━━━━━━━━━━━━━━━━\n" +
        "\n".join(cc_list)
    )
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Re-generate", callback_data=f"regen:{args}"))
    markup.add(InlineKeyboardButton("Menu", callback_data="menu"))
    bot.send_message(message.chat.id, reply, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('regen:'))
def re_generate(call):
    bin_input = call.data.split(':', 1)[1]
    fake_message = type('msg', (), {
        'chat': call.message.chat,
        'text': f"/gen {bin_input}",
        'from_user': call.from_user
    })
    gen_cc(fake_message)

# /fake command
@bot.message_handler(commands=['fake'])
def fake_address(message):
    animated_reply(message.chat.id, "🏠 Generating Fake Address...", 1.2)
    postal = str(random.randint(10000, 99999))
    address = (
        "━━━━━━━━━━━━━━━━\n"
        "Street: 123 Raven Lane\n"
        "City: Gotham\n"
        "Country: USA\n"
        f"Postal Code: <code>{postal}</code>"
    )
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Copy Postal Code", callback_data=f"copy:{postal}"))
    markup.add(InlineKeyboardButton("Menu", callback_data="menu"))
    bot.send_message(message.chat.id, address, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('copy:'))
def copy_postal(call):
    postal = call.data.split(':', 1)[1]
    bot.answer_callback_query(call.id, f"Copied: {postal}")

# /info command
@bot.message_handler(commands=['info'])
def user_info(message):
    animated_reply(message.chat.id, "🔍 Processing User Info...", 1.2)
    user = message.from_user
    info = (
        "🔍 Showing User's Profile Info 📋\n"
        "━━━━━━━━━━━━━━━━\n"
        f"• Full Name: <b>{user.first_name.upper()}</b>\n"
        f"• Username: @{user.username}\n"
        f"• User ID: <code>{user.id}</code>\n"
        f"• Chat ID: <code>{message.chat.id}</code>\n"
        "• Premium User: Yes\n"
        "• Data Center: SIN, Singapore, SG\n"
        "• Created On: June 22, 2023\n"
        "• Account Age: 2 years, 1 months, 9 days\n"
        "━━━━━━━━━━━━━━━━\n"
        "👁 Thank You for Using Our Tool ✅"
    )
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("User ID", callback_data=f"uid:{user.id}"))
    markup.add(InlineKeyboardButton("Menu", callback_data="menu"))
    bot.send_message(message.chat.id, info, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('uid:'))
def copy_uid(call):
    uid = call.data.split(':', 1)[1]
    bot.answer_callback_query(call.id, f"Copied: {uid}")

# Menu button handler
@bot.callback_query_handler(func=lambda call: call.data == "menu")
def menu_handler(call):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("💳 Gen", callback_data="menu_gen"),
        InlineKeyboardButton("🏠 Fake", callback_data="menu_fake"),
        InlineKeyboardButton("👤 Info", callback_data="menu_info")
    )
    bot.send_message(call.message.chat.id, "📜 <b>Choose a command:</b>", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('menu_'))
def menu_command_handler(call):
    if call.data == "menu_gen":
        bot.send_message(call.message.chat.id, "Type <code>/gen BIN</code> or <code>/gen BIN|MM|YY</code>")
    elif call.data == "menu_fake":
        bot.send_message(call.message.chat.id, "Type <code>/fake</code> to get a fake address.")
    elif call.data == "menu_info":
        bot.send_message(call.message.chat.id, "Type <code>/info</code> to get your profile info.")

# Run bot
if __name__ == "__main__":
    print("🤖 GADGET CC GENERATOR BOT is running...")
    if __name__ == "__main__":
    safe_polling()
