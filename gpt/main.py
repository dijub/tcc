from app.db.session import get_db
from sqlalchemy import text

db = next(get_db())
print("Conectado ao banco de dados")
result = db.execute(text("SELECT version()"))
print(result.scalar())
