import os
import time
import telebot
import openai

# ====== ENV ======
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise RuntimeError("Mancano TELEGRAM_TOKEN o OPENAI_API_KEY nelle variabili d'ambiente.")

openai.api_key = OPENAI_API_KEY
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# ====== PROMPT ======
SYSTEM_PROMPT = (
    "Sei un coach motivazionale energico, diretto e ironico. "
    "Dai incoraggiamenti e mini-task pratici e brevi."
)

# ====== OPENAI WRAPPER ======
def ask_openai(user_message: str) -> str:
    try:
        # Modello compatibile con openai==0.28.1
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message or ""},
            ],
            max_tokens=250,
            temperature=0.9,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI error:", e, flush=True)
        return "Ho un problema a contattare il cervello centrale. Riprova tra poco."

# ====== HANDLERS ======
@bot.message_handler(commands=['start'])
def start(msg):
    print(f"/start from chat_id={msg.chat.id}", flush=True)
    bot.reply_to(msg, "Ciao! Sono il tuo Coach Bot 💪 Scrivimi qualcosa per iniziare!")

@bot.message_handler(func=lambda m: True)
def handle_message(msg):
    try:
        print(f"RX from chat_id={msg.chat.id}: {msg.text}", flush=True)
        reply = ask_openai(msg.text or "")
        print(f"TX preview: {reply[:80]}", flush=True)
        bot.reply_to(msg, reply)
    except Exception as e:
        print("Handler error:", e, flush=True)
        try:
            bot.reply_to(msg, "Oops, ho avuto un intoppo. Riprova tra poco!")
        except Exception as ee:
            print("Secondary reply error:", ee, flush=True)

# ====== BOOT ======
print("Booting Coach Bot...", flush=True)
print(f"HAS_TELEGRAM_TOKEN={bool(TELEGRAM_TOKEN)}  HAS_OPENAI_KEY={bool(OPENAI_API_KEY)}", flush=True)

# Disattiva qualsiasi webhook residuo e scarta eventuali messaggi arretrati
try:
    bot.remove_webhook(drop_pending_updates=True)
    print("Webhook removed.", flush=True)
except Exception as e:
    print("Error removing webhook:", e, flush=True)

# Loop di polling con retry e log
while True:
    try:
        print("Starting polling...", flush=True)
        bot.infinity_polling(skip_pending=True, timeout=20)
    except Exception as e:
        print("Polling crashed:", e, flush=True)
        time.sleep(5)
