import os, random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import import os, random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# ✨ Animation-style reply
async def animated_reply(update, text):
    await update.message.chat.send_action("typing")
    await update.message.reply_text(text)

# ✅ /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🆕 Update", url="https://t.me/shuvogadgetbox")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await animated_reply(update, "👋 Welcome to GADGET CC GENERATOR BOT!")
    await update.message.reply_text(
        "🔮 Generate CC from BIN\n📍 Get Fake Address\nℹ️ View Your Info",
        reply_markup=reply_markup
    )

# ✅ /gen
async def gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await animated_reply(update, "❌ Please provide a BIN.")
        return

    bin_input = args[0]
    parts = bin_input.split("|")
    bin_code = parts[0]
    mm = parts[1] if len(parts) > 1 else None
    yy = parts[2] if len(parts) > 2 else None

    cc_list = []
    for _ in range(10):
        exp_mm = mm if mm else f"{random.randint(1,12):02d}"
        exp_yy = yy if yy else f"{random.randint(25,30)}"
        cvv = random.randint(100, 999)
        cc = f"{bin_code}xxxxxx | {exp_mm} | {exp_yy} | {cvv}"
        cc_list.append(cc)

    cc_text = "\n".join(cc_list)
    keyboard = [[InlineKeyboardButton("🔁 Re-generate", callback_data=f"regen:{bin_input}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await animated_reply(update, "🔄 Generating Credit Cards...")
    await update.message.reply_text(f"💳 BIN: {bin_code}\n━━━━━━━━━━━━━━\n{cc_text}\n━━━━━━━━━━━━━━", reply_markup=reply_markup)

# ✅ /fake
async def fake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    country = context.args[0] if context.args else "Bangladesh"
    postal_code = "1219" if country.lower() == "bangladesh" else "10001"
    keyboard = [[InlineKeyboardButton("📋 Copy Postal Code", callback_data=f"copy:{postal_code}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await animated_reply(update, "🏗 Generating Fake Address...")
    await update.message.reply_text(
        f"📍 Address for {country}\n━━━━━━━━━━━━━━\n• Street: ২৩ খিলগাঁও চৌরাস্তা\n• City: ঢাকা\n• Postal Code: {postal_code}\n━━━━━━━━━━━━━━",
        reply_markup=reply_markup
    )

# ✅ /info
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [[InlineKeyboardButton("🆔 User ID", callback_data=f"uid:{user.id}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await animated_reply(update, "🔍 Processing User Info...")
    await update.message.reply_text(
        f"🔍 Showing User's Profile Info 📋\n━━━━━━━━━━━━━━\n• Full Name: {user.full_name}\n• Username: @{user.username}\n• User ID: {user.id}\n• Chat ID: {user.id}\n• Premium User: {'Yes' if user.is_premium else 'No'}\n━━━━━━━━━━━━━━\n👁 Thank You for Using Our Tool ✅",
        reply_markup=reply_markup
    )

# ✅ Callback handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("regen:"):
        bin_input = data.split(":")[1]
        parts = bin_input.split("|")
        bin_code = parts[0]
        mm = parts[1] if len(parts) > 1 else None
        yy = parts[2] if len(parts) > 2 else None

        cc_list = []
        for _ in range(10):
            exp_mm = mm if mm else f"{random.randint(1,12):02d}"
            exp_yy = yy if yy else f"{random.randint(25,30)}"
            cvv = random.randint(100, 999)
            cc = f"{bin_code}xxxxxx | {exp_mm} | {exp_yy} | {cvv}"
            cc_list.append(cc)

        cc_text = "\n".join(cc_list)
        await query.edit_message_text(f"💳 BIN: {bin_code}\n━━━━━━━━━━━━━━\n{cc_text}\n━━━━━━━━━━━━━━")

    elif data.startswith("copy:"):
        postal = data.split(":")[1]
        await query.answer(f"📋 Postal Code copied: {postal}", show_alert=True)

    elif data.startswith("uid:"):
        uid = data.split(":")[1]
        await query.answer(f"🆔 User ID copied: {uid}", show_alert=True)

# ✅ Bot setup
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gen", gen))
app.add_handler(CommandHandler("fake", fake))
app.add_handler(CommandHandler("info", info))
app.add_handler(CallbackQueryHandler(button_handler))

print("🤖 GADGET CC GENERATOR BOT is running...")
app.run_polling(), CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("7754449564:AAE7_8SphGIBbGNCuR-W9X6GEZSdUewnUZQ")
ADMIN_ID = int(os.getenv("6074463370"))

# ✨ Animation-style reply
async def animated_reply(update, text):
    await update.message.chat.send_action("typing")
    await update.message.reply_text(text)

# ✅ /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🆕 Update", url="https://t.me/shuvogadgetbox")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await animated_reply(update, "👋 Welcome to GADGET CC GENERATOR BOT!")
    await update.message.reply_text(
        "🔮 Generate CC from BIN\n📍 Get Fake Address\nℹ️ View Your Info",
        reply_markup=reply_markup
    )

# ✅ /gen
async def gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await animated_reply(update, "❌ Please provide a BIN.")
        return

    bin_input = args[0]
    parts = bin_input.split("|")
    bin_code = parts[0]
    mm = parts[1] if len(parts) > 1 else None
    yy = parts[2] if len(parts) > 2 else None

    cc_list = []
    for _ in range(10):
        exp_mm = mm if mm else f"{random.randint(1,12):02d}"
        exp_yy = yy if yy else f"{random.randint(25,30)}"
        cvv = random.randint(100, 999)
        cc = f"{bin_code}xxxxxx | {exp_mm} | {exp_yy} | {cvv}"
        cc_list.append(cc)

    cc_text = "\n".join(cc_list)
    keyboard = [[InlineKeyboardButton("🔁 Re-generate", callback_data=f"regen:{bin_input}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await animated_reply(update, "🔄 Generating Credit Cards...")
    await update.message.reply_text(f"💳 BIN: {bin_code}\n━━━━━━━━━━━━━━\n{cc_text}\n━━━━━━━━━━━━━━", reply_markup=reply_markup)

# ✅ /fake
async def fake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    country = context.args[0] if context.args else "Bangladesh"
import os, random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# ✨ Animation-style reply
async def animated_reply(update, text):
    await update.message.chat.send_action("typing")
    await update.message.reply_text(text)

# ✅ /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🆕 Update", url="https://t.me/shuvogadgetbox")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await animated_reply(update, "👋 Welcome to GADGET CC GENERATOR BOT!")
    await update.message.reply_text(
        "🔮 Generate CC from BIN\n📍 Get Fake Address\nℹ️ View Your Info",
        reply_markup=reply_markup
    )

# ✅ /gen
async def gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await animated_reply(update, "❌ Please provide a BIN.")
        return

    bin_input = args[0]
    parts = bin_input.split("|")
    bin_code = parts[0]
    mm = parts[1] if len(parts) > 1 else None
    yy = parts[2] if len(parts) > 2 else None

    cc_list = []
    for _ in range(10):
        exp_mm = mm if mm else f"{random.randint(1,12):02d}"
        exp_yy = yy if yy else f"{random.randint(25,30)}"
        cvv = random.randint(100, 999)
        cc = f"{bin_code}xxxxxx | {exp_mm} | {exp_yy} | {cvv}"
        cc_list.append(cc)

    cc_text = "\n".join(cc_list)
    keyboard = [[InlineKeyboardButton("🔁 Re-generate", callback_data=f"regen:{bin_input}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await animated_reply(update, "🔄 Generating Credit Cards...")
import os, random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# ✨ Animation-style reply
async def animated_reply(update, text):
    await update.message.chat.send_action("typing")
    await update.message.reply_text(text)

# ✅ /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🆕 Update", url="https://t.me/shuvogadgetbox")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await animated_reply(update, "👋 Welcome to GADGET CC GENERATOR BOT!")
    await update.message.reply_text(
        "🔮 Generate CC from BIN\n📍 Get Fake Address\nℹ️ View Your Info",
        reply_markup=reply_markup
    )

# ✅ /gen
async def gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await animated_reply(update, "❌ Please provide a BIN.")
        return

    bin_input = args[0]
    parts = bin_input.split("|")
    bin_code = parts[0]
    mm = parts[1] if len(parts) > 1 else None
    yy = parts[2] if len(parts) > 2 else None

    cc_list = []
    for _ in range(10):
        exp_mm = mm if mm else f"{random.randint(1,12):02d}"
        exp_yy = yy if yy else f"{random.randint(25,30)}"
        cvv = random.randint(100, 999)
        cc = f"{bin_code}xxxxxx | {exp_mm} | {exp_yy} | {cvv}"
        cc_list.append(cc)

    cc_text = "\n".join(cc_list)
    keyboard = [[InlineKeyboardButton("🔁 Re-generate", callback_data=f"regen:{bin_input}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await animated_reply(update, "🔄 Generating Credit Cards...")
    await update.message.reply_text(f"💳 BIN: {bin_code}\n━━━━━━━━━━━━━━\n{cc_text}\n━━━━━━━━━━━━━━", reply_markup=reply_markup)

# ✅ /fake
async def fake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    country = context.args[0] if context.args else "Bangladesh"
    postal_code = "1219" if country.lower() == "bangladesh" else "10001"
    keyboard = [[InlineKeyboardButton("📋 Copy Postal Code", callback_data=f"copy:{postal_code}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await animated_reply(update, "🏗 Generating Fake Address...")
    await update.message.reply_text(
        f"📍 Address for {country}\n━━━━━━━━━━━━━━\n• Street: ২৩ খিলগাঁও চৌরাস্তা\n• City: ঢাকা\n• Postal Code: {postal_code}\n━━━━━━━━━━━━━━",
        reply_markup=reply_markup
    )

# ✅ /info
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [[InlineKeyboardButton("🆔 User ID", callback_data=f"uid:{user.id}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await animated_reply(update, "🔍 Processing User Info...")
    await update.message.reply_text(
        f"🔍 Showing User's Profile Info 📋\n━━━━━━━━━━━━━━\n• Full Name: {user.full_name}\n• Username: @{user.username}\n• User ID: {user.id}\n• Chat ID: {user.id}\n• Premium User: {'Yes' if user.is_premium else 'No'}\n━━━━━━━━━━━━━━\n👁 Thank You for Using Our Tool ✅",
        reply_markup=reply_markup
    )

# ✅ Callback handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

