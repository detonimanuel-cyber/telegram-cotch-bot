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

print("Booting Coach Bot...", flush=True)
print(f"HAS_TELEGRAM_TOKEN={bool(TELEGRAM_TOKEN)}  HAS_OPENAI_KEY={bool(OPENAI_API_KEY)}", flush=True)

# Disattiva qualsiasi webhook residuo (per evitare errori 409)
try:
    bot.remove_webhook()
    print("Webhook removed.", flush=True)
except Exception as e:
    print("Error removing webhook:", e, flush=True)

# Loop di polling con retry automatico
while True:
    try:
        print("Starting polling...", flush=True)
        bot.infinity_polling(skip_pending=True, timeout=20)
    except Exception as e:
        print("Polling crashed:", e, flush=True)
        time.sleep(5)
