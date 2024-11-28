# Установлюємо базовий образ Python
FROM python:3.10

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# Копіюємо файл requirements.txt у робочу директорію
COPY requirments.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirments.txt

# Копіюємо всі файли проєкту у робочу директорію контейнера
COPY . .

# Відкриваємо порт для доступу до Django
EXPOSE 8000

# Команда за замовчуванням для запуску сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

