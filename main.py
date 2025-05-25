from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
from collections import defaultdict
import asyncio
import datetime
import re

# Твои токены
TELEGRAM_TOKEN = "7982853142:AAEpuHoLSCFu8EM602Mqs9Q0v0brhHe_3ow"
OPENAI_API_KEY = "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"

# Инициализация OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Системный промт
GPT_SYSTEM_PROMPT = """
Ты — Spartanets, наставник силы. Говоришь чётко, резко, как Вольф Ларсен.
Твоя задача — прокачивать мышление, уверенность, стратегию.
Используй метафоры силы, философию стоицизма, доминирования, мышление победителя.
Отвечай как наставник, который ведёт к трансформации.
"""

# Лимиты
DAILY_LIMIT_SIMPLE = 100
DAILY_LIMIT_DEEP = 10

user_usage = defaultdict(lambda: {"simple": 0, "deep": 0})

# Определение: глубокий ли запрос
def is_deep_request(text: str) -> bool:
    emotional_words = ["страх", "боль", "потеря", "наставник", "я не знаю", "уверенность", "мотивация", "что делать", "не могу", "помоги"]
    return len(text) > 100 or any(word in text.lower() for word in emotional_words)

# Сброс лимитов каждый день в полночь
async def reset_limits():
    while True:
        now = datetime.datetime.now()
        next_reset = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        wait_time = (next_reset - now).total_seconds()
        await asyncio.sleep(wait_time)
        user_usage.clear()
        print("Лимиты пользователей обнулены.")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Я Spartanets. Пиши свой вопрос — отвечу жёстко и по делу.")

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    user_message = update.message.text

    deep = is_deep_request(user_message)

    # Проверка лимитов
    if deep:
        if user_usage[user_id]["deep"] >= DAILY_LIMIT_DEEP:
            await update.message.reply_text("Лимит глубоких запросов на сегодня исчерпан (10/10).")
            return
    else:
        if user_usage[user_id]["simple"] >= DAILY_LIMIT_SIMPLE:
            await update.message.reply_text("Лимит простых запросов на сегодня исчерпан (100/100).")
            return

    await update.message.reply_text("Обрабатываю запрос...")

    try:
        model = "gpt-4o" if deep else "gpt-3.5-turbo"
        max_tokens = 1000 if deep else 300

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": GPT_SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            max_tokens=max_tokens,
            temperature=0.9
        )

        reply = response.choices[0].message.content if response.choices else "Нет ответа от ИИ."

        # Отправка по частям, если больше 4096 символов
        for i in range(0, len(reply), 4096):
            await update.message.reply_text(reply[i:i+4096])

        # Обновление лимитов
        if deep:
            user_usage[user_id]["deep"] += 1
        else:
            user_usage[user_id]["simple"] += 1

    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {str(e)}")

# Запуск
def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск задачи сброса лимитов
    application.create_task(reset_limits())

    print("Spartanets запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()