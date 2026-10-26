import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Tes identifiants
TELEGRAM_TOKEN = "8922246133:AAElSpQlhrjtmxFNgubIdKwngAIIp823CkQ"
VINTED_SESSION = "STdHcU85VTlpSFkyOWcyZUhFZFNNcVZRSHlhbUU4cGtmTTNXYy9FaDJ4dkNDYjE5WU9hK09yYmpTUkpOa0VQcUlRSmFuVCt5Umt3eGNlUVczREVOdmxWNFI0Ukp2bHZqdEN3RWg1TFMwVUxSSHpIZ1V4RHdyd094YkZBL1pDTkpzWFFRRWtkemJTZVd0TWJOelBGcXZvL2pRT1N2WUN6b25pQW1YVjQxWmw5bUJKcDdDWm9TVFBxN2l6TUpYMmt5YlVQdDJTZ0dLV3JmRG9sRWlLMk9VUFR1MEVSR2pkTEp6ZStpVU1NQklmSkJBT0MrdUpwRE9YN2ZmMmVBeTRUQVp1cDg1bTErVjZnVVdZUzV6QW9YNEIydWx2NDJBbkdiL2FUc1plaW1NbnFjUC9GUGZQOXhVdERTSUdIYW4wYmgtLWNrMmF0V25sNSs4T2tkZkMyam43R3c9PQ%3D%3D--277a21dd49622e9abd4ff34cdf105d4972e04b43"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": f"_vinted_fr_session={VINTED_SESSION}"
}

def dupliquer_annonce(item_id):
    session = requests.Session()
    session.headers.update(headers)

    # Récupération des données
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

    # Suppression
    session.delete(f"https://www.vinted.fr/api/v2/items/{item_id}")

    # Republication
    res_post = session.post("https://www.vinted.fr/api/v2/items", json=payload)
    if res_post.status_code in [200, 201]:
        return True, "✅ Annonce républiée avec succès !"
    else:
        return False, f"⚠️ Erreur lors de la republication ({res_post.status_code})."

async def gerer_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "vinted.fr/items/" in url:
        item_id = url.split("items/")[1].split("-")[0]
        await update.message.reply_text(f"⏳ Repost de l'article #{item_id} en cours...")
        succes, msg = dupliquer_annonce(item_id)
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text("Envoie un lien Vinted valide.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), gerer_message))
    app.run_polling()
