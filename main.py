import os
import threading
from flask import Flask
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Mini-serveur Web pour Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot actif !"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

# CONFIGURATION
TELEGRAM_TOKEN = "8922246133:AAElSpQlhrjtmxfNgubIdKWngAIIp823CkQ"
VINTED_SESSION = "VTduNEtoREFlWWhBTzBhYUFzK0pQMjlTWDBYbkVielpNUVd5ZFkrekZOS25KbTIwN2svVTlYNGpJQjBzeWdXRnVTTTJjWFJCMmVYVFFXMVlUaHQ3WjRpUXlxb2kzU0swR0VSUnZZbXdRN0tuRHpwMXFaNWNYdDB0QkRydTZjdWhvKzVjbEs2OE96VEJneXpmczltZzhqRUtYSzh4YXZEc1JzYXNQdnBtTmc2OXN3YmQwSDRRdjVpelptWGZsWW00MHB2SEJWTjJXaEp5eWllSDFYOHVGTEdJV2h2bXkwN2E1ZFdWbS84c0JuV0dpQ2RYSHRGQnB1YUp1cWUvdDE2VGx3djR5YTFLcDQ0cS9yS0p3dE52UXpBbDJrVmFuZ2xiVStxTTYyUnJWWTd3WHhVY0R6cGR1SmlDbXdlZjVERy8tLThZT1N3YVFlNmdjMlNYWkhzSHp0TWc9PQ%3D%3D--8f33e410b4326c6b275e9e12627f024f13393446"

def dupliquer_annonce(item_id):
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    })

    # 1. Première requête sur la page d'accueil pour initialiser les cookies Vinted
    try:
        session.get("https://www.vinted.fr")
    except Exception as e:
        return False, f"❌ Impossible de joindre Vinted : {e}"

    # 2. Ajout du cookie de session utilisateur
    session.cookies.set("_vinted_fr_session", VINTED_SESSION, domain=".vinted.fr")

    # 3. Récupération des infos de l'annonce
    res = session.get(f"https://www.vinted.fr/api/v2/items/{item_id}")
    
    if res.status_code == 401 or res.status_code == 403:
        return False, f"❌ Erreur {res.status_code} : Session Vinted rejetée ou bloquée par l'anti-bot."
    elif res.status_code != 200:
        return False, f"❌ Échec (Code {res.status_code}). Annonce introuvable."

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

    # 4. Suppression
    del_res = session.delete(f"https://www.vinted.fr/api/v2/items/{item_id}")
    if del_res.status_code not in [200, 204]:
        return False, f"❌ Erreur lors de la suppression (Code {del_res.status_code})."

    # 5. Republication
    post_res = session.post("https://www.vinted.fr/api/v2/items", json=payload)
    if post_res.status_code in [200, 201]:
        return True, "✅ Annonce supprimée et republiée avec succès !"
    
    return False, f"❌ Erreur lors de la republication (Code {post_res.status_code})."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "vinted.fr" in text and "/items/" in text:
        try:
            item_id = text.split("/items/")[1].split("-")[0]
            await update.message.reply_text("🔄 Traitement de l'annonce en cours...")
            success, msg = dupliquer_annonce(item_id)
            await update.message.reply_text(msg)
        except Exception as e:
            await update.message.reply_text(f"❌ Erreur de lecture du lien : {e}")
    else:
        await update.message.reply_text("Envoie-moi un lien d'annonce Vinted valide.")

if __name__ == "__main__":
    app_telegram = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app_telegram.run_polling()

