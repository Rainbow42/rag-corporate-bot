import asyncio
import logging
import os

from telegram import Message, Update
from telegram.constants import ChatAction
from telegram.error import NetworkError
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.request import HTTPXRequest

from rag_core import RAGService, create_service


logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def reply_with_retry(message: Message, text: str, attempts: int = 3) -> None:
    for attempt in range(attempts):
        try:
            await message.reply_text(text)
            return
        except NetworkError:
            if attempt == attempts - 1:
                raise
            await asyncio.sleep(2**attempt)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    if update.message:
        await reply_with_retry(update.message, "Задайте вопрос по базе знаний QuantumForge.")


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return
    try:
        await update.message.chat.send_action(ChatAction.TYPING)
    except NetworkError:
        logger.warning("Не удалось отправить индикатор набора текста")
    service: RAGService = context.application.bot_data["service"]
    result = await asyncio.to_thread(service.ask, update.message.text)
    sources = ", ".join(result["sources"]) or "нет"
    message = f"{result['answer']}\n\nИсточники: {sources}"
    await reply_with_retry(update.message, message[:4096])


async def log_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    del update
    logger.error("Ошибка при обработке Telegram-сообщения", exc_info=context.error)


def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is required")
    request = HTTPXRequest(connect_timeout=30, read_timeout=30, write_timeout=30, pool_timeout=10)
    updates_request = HTTPXRequest(connect_timeout=30, read_timeout=30, write_timeout=30, pool_timeout=10)
    application = (
        Application.builder()
        .token(token)
        .request(request)
        .get_updates_request(updates_request)
        .build()
    )
    application.bot_data["service"] = create_service()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ask))
    application.add_error_handler(log_error)
    application.run_polling(bootstrap_retries=5)


if __name__ == "__main__":
    main()
