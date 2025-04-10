# Використовуємо офіційний образ Python
FROM python:3.12

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . /app

# Запускаємо бота
CMD ["python", "main.py"]
