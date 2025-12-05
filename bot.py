import os
import json
from dotenv import load_dotenv
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Load .env file
load_dotenv()

# Get variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
MINIAPP_URL = os.getenv('MINIAPP_URL')
ADMIN_ID = os.getenv('ADMIN_ID')

# File to save user IDs
USERS_FILE = 'users.json'

def load_users():
    """Load user list from file"""
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_user(user_id):
    """Save new user ID"""
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f)
        print(f"✅ New user saved: {user_id}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Save user ID
    save_user(user_id)
    
    # Debug: check URL
    print(f"DEBUG - URL used: {MINIAPP_URL}")
    
    if not MINIAPP_URL or MINIAPP_URL == "https://your-miniapp-url.com":
        await update.message.reply_text("❌ MINIAPP_URL not set in .env file!")
        return
    
    # Create button
    keyboard = [[
        InlineKeyboardButton(
            text="COLLECT WOOT", 
            web_app=WebAppInfo(url=MINIAPP_URL)
        )
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Hi.. Welcome 👋🏻\nClaim WOOT by farming easily now\nAnd collect limited rewards for you! 🎉",
        reply_markup=reply_markup
    )

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command to broadcast message with button to all users (admin only)"""
    user_id = update.effective_user.id
    
    # Check if user is admin (ignore if not)
    if not ADMIN_ID or str(user_id) != ADMIN_ID:
        return
    
    # Check if there's a message to broadcast
    if not context.args:
        await update.message.reply_text(
            "📢 How to use:\n/broadcast <your message>\n\n"
            "Example:\n/broadcast 🎁 WOOT tokens ready to collect!"
        )
        return
    
    # Combine all arguments into one message
    message = ' '.join(context.args)
    
    # Load all users
    users = load_users()
    
    if not users:
        await update.message.reply_text("❌ No registered users yet!")
        return
    
    # Create button
    keyboard = [[
        InlineKeyboardButton(
            text="COLLECT WOOT", 
            web_app=WebAppInfo(url=MINIAPP_URL)
        )
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send to all users
    success = 0
    failed = 0
    
    await update.message.reply_text(f"📤 Sending broadcast to {len(users)} users...")
    
    for uid in users:
        try:
            await context.bot.send_message(
                chat_id=uid, 
                text=message,
                reply_markup=reply_markup
            )
            success += 1
        except Exception as e:
            print(f"❌ Failed sending to {uid}: {e}")
            failed += 1
    
    await update.message.reply_text(
        f"✅ Broadcast complete!\n\n"
        f"✅ Success: {success}\n"
        f"❌ Failed: {failed}"
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command to check number of users (admin only)"""
    user_id = update.effective_user.id
    
    # Check if user is admin (ignore if not)
    if not ADMIN_ID or str(user_id) != ADMIN_ID:
        return
    
    users = load_users()
    await update.message.reply_text(f"📊 Total users: {len(users)}")

def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not set!")
        return
    
    print(f"✅ Bot token: {BOT_TOKEN[:10]}...")
    print(f"✅ Miniapp URL: {MINIAPP_URL}")
    print(f"✅ Admin ID: {ADMIN_ID}")
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handler commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.add_handler(CommandHandler("stats", stats))
    
    print("✅ Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
