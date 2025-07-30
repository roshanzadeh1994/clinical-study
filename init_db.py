import time
from sqlalchemy.exc import OperationalError
from app.db.database import Base, engine
from app.db import models

MAX_RETRIES = 10

for i in range(MAX_RETRIES):
    try:
        print("🔄 Trying to connect to the database...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully.")
        break
    except OperationalError as e:
        print(f"❌ Database not ready yet ({i + 1}/{MAX_RETRIES})... retrying in 2s")
        time.sleep(2)
else:
    print("🚨 Could not connect to the database after several attempts.")
    exit(1)
