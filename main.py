import os
import logging
import signal
import sys
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Токены
TELEGRAM_TOKEN = "7982853142:AAEpuHoLSCFu8EM602Mqs9Q0v0brhHe_3ow"
OPENAI_API_KEY = "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"

# Инициализация клиента OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне сообщение, и я отвечу на твой вопрос.")

# Ответ на текстовое сообщение
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    logger.info(f"Получено сообщение от {update.message.from_user.id}: {user_message}")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
            max_tokens=500
        )
        reply = response.choices[0].message.content
    except Exception as e:
        logger.error(f"Ошибка при обращении к OpenAI: {e}")
        reply = f"Извините, произошла ошибка: {e}"

    await update.message.reply_text(reply)

# Ответ на нетекстовое сообщение
async def handle_non_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пожалуйста, отправьте текстовое сообщение.")

# Запуск бота
if __name__ == "__main__":
    if not TELEGRAM_TOKEN or not OPENAI_API_KEY or not TELEGRAM_TOKEN.strip() or not OPENAI_API_KEY.strip():
        logger.error("TELEGRAM_TOKEN или OPENAI_API_KEY не заданы или пусты.")
        raise ValueError("Ошибка: TELEGRAM_TOKEN или OPENAI_API_KEY не заданы или пусты.")
    
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(~filters.TEXT, handle_non_text))

    # Завершение по Ctrl+C
    def signal_handler(sig, frame):
        logger.info("Остановка бота...")
        app.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    logger.info("Бот запущен!")
    app.run_polling()