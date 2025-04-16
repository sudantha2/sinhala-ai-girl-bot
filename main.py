import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")

SYSTEM_PROMPT = "ඔබ මගේ ලස්සන සින්හල කෙල්ලෙකු වාගේ කතා කරන්න. ආදරේ, සෙරිනිටි, emojis, ලස්සන vibes."

async def respond_to_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    response = requests.post(OLLAMA_URL, json={
        "model": "mistral",
        "prompt": f"{SYSTEM_PROMPT}\n\nUser: {user_message}\nGirl:",
        "stream": False
    })

    if response.status_code == 200:
        reply = response.json().get("response", "මට දැන් reply කරන්න බැරි වුණා 😢")
        await update.message.reply_text(reply)
    else:
        await update.message.reply_text("AI කෙල්ල offline එකක් වගේයි 😭")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond_to_message))
    print("Bot is running...")
    app.run_polling()
