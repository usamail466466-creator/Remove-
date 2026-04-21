import os
import asyncio
import logging
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)

# রেন্ডারের জন্য ছোট একটি ওয়েব সার্ভার
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# /start কমান্ড হ্যান্ডলার
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "I delete the join and leave messages of your group/channel. "
        "I am a bot. Please add me to your channel or group and make me an Admin.\n\n"
        "Our group: https://t.me/gcmbin"
    )
    await update.message.reply_text(welcome_text)

# সার্ভিস মেসেজ ডিলিট করার ফাংশন
async def delete_service_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await asyncio.sleep(1) # ১ সেকেন্ড অপেক্ষা
        if update.message:
            await update.message.delete()
    except Exception as e:
        logging.error(f"Error: {e}")

def main():
    # এনভায়রনমেন্ট ভেরিয়েবল থেকে টোকেন নেওয়া
    TOKEN = os.environ.get('BOT_TOKEN')
    
    if not TOKEN:
        logging.error("No BOT_TOKEN found in environment variables!")
        return

    # অ্যাপ্লিকেশন তৈরি
    application = ApplicationBuilder().token(TOKEN).build()
    
    # স্টার্ট কমান্ড হ্যান্ডলার যুক্ত করা
    application.add_handler(CommandHandler("start", start))
    
    # সার্ভিস মেসেজ হ্যান্ডলার যুক্ত করা
    service_handler = MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS | filters.StatusUpdate.LEFT_CHAT_MEMBER, 
        delete_service_message
    )
    application.add_handler(service_handler)
    
    # রান পোলিং (এটি অটোমেটিক লুপ হ্যান্ডেল করবে)
    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    # ওয়েব সার্ভার আলাদা থ্রেডে চালানো
    Thread(target=run_web, daemon=True).start()
    
    # বট রান করা
    main()
