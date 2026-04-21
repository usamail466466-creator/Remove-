import os
import asyncio
import logging
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)

# রেন্ডারের জন্য ছোট একটি ওয়েব সার্ভার
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_web():
    # রেন্ডার সাধারণত ১০০০০ পোর্টে রান করে
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# টেলিগ্রাম বটের মূল কাজ
async def delete_service_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await asyncio.sleep(1) # ১ সেকেন্ড অপেক্ষা
        if update.message:
            await update.message.delete()
    except Exception as e:
        logging.error(f"Error: {e}")

async def main():
    # এনভায়রনমেন্ট ভেরিয়েবল থেকে টোকেন নেওয়া
    TOKEN = os.environ.get('BOT_TOKEN')
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    service_handler = MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS | filters.StatusUpdate.LEFT_CHAT_MEMBER, 
        delete_service_message
    )
    
    application.add_handler(service_handler)
    
    # বট স্টার্ট করা
    async with application:
        await application.initialize()
        await application.start_polling()
        await asyncio.Event().wait()

if __name__ == '__main__':
    # ওয়েব সার্ভার আলাদা থ্রেডে চালানো
    Thread(target=run_web).start()
    
    # বট রান করা
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
