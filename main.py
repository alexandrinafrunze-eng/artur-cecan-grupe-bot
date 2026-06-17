from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import asyncio

TOKEN = os.getenv("BOT_TOKEN")

GRUPE = {
    "Botanica": [
        {"grupa": "501", "profesor": "Pădureț Andrei", "link": "https://t.me/+zT4NxH-zRyk5ODgy"},
        {"grupa": "502", "profesor": "Pădureț Andrei", "link": "https://t.me/+B9q7Zqp0BQo1ZjRi"},
        {"grupa": "503", "profesor": "Murahovschi Pavel", "link": "https://t.me/+uQCLVLUFV1plYTVi"},
    ],
    "Ciocana": [
        {"grupa": "42", "profesor": "Uscatu Ion-Mihail", "link": "https://t.me/+fY7Ye5Og-VxkZDQy"},
        {"grupa": "43", "profesor": "Uscatu Ion-Mihail", "link": "https://t.me/+KMn8eWvVsFBkNzZi"},
        {"grupa": "44", "profesor": "Cecan Artur", "link": "https://t.me/+--athpFpXr9kMTBi"},
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
        "Selectează sediul unde ești înscris:",
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
                    f"📚 Grupa {item['grupa']} | 👨‍🏫 Prof. {item['profesor']}",
                    callback_data=f"grupa_{sediu}|{index}"
                )
            ])

        keyboard.append([InlineKeyboardButton("⬅️ Înapoi", callback_data="inapoi")])

        await query.edit_message_text(
            f"<b>📍 Sediul {sediu}</b>\n\n"
            "<b>Grupe disponibile:</b>\n\n"
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
            f"📍 <b>Sediul:</b> {sediu}\n"
            f"📚 <b>Grupa:</b> {item['grupa']}\n"
            f"👨‍🏫 <b>Profesor:</b> {item['profesor']}\n\n"
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
            "Selectează sediul unde ești înscris:",
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
