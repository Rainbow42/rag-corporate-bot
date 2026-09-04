import asyncio
import logging
import os

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from rag_core import RAGService, create_service


logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    if update.message:
        await update.message.reply_text("Задайте вопрос по базе знаний QuantumForge.")


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return
    await update.message.chat.send_action(ChatAction.TYPING)
    service: RAGService = context.application.bot_data["service"]
    result = await asyncio.to_thread(service.ask, update.message.text)
    sources = ", ".join(result["sources"]) or "нет"
    message = f"{result['answer']}\n\nИсточники: {sources}"
    await update.message.reply_text(message[:4096])


def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is required")
    application = Application.builder().token(token).build()
    application.bot_data["service"] = create_service()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ask))
    application.run_polling()


if __name__ == "__main__":
    main()
