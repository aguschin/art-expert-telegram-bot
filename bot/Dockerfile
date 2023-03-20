FROM python:3.9.5-slim
WORKDIR /app


COPY requirements.txt .
RUN pip install -r requirements.txt && pip cache purge
COPY . ./
CMD python bot.py

