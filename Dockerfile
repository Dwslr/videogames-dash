# Базовый образ для Python-приложения
FROM python:3.9

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt . 
RUN pip install -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Устанавливаем Nginx
RUN apt-get update && apt-get install -y nginx

# Копируем конфигурацию Nginx в контейнер
COPY nginx.conf /etc/nginx/nginx.conf

# Экспонируем порты Nginx и Gunicorn
EXPOSE 80 8050

# Запуск Nginx и приложения через Gunicorn
CMD service nginx start && gunicorn -b 0.0.0.0:8050 games_market_dash_Dm_Ch:server
