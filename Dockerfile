FROM python:3.11-slim

# Installeer ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Werkmap
WORKDIR /app

# Kopieer bestanden
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Start de bot
CMD ["python", "bot.py"]
