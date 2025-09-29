from app.core.database import SessionLocal, Base
from sqlalchemy import text
from app.models.cliente import Cliente

db = SessionLocal()

Base.metadata.create_all(bind=db.bind)
print(db.execute(text("SELECT version()")).fetchone())

db.close()