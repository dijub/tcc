from app.core.database import SessionLocal
from sqlalchemy import text



db = SessionLocal()

print(db.execute(text("SELECT version()")).fetchone())

db.close()