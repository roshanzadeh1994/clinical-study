FROM python:3.11-slim

WORKDIR /app

# نصب پیش‌نیازها
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# کپی کدهای پروژه
COPY ./app /app/app
COPY ./init_db.py /app/init_db.py

# اجرای init_db و بعد اجرای برنامه
CMD ["sh", "-c", "python init_db.py && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
