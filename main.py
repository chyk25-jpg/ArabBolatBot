import os
import requests
from bs4 import BeautifulSoup

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

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

    if translations:
        return "\n".join(translations)
    else:
        return "❌ Перевод не найден"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Отправь арабское слово — я переведу 🤍")

def handle_text(update: Update, context: CallbackContext):
    word = update.message.text.strip()
    result = get_word_from_arabus(word)
    update.message.reply_text(result)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
