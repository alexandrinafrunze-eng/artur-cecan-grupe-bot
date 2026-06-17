from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import asyncio

TOKEN = os.getenv("BOT_TOKEN")

GRUPE = {
    "Botanica": {
        "Grupa 501 - Pădureț Andrei": "https://t.me/+xr11I1hqhegwOGZi",
        "Grupa 502 - Pădureț Andrei": "https://t.me/+ZnpPMLiz31ZlNWNi",
        "Grupa 503 - Murahovschi Pavel": "https://t.me/+FIVltLewmUQxMWYy"
    },
    "Ciocana": {
        "Grupa 42 - Uscatu Ion-Mihail": "https://t.me/+eqOPYvLSVntlMWJi",
        "Grupa 43 - Uscatu Ion-Mihail": "https://t.me/+pWJUYFn7kesyMzli",
        "Grupa 44 - Cecan Artur": "https://t.me/+9xcdpLU0AVM1MmJi"
    }
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📍 Botanica", callback_data="sediu_Botanica")],
        [InlineKeyboardButton("📍 Ciocana", callback_data="sediu_Ciocana")]
    ]

    await update.message.reply_text(
        "🚗 Bun venit la Școala Auto Artur Cecan!\n\n"
        "Te rugăm să selectezi sediul unde ești înscris:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("sediu_"):
        sediu = data.replace("sediu_", "")

        keyboard = [
            [InlineKeyboardButton(grupa, callback_data=f"grupa_{sediu}|{grupa}")]
            for grupa in GRUPE[sediu]
        ]

        keyboard.append([InlineKeyboardButton("⬅️ Înapoi", callback_data="inapoi")])

        await query.edit_message_text(
            f"📚 Grupe disponibile la sediul {sediu}:\n\n"
            "Alege grupa în care ești înscris:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("grupa_"):
        info = data.replace("grupa_", "")
        sediu, grupa = info.split("|")

        link = GRUPE[sediu][grupa]

        keyboard = [
            [InlineKeyboardButton("🔗 Intră în grup", url=link)],
            [InlineKeyboardButton("⬅️ Înapoi la grupe", callback_data=f"sediu_{sediu}")]
        ]

        await query.edit_message_text(
            f"🚗 Școala Auto Artur Cecan\n\n"
            f"✅ Ai ales:\n"
            f"📍 Sediul: {sediu}\n"
            f"📚 {grupa}\n\n"
            f"Apasă butonul de mai jos pentru a intra în grupul tău Telegram.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "inapoi":
        keyboard = [
            [InlineKeyboardButton("📍 Botanica", callback_data="sediu_Botanica")],
            [InlineKeyboardButton("📍 Ciocana", callback_data="sediu_Ciocana")]
        ]

        await query.edit_message_text(
            "🚗 Bun venit la Școala Auto Artur Cecan!\n\n"
            "Te rugăm să selectezi sediul unde ești înscris:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
