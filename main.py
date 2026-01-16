import os
import requests
from bs4 import BeautifulSoup
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

def get_word_from_arabus(word):
    url = f"https://arabus.ru/?q={word}"
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    translations = []
    for li in soup.select("li"):
        text = li.get_text(strip=True)
        if text:
            translations.append(text)
        if len(translations) >= 6:
            break
    return translations

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📖 Учить слова", "🧪 Тест"],
        ["🔁 Повторение", "📊 Прогресс"]
    ]
    await update.message.reply_text(
        "🕌 *ArabBolatBot*\n"
        "Учим арабские слова (Коран + классический арабский).\n\n"
        "Отправь арабское слово.",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode="Markdown"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word = update.message.text.strip()
    translations = get_word_from_arabus(word)

    if not translations:
        await update.message.reply_text("❌ Не нашёл слово. Попробуй другую форму.")
        return

    text = f"📘 *{word}*\n\n*Значения:*\n"
    for i, t in enumerate(translations, 1):
        text += f"{i}. {t}\n"

    await update.message.reply_text(text, parse_mode="Markdown")

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN not set")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
