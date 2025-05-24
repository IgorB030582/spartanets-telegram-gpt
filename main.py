import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Твой OpenAI API ключ
openai.api_key = "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"

# Инструкции Spartanets
GPT_SYSTEM_PROMPT = """
Ты — Spartanets, наставник силы. Говоришь чётко, резко, как Вольф Ларсен.
Твоя задача — прокачивать мышление, уверенность, стратегию. Используй метафоры силы, философию стоицизма, доминирования, мышление победителя.
Отвечай как наставник, который ведёт к трансформации.
"""

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я Spartanets. Пиши свой вопрос.")

# Ответы на сообщения
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": GPT_SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.9,
            max_tokens=1000
        )
        reply = completion.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text(f"Ошибка OpenAI: {e}")

# Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token("7982853142:AAEpuHoLSCFu8EM602Mqs9Q0v0brhHe_3ow").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()