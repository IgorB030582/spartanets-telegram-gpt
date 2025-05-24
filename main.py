from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# Прямо в коде (не через .env) — ТВОИ ТОКЕНЫ
TELEGRAM_TOKEN = "7982853142:AAEpuHoLSCFu8EM602Mqs9Q0v0brhHe_3ow"
OPENAI_API_KEY = "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"

# Инициализация OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# System prompt в стиле Spartanets
GPT_SYSTEM_PROMPT = """
Ты — Spartanets, наставник силы. Говоришь чётко, резко, как Вольф Ларсен.
Твоя задача — прокачивать мышление, уверенность, стратегию. 
Используй метафоры силы, философию стоицизма, доминирования, мышление победителя.
Отвечай как наставник, который ведёт к трансформации.
"""

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Я Spartanets. Пиши свой вопрос — отвечу жёстко и по делу.")

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    await update.message.reply_text("Обрабатываю запрос...")

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": GPT_SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            max_tokens=1000,
            temperature=0.9
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {str(e)}")

# Запуск
def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Spartanets запущен...")
    application.run_polling()

if name == "__main__":
    main()