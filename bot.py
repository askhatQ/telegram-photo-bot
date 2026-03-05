import os
import logging
import base64
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токены из переменных окружения
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

if not TELEGRAM_TOKEN:
    raise ValueError("Нет TELEGRAM_TOKEN в переменных окружения!")
if not ANTHROPIC_API_KEY:
    raise ValueError("Нет ANTHROPIC_API_KEY в переменных окружения!")


def analyze_image_with_claude(image_bytes: bytes) -> str:
    """Отправляет фото в Claude Vision и возвращает описание."""
    image_base64 = base64.standard_b64encode(image_bytes).decode("utf-8")

    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": "claude-opus-4-5",
            "max_tokens": 1024,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_base64,
                            },
                        },
                        {
                            "type": "text",
                            "text": (
                                "Подробно опиши это изображение на русском языке. "
                                "Расскажи что на нём изображено, какие объекты, люди, "
                                "место действия, настроение и любые другие интересные детали."
                            ),
                        },
                    ],
                }
            ],
        },
        timeout=30,
    )

    if response.status_code != 200:
        logger.error(f"Ошибка API Claude: {response.status_code} — {response.text}")
        return "❌ Ошибка при анализе изображения. Попробуйте ещё раз."

    data = response.json()
    return data["content"][0]["text"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start."""
    await update.message.reply_text(
        "👋 Привет! Я бот для анализа фотографий.\n\n"
        "📸 Просто отправь мне любое фото — и я подробно опишу, что на нём изображено.\n\n"
        "Попробуй прямо сейчас!"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help."""
    await update.message.reply_text(
        "ℹ️ *Как пользоваться ботом:*\n\n"
        "1. Отправь фото прямо в чат\n"
        "2. Подожди несколько секунд\n"
        "3. Получи подробное описание!\n\n"
        "Бот анализирует: людей, объекты, места, текст на фото, настроение и многое другое.",
        parse_mode="Markdown"
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает входящие фото."""
    await update.message.reply_text("🔍 Анализирую фото, подождите секунду...")

    try:
        # Берём фото наилучшего качества (последнее в списке)
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)

        # Скачиваем фото
        photo_bytes = await file.download_as_bytearray()

        # Анализируем через Claude
        description = analyze_image_with_claude(bytes(photo_bytes))

        await update.message.reply_text(f"🖼 *Описание фото:*\n\n{description}", parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Ошибка обработки фото: {e}")
        await update.message.reply_text(
            "😔 Произошла ошибка при обработке фото. Пожалуйста, попробуйте ещё раз."
        )


async def handle_document_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает фото, отправленные как документ (без сжатия)."""
    document = update.message.document

    if not document.mime_type or not document.mime_type.startswith("image/"):
        await update.message.reply_text(
            "📎 Я умею анализировать только изображения. Отправьте фото или картинку."
        )
        return

    await update.message.reply_text("🔍 Анализирую изображение, подождите...")

    try:
        file = await context.bot.get_file(document.file_id)
        image_bytes = await file.download_as_bytearray()

        description = analyze_image_with_claude(bytes(image_bytes))

        await update.message.reply_text(f"🖼 *Описание изображения:*\n\n{description}", parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Ошибка обработки документа: {e}")
        await update.message.reply_text(
            "😔 Произошла ошибка. Пожалуйста, попробуйте ещё раз."
        )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отвечает на текстовые сообщения."""
    await update.message.reply_text(
        "📸 Отправь мне фото, и я его опишу!\n\n"
        "Используй /help для подробной инструкции."
    )


def main() -> None:
    """Запуск бота."""
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Регистрируем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.Document.IMAGE, handle_document_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("Бот запущен!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
