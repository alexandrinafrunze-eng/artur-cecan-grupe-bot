from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ConversationHandler,
    ContextTypes, filters
)
import os
import json
import asyncio
import gspread
from google.oauth2.service_account import Credentials

TOKEN = os.getenv("BOT_TOKEN")
SHEET_ID = os.getenv("SHEET_ID")
SHEET_GID = int(os.getenv("SHEET_GID", "0"))
GOOGLE_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")

ASK_NAME, ASK_IDNP = range(2)

GRUPE_LINKURI = {
    "501": {
        "sediu": "Botanica",
        "instructor": "Pădureț Andrei",
        "link": "https://t.me/+xr11I1hqhegwOGZi"
    },
    "502": {
        "sediu": "Botanica",
        "instructor": "Pădureț Andrei",
        "link": "https://t.me/+ZnpPMLiz31ZlNWNi"
    },
    "503": {
        "sediu": "Botanica",
        "instructor": "Murahovschi Pavel",
        "link": "https://t.me/+FIVltLewmUQxMWYy"
    },
    "42": {
        "sediu": "Ciocana",
        "instructor": "Uscatu Ion-Mihail",
        "link": "https://t.me/+eqOPYvLSVntlMWJi"
    },
    "43": {
        "sediu": "Ciocana",
        "instructor": "Uscatu Ion-Mihail",
        "link": "https://t.me/+pWJUYFn7kesyMzli"
    },
    "44": {
        "sediu": "Ciocana",
        "instructor": "Cecan Artur",
        "link": "https://t.me/+9xcdpLU0AVM1MmJi"
    }
}


def normalize(text):
    return str(text).strip().lower().replace("  ", " ")


def get_sheet_records():
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    creds_dict = json.loads(GOOGLE_JSON)
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(creds)

    spreadsheet = client.open_by_key(SHEET_ID)
    worksheet = spreadsheet.get_worksheet_by_id(SHEET_GID)

    return worksheet.get_all_records()


def find_student(full_name, last4):
    name_input = normalize(full_name)
    last4 = str(last4).strip()

    records = get_sheet_records()

    for row in records:
        name = normalize(row.get("Nume/Prenume", ""))
        idnp = str(row.get("CNP Cursant", "")).strip()
        grupa = str(row.get("Grupa", "")).strip()

        if not name or not idnp or not grupa:
            continue

        if name_input == name and idnp.endswith(last4):
            return {
                "name": row.get("Nume/Prenume", ""),
                "grupa": grupa,
                "idnp_last4": last4
            }

    return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "<b>🚗 Școala Auto Artur Cecan</b>\n\n"
        "Pentru a primi acces în grupa ta Telegram,\n"
        "te rugăm să confirmăm înscrierea.\n\n"
        "Scrie <b>Numele și Prenumele</b> exact ca la înscriere:",
        parse_mode="HTML"
    )
    return ASK_NAME


async def ask_idnp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["full_name"] = update.message.text.strip()

    await update.message.reply_text(
        "Acum scrie <b>ultimele 4 cifre din IDNP</b>:",
        parse_mode="HTML"
    )
    return ASK_IDNP


async def verify_student(update: Update, context: ContextTypes.DEFAULT_TYPE):
    last4 = update.message.text.strip()
    full_name = context.user_data.get("full_name", "")

    if not last4.isdigit() or len(last4) != 4:
        await update.message.reply_text(
            "Te rog să introduci doar <b>4 cifre</b>.",
            parse_mode="HTML"
        )
        return ASK_IDNP

    student = find_student(full_name, last4)

    if not student:
        await update.message.reply_text(
            "❌ Nu am găsit această înscriere.\n\n"
            "Verifică numele/prenumele și ultimele 4 cifre din IDNP.\n"
            "Dacă problema persistă, contactează secretariatul."
        )
        return ConversationHandler.END

    grupa = student["grupa"]

    if grupa not in GRUPE_LINKURI:
        await update.message.reply_text(
            f"✅ Te-am identificat în baza noastră.\n\n"
            f"📚 Grupa ta este: <b>{grupa}</b>\n\n"
            f"Momentan această grupă nu are link Telegram setat în bot.",
            parse_mode="HTML"
        )
        return ConversationHandler.END

    info = GRUPE_LINKURI[grupa]

    keyboard = [
        [InlineKeyboardButton("🔗 Intră în grup", url=info["link"])]
    ]

    await update.message.reply_text(
        "<b>🚗 Școala Auto Artur Cecan</b>\n\n"
        "<b>✅ Te-am identificat în baza noastră.</b>\n\n"
        f"👤 <b>Cursant:</b> {student['name']}\n"
        f"📍 <b>Sediul:</b> {info['sediu']}\n"
        f"📚 <b>Grupa:</b> {grupa}\n"
        f"👨‍🏫 <b>Instructor:</b> {info['instructor']}\n\n"
        "Apasă pe butonul de mai jos pentru a intra în "
        "<b>grupul Telegram al grupei tale</b>.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Proces anulat. Scrie /start pentru a începe din nou.")
    return ConversationHandler.END


async def main():
    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_idnp)],
            ASK_IDNP: [MessageHandler(filters.TEXT & ~filters.COMMAND, verify_student)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv)

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
