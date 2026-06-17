from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import asyncio

TOKEN = os.getenv("BOT_TOKEN")

GRUPE = {
    "Botanica": [
        {
            "grupa": "501",
            "instructor": "Pădureț Andrei",
            "link": "https://t.me/+xr11I1hqhegwOGZi"
        },
        {
            "grupa": "502",
            "instructor": "Pădureț Andrei",
            "link": "https://t.me/+ZnpPMLiz31ZlNWNi"
        },
        {
            "grupa": "503",
            "instructor": "Murahovschi Pavel",
            "link": "https://t.me/+FIVltLewmUQxMWYy"
        }
    ],
    "Ciocana": [
        {
            "grupa": "42",
            "instructor": "Uscatu Ion-Mihail",
            "link": "https://t.me/+eqOPYvLSVntlMWJi"
        },
        {
            "grupa": "43",
            "instructor": "Uscatu Ion-Mihail",
            "link": "https://t.me/+pWJUYFn7kesyMzli"
        },
        {
            "grupa": "44",
            "instructor": "Cecan Artur",
            "link": "https://t.me/+9xcdpLU0AVM1MmJi"
        }
    ]
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

        keyboard = []

        for index, item in enumerate(GRUPE[sediu]):
            text_buton = f"📚 Grupa {item['grupa']} | 👨‍🏫 {item['instructor']}"
            keyboard.append([
                InlineKeyboardButton(
                    text_buton,
                    callback_data=f"grupa_{sediu}|{index}"
                )
            ])

        keyboard.append([InlineKeyboardButton("⬅️ Înapoi", callback_data="inapoi")])

        await query.edit_message_text(
            f"📚 Grupe disponibile la sediul {sediu}:\n\n"
            "Alege grupa în care ești înscris:",
            reply_markup=InlineKeyboardMarkup(keyboard)
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
            f"🚗 Școala Auto Artur Cecan\n\n"
            f"📍 Sediul: {sediu}\n"
            f"📚 Grupa: {item['grupa']}\n"
            f"👨‍🏫 Instructor: {item['instructor']}\n\n"
            f"Apasă butonul de mai jos pentru a intra în grupul Telegram.",
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
