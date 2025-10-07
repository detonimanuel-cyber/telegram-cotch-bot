# Usa un'immagine Python leggera
FROM python:3.11-slim

# Imposta la cartella di lavoro
WORKDIR /app

# Copia tutto il contenuto del repo nella cartella /app
COPY . .

# Installa le dipendenze dal file requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Avvia il bot
CMD ["python", "coach_bot.py"]
