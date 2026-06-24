import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = 8642204656:AAEZfAF5EYWOHcs-gv1HzzQjRAI6m_DW6js
MY_ID = 728141177
MY_NAMES = ["\u0440\u0443\u0441\u043b\u0430\u043d", "@ruslanomr"]

logging.basicConfig(level=logging.INFO)

async def check_mention(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return
    if message.chat.type == "private":
        return

    text_lower = message.text.lower()
    mentioned = any(name in text_lower for name in MY_NAMES)
    reply_to_me = (
        message.reply_to_message and
        message.reply_to_message.from_user and
        message.reply_to_message.from_user.id == MY_ID
    )

    if mentioned or reply_to_me:
        chat = message.chat
        sender = message.from_user.full_name if message.from_user else "Unknown"
        group_name = chat.title or "Group"

        if chat.username:
            link = f"https://t.me/{chat.username}/{message.message_id}"
        else:
            chat_id_str = str(chat.id).replace("-100", "")
            link = f"https://t.me/c/{chat_id_str}/{message.message_id}"

        notification = (
            f"--- \u0417\u0410\u0414\u0410\u0427\u0410 \u0414\u041b\u042f \u0420\u0423\u0421\u041b\u0410\u041d\u0410 ---\n\n"
            f"\u041e\u0442: {sender}\n"
            f"\u0413\u0440\u0443\u043f\u043f\u0430: {group_name}\n\n"
            f"\u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435:\n{message.text}"
        )

        keyboard = [[InlineKeyboardButton("\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435", url=link)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_message(
            chat_id=MY_ID,
            text=notification,
            reply_markup=reply_markup
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_mention))
    print("Bot started...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
