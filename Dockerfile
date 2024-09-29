FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8050

CMD ["gunicorn", "-b", "0.0.0.0:8050", "games_market_dash_Dm_Ch:server"]
