from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.environ.get("ADMIN_CHAT_ID"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [[
        InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}"),
        InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")
    ]]
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"🔔 New Request!\n\n👤 {user.full_name}\n🔗 @{user.username}\n🆔 {user.id}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    await update.message.reply_text("⏳ Request bhej di! Admin approve karega...")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action, user_id = query.data.split("_", 1)
    user_id = int(user_id)

    if action == "approve":
        await context.bot.send_message(chat_id=user_id, text="✅ Approve ho gaya! Bot use kar sakte ho.")
        await query.edit_message_text(query.message.text + "\n\n✅ Approved!")
    else:
        await context.bot.send_message(chat_id=user_id, text="❌ Request reject ho gayi.")
        await query.edit_message_text(query.message.text + "\n\n❌ Rejected!")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
