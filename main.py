import os
import requests
from bs4 import BeautifulSoup

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")


def get_word_from_arabus(word: str):
    url = f"https://arabus.ru/?q={word}"
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    translations = []
    for li in soup.select("li"):
        text = li.get_text(strip=True)
        if text and word not in text:
            translations.append(text)
        if len(translations) >= 6:
            break

    return translations


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Отправь арабское слово — я покажу перевод 📘"
    )


async def handle_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    word = update.message.text.strip()
    translations = get_word_from_arabus(word)

    if not translations:
        await update.message.reply_text("Перевод не найден ❌")
        return

    reply = f"📖 {word}\n\n" + "\n".join(f"• {t}" for t in translations)
    await update.message.reply_text(reply)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_word))

    app.run_polling()


if __name__ == "__main__":
    main()
