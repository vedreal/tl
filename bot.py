import os
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Ambil token dari environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
MINIAPP_URL = os.getenv('MINIAPP_URL', 'https://your-miniapp-url.com')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk command /start"""
    
    # Buat keyboard dengan tombol Web App
    keyboard = [
        [InlineKeyboardButton(
            text="🎮 START", 
            web_app=WebAppInfo(url=MINIAPP_URL)
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Kirim pesan dengan tombol
    welcome_text = "🎯 you're among the top DPS farmers — don't lose it!\n\nPress button below to start"
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup
    )

def main():
    """Fungsi utama untuk menjalankan bot"""
    
    # Cek apakah token sudah diset
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        print("❌ Error: BOT_TOKEN belum diset!")
        return
    
    # Buat aplikasi bot
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Tambahkan handler
    application.add_handler(CommandHandler("start", start))
    
    # Jalankan bot
    print("✅ Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
```

---
