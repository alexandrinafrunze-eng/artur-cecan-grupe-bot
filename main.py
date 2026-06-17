from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import asyncio

TOKEN = os.getenv("BOT_TOKEN")

GRUPE = {
    "Botanica": [
        {"grupa": "501", "instructor": "Pădureț Andrei", "link": "https://t.me/+xr11I1hqhegwOGZi"},
        {"grupa": "502", "instructor": "Pădureț Andrei", "link": "https://t.me/+ZnpPMLiz31ZlNWNi"},
        {"grupa": "503", "instructor": "Murahovschi Pavel", "link": "https://t.me/+FIVltLewmUQxMWYy"}
    ],
    "Ciocana": [
        {"grupa": "42", "instructor": "Uscatu Ion-Mihail", "link": "https://t.me/+eqOPYvLSVntlMWJi"},
        {"grupa": "43", "instructor": "Uscatu Ion-Mihail", "link": "https://t.me/+pWJUYFn7kesyMzli"},
        {"grupa": "44", "instructor": "Cecan Artur", "link": "https://t.me/+9xcdpLU0AVM1MmJi"}
    ]
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📍 Botanica", callback_data="sediu_Botanica")],
        [InlineKeyboardButton("📍 Ciocana", callback_data="sediu_Ciocana")]
    ]

    await update.message.reply_text(
        "<b>🚗 Școala Auto Artur Cecan</b>\n\n"
        "Bine ai venit!\n\n"
        "Pentru a primi acces în grupa potrivită,\n"
        "te rugăm să selectezi <b>sediul</b> unde ești înscris:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("sediu_"):
        sediu = data.replace("sediu_", "")

        keyboard = []
        for index, item in enumerate(GRUPE[sediu]):
            keyboard.append([
                InlineKeyboardButton(
                    f"📚 Grupa {item['grupa']} | 👨‍🏫 {item['instructor']}",
                    callback_data=f"grupa_{sediu}|{index}"
                )
            ])

        keyboard.append([InlineKeyboardButton("⬅️ Înapoi", callback_data="inapoi")])

        await query.edit_message_text(
            f"<b>📍 Sediul {sediu}</b>\n\n"
            f"<b>Grupe disponibile:</b>\n\n"
            "Alege grupa în care ești înscris:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )

    elif data.startswith("grupa_"):
        info = data.replace("grupa_", "")
        sediu, index = info.split("|")
        item = GRUPE[sediu][int(index)]

        keyboard = [
            [InlineKeyboardButton("🔗 Intră în grup", url=item["link"])],
            [InlineKeyboardButton("⬅️ Înapoi la grupe", callback_data=f"sediu_{sediu}")]
        ]

        await query.edit_message_text(
            "<b>🚗 Școala Auto Artur Cecan</b>\n\n"
            "<b>✅ Ai ales:</b>\n\n"
            f"📍 <b>Sediul:</b> {sediu}\n"
            f"📚 <b>Grupa:</b> {item['grupa']}\n"
            f"👨‍🏫 <b>Instructor:</b> {item['instructor']}\n\n"
            "Apasă pe butonul de mai jos pentru a intra în "
            "<b>grupul Telegram al grupei tale</b>.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )

    elif data == "inapoi":
        keyboard = [
            [InlineKeyboardButton("📍 Botanica", callback_data="sediu_Botanica")],
            [InlineKeyboardButton("📍 Ciocana", callback_data="sediu_Ciocana")]
        ]

        await query.edit_message_text(
            "<b>🚗 Școala Auto Artur Cecan</b>\n\n"
            "Te rugăm să selectezi <b>sediul</b> unde ești înscris:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
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


if __name__ == "__main__":
    asyncio.run(main())
