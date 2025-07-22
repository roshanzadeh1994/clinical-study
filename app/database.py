from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# استفاده از مقدار محیطی (env) برای آدرس دیتابیس، و مقدار پیش‌فرض برای توسعه محلی
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@postgres:5432/clinical_db"
)

# ساخت engine برای اتصال به دیتابیس
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True  # مفید برای بررسی اتصال سالم
)

# ساخت session برای استفاده در endpointها
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base کلاس پایه‌ی ORM مدل‌ها
Base = declarative_base()
