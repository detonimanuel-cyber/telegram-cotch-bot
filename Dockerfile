# Usa un'immagine Python leggera
FROM python:3.10-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file del progetto
COPY . /app

# Installa le dipendenze
RUN pip install -r requirements.txt

# Comando per avviare il bot
CMD ["python", "coach_bot.py"]
