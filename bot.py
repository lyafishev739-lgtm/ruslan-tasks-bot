import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# === НАСТРОЙКИ ===
BOT_TOKEN = "8642204656:AAG7bC8iFrxIMb1d8p4XMfwZJBoycEai4NE"
MY_ID = 728141177
MY_NAMES = ["руслан", "ruslan", "@ruslanomr"]  # добавь свои варианты

logging.basicConfig(level=logging.INFO)

async def check_mention(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    # Игнорируем личные сообщения
    if message.chat.type == "private":
        return

    text_lower = message.text.lower()
    
    # Проверяем упоминание
    mentioned = any(name in text_lower for name in MY_NAMES)
    
    # Проверяем прямой reply на моё сообщение
    reply_to_me = (
        message.reply_to_message and 
        message.reply_to_message.from_user and
        message.reply_to_message.from_user.id == MY_ID
    )

    if mentioned or reply_to_me:
        chat = message.chat
        sender = message.from_user.full_name if message.from_user else "Неизвестно"
        group_name = chat.title or "Группа"
        
        # Ссылка на сообщение
        if chat.username:
            link = f"https://t.me/{chat.username}/{message.message_id}"
        else:
            chat_id_str = str(chat.id).replace("-100", "")
            link = f"https://t.me/c/{chat_id_str}/{message.message_id}"

        notification = (
            f"📌 *Задача для тебя*\n\n"
            f"👤 От: {sender}\n"
            f"💬 Группа: {group_name}\n\n"
            f"📝 *Текст:*\n{message.text}\n\n"
            f"🔗 [Открыть сообщение]({link})"
        )

        await context.bot.send_message(
            chat_id=MY_ID,
            text=notification,
            parse_mode="Markdown"
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_mention))
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
