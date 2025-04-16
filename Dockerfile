FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl gnupg
RUN curl -fsSL https://ollama.com/install.sh | sh
RUN ollama pull mistral

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

ENV OLLAMA_URL=http://localhost:11434/api/generate
EXPOSE 11434

CMD ["sh", "-c", "ollama serve & sleep 3 && python main.py"]
