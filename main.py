import asyncio
import logging
import os
import random
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
import requests
import aiohttp
import io

# Список кот-каомодзи (расширенный, случайный выбор)
CAT_KAOMOJI = [
    "=^._.^= ∫", "(^=◕ᴥ◕=^)", "ฅ(＾・ω・＾ฅ)", "(=^･ω･^=)", "(=^･ｪ･^=)",
    "(ﾐΦ ﻌ Φﾐ)ﾉ", "/ᐠ｡ꞈ｡ᐟ\\", "චᆽච", "(ⓛ ω ⓛ *)", "(=｀ﻌ´=)",
    "ฅ^•ﻌ•^ฅ", "/ᐠ - ˕ -マ", "ᓚ₍ ^. .^ ₎", "(๑ↀᆺↀ๑)", "(Ф∀Ф)",
    "(=^‥^=)", "(^._.^)ﾉ", "(ﾐዎ ﻌ ዎﾐ)ﾉ", "/ᐠ.ᆽ.ᐟ \\", "♡(ﾐ ᵕ̣̣̣̣̣̣ ﻌ ᵕ̣̣̣̣̣̣ ﾐ)ﾉ"
]

# Токен бота от @BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def handle_message(update: Update, context):
    if update.message.from_user.is_bot:
        return  # Игнорируем ботов и себя
    
    text = update.message.text.lower().strip() if update.message.text else None
    
    if text == "мяу":
        # Получаем случайную картинку кота
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.thecatapi.com/v1/images/search?size=med&mime_types=jpg&format=json&order=RANDOM&limit=1") as resp:
                data = await resp.json()
                if data:
                    url = data[0]["url"]
                    await update.message.reply_photo(photo=url, caption="Мяу-мяу! 🐱")
    elif text:  # Любое другое текстовое сообщение
        kaomoji = random.choice(CAT_KAOMOJI)
        await update.message.reply_text(kaomoji)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
