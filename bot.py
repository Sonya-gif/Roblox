
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
REF_LINK = "https://rblx.earth/?referredBy=4139558889"

# Простая in-memory статистика
user_stats = {
    "ref_clicks": 0,
    "total_users": set()
}

LANGS = {
    "ru": {
        "start": "Привет! Хочешь бесплатные робуксы? Жми на кнопки ниже!",
        "how": "1. Жми «Заработать Robux»\n2. Введи ник Roblox\n3. Выполняй задания\n4. Получай Robux!",
        "codes": "Промокоды (апрель 2025):\n- DAVI2023\n- NOOB\n- Subtodavibloxian\n- Sub2jckunrb",
        "menu": [
            ["Заработать Robux", "how", "codes"],
            ["Выбрать язык", "faq", "admin"]
        ]
    },
    "en": {
        "start": "Hey! Want free Robux? Tap a button below!",
        "how": "1. Tap 'Earn Robux'\n2. Enter your username\n3. Complete offers\n4. Get Robux!",
        "codes": "Promo codes (April 2025):\n- DAVI2023\n- NOOB\n- Subtodavibloxian\n- Sub2jckunrb",
        "menu": [
            ["Earn Robux", "how", "codes"],
            ["Choose Language", "faq", "admin"]
        ]
    }
}

user_lang = {}

def get_lang(user_id):
    return user_lang.get(user_id, "ru")

def build_menu(lang):
    data = LANGS[lang]["menu"]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text, url=REF_LINK) if text.lower().startswith("зараб") or text.lower().startswith("earn") else
         InlineKeyboardButton(text, callback_data=text.lower().replace(" ", "_")) for text in row]
        for row in data
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_lang[user.id] = "ru"
    user_stats["total_users"].add(user.id)
    await context.bot.send_message(chat_id=your_admin_id, text=f"{user.first_name} запустил бота (@{user.username})")
    await update.message.reply_text(LANGS["ru"]["start"], reply_markup=build_menu("ru"))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    lang = get_lang(user_id)
    await query.answer()

    if query.data == "how":
        await query.edit_message_text(LANGS[lang]["how"])
    elif query.data == "codes":
        await query.edit_message_text(LANGS[lang]["codes"])
    elif query.data == "choose_language":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Русский", callback_data="lang_ru"),
             InlineKeyboardButton("English", callback_data="lang_en")]
        ])
        await query.edit_message_text("Выбери язык / Choose your language:", reply_markup=keyboard)
    elif query.data.startswith("lang_"):
        new_lang = query.data.split("_")[1]
        user_lang[user_id] = new_lang
        await query.edit_message_text(LANGS[new_lang]["start"], reply_markup=build_menu(new_lang))
    elif query.data == "faq":
        await query.edit_message_text("Ответы на частые вопросы скоро будут добавлены.")
    elif query.data == "admin":
        await query.edit_message_text("Напиши админу: @your_admin_username")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Всего пользователей: {len(user_stats['total_users'])}\nКликов по ссылке: {user_stats['ref_clicks']}"
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
