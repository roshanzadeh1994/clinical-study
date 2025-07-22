from app.database import Base, engine
from app import models  # 👈 خیلی مهمه! بدون این، مدل‌ها شناخته نمی‌شن!

print("Creating tables...")
print(Base.metadata.tables.keys())

Base.metadata.create_all(bind=engine)
print("Done.")
