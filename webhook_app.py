# webhook_app.py
import os
from fastapi import FastAPI, Request, HTTPException
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler

TOKEN = os.getenv("TG_BOT_TOKEN")
SECRET = os.getenv("WEBHOOK_SECRET", "")

if not TOKEN:
    raise SystemExit("Set TG_BOT_TOKEN environment variable")

bot = Bot(token=TOKEN)
app = FastAPI()
dp = Dispatcher(bot, None, workers=0)  # sync processing

def start(update, context):
    update.message.reply_text("Привет! Я работаю через webhook ✅")

dp.add_handler(CommandHandler("start", start))

@app.post("/webhook")
async def webhook(request: Request):
    # проверка секретного заголовка (если задан)
    if SECRET:
        header = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if header != SECRET:
            raise HTTPException(status_code=403, detail="Forbidden")

    data = await request.json()
    update = Update.de_json(data, bot)
    dp.process_update(update)
    return {"ok": True}
