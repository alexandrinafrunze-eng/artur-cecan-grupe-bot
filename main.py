from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

GRUPE = {
    "Pavel": {
        "Pavel - 11 iunie": "https://t.me/link_pavel_11",
        "Pavel - 25 iunie": "https://t.me/link_pavel_25"
    },
    "Artur": {
        "Artur - 7 iulie": "https://t.me/link_artur_7"
    },
    "Andrei": {
        "Andrei - 18 iunie": "https://t.me/link_andrei_18"
    }
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []

    for profesor in GRUPE.keys():
        keyboard.append(
            [InlineKeyboardButton(profesor, callback_data=f"prof_{profesor}")]
        )

    await update.message.reply_text(
        "🚗 Bun venit la Școala Auto Artur Cecan!\n\nAlege profesorul:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("prof_"):
        profesor = data.replace("prof_", "")

        keyboard = []

        for grupa in GRUPE[profesor]:
            keyboard.append(
                [InlineKeyboardButton(grupa, callback_data=f"grupa_{profesor}|{grupa}")]
            )

        await query.edit_message_text(
            f"📚 Grupele profesorului {profesor}:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("grupa_"):
        info = data.replace("grupa_", "")
        profesor, grupa = info.split("|")

        link = GRUPE[profesor][grupa]

        await query.edit_message_text(
            f"✅ Ai selectat:\n\n{grupa}\n\n🔗 Link grup:\n{link}"
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()


if __name__ == "__main__":
    main()
