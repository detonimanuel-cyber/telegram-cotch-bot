import os
import telebot
import openai

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise RuntimeError("Mancano TELEGRAM_TOKEN o OPENAI_API_KEY nelle variabili d'ambiente.")

openai.api_key = OPENAI_API_KEY
bot = telebot.TeleBot(TELEGRAM_TOKEN)

SYSTEM_PROMPT = ("Sei un coach motivazionale energico, diretto e ironico. "
                 "Dai incoraggiamenti e mini-task pratici e brevi.")

def ask_openai(user_message):
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message or ""}
            ],
            max_tokens=250,
            temperature=0.9
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return "Ho un problema a contattare il cervello centrale. Riprova tra poco."

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "Ciao! Sono il tuo Coach Bot 💪 Scrivimi qualcosa per iniziare!")

@bot.message_handler(func=lambda m: True)
def handle_message(msg):
    bot.reply_to(msg, ask_openai(msg.text))

if __name__ == "__main__":
# Disattiva qualsiasi webhook rimasto attivo prima di usare getUpdates
bot.remove_webhook()

# Avvia il long-polling e scarta eventuali messaggi “arretrati”
bot.infinity_polling(skip_pending=True, timeout=20)
