import os
import threading
from flask import Flask
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Serveur factice pour garder Render gratuit
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot actif !"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# Identifiants
TELEGRAM_TOKEN = "TON_TOKEN_BOTFATHER"
VINTED_SESSION = "TA_SESSION_VINTED"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Cookie": f"_vinted_fr_session={VINTED_SESSION}"
}

def dupliquer_annonce(item_id):
    session = requests.Session()
    session.headers.update(headers)

    res = session.get(f"https://www.vinted.fr/api/v2/items/{item_id}")
    if res.status_code != 200:
        return False, "❌ Échec. Session expirée ou annonce introuvable."

    item = res.json().get("item", {})
    payload = {
        "item": {
            "title": item.get("title"),
            "description": item.get("description"),
            "price": item.get("price"),
            "currency": item.get("currency"),
            "category_id": item.get("category_id"),
            "status_id": item.get("status_id"),
        }
    }

    session.delete(f"https://www.vinted.fr/api/v2/items/{item_id}")
    res_post = session.post("https://www.vinted.fr/api/v2/items", json=payload)
    
    if res_post.status_code in [200, 201]:
        return True, "✅ Annonce republiée avec succès !"
    return False, "❌ Erreur lors de la republication."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "vinted.fr" in text and "/items/" in text:
        try:
            item_id = text.split("/items/")[1].split("-")[0]
            await update.message.reply_text("🔄 Traitement de l'annonce en cours...")
            success, msg = dupliquer_annonce(item_id)
            await update.message.reply_text(msg)
        except Exception:
            await update.message.reply_text("❌ Lien Vinted invalide.")
    else:
        await update.message.reply_text("Envoie-moi un lien d'annonce Vinted valide.")

if __name__ == "__main__":
    app_telegram = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app_telegram.run_polling()
