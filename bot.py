import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8642204656:AAG7bC8iFrxIMb1d8p4XMfwZJBoycEai4NE"
MY_ID = 728141177
MY_NAMES = ["руслан", "@ruslanomr"]

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
            f"ZADACHA DLYA RUSLANA\n\n"
            f"Ot: {sender}\n"
            f"Gruppa: {group_name}\n\n"
            f"Soobshenie:\n{message.text}\n\n"
            f"Pereiti: {link}"
        )

        keyboard = [[InlineKeyboardButton("Открыть сообщение", url=link)]]
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
