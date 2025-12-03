import os
from dotenv import load_dotenv
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Load file .env
load_dotenv()

# Ambil variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
MINIAPP_URL = os.getenv('MINIAPP_URL')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Debug: cek URL yang kebaca
    print(f"DEBUG - URL yang dipakai: {MINIAPP_URL}")
    
    if not MINIAPP_URL or MINIAPP_URL == "https://your-miniapp-url.com":
        await update.message.reply_text("❌ MINIAPP_URL belum diset di file .env!")
        return
    
    # Buat tombol
    keyboard = [[
        InlineKeyboardButton(
            text="🎮 START", 
            web_app=WebAppInfo(url=MINIAPP_URL)
        )
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎯 Press button below to start",
        reply_markup=reply_markup
    )

def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN belum diset!")
        return
    
    print(f"✅ Bot token: {BOT_TOKEN[:10]}...")
    print(f"✅ Miniapp URL: {MINIAPP_URL}")
    
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    print("✅ Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
