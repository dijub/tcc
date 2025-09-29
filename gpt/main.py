from app.db.session import get_db
from sqlalchemy import text
from app.models.cliente import Cliente
from app.db.base import Base
db = next(get_db())
engine = db.get_bind()
Base.metadata.create_all(engine)
print("Conectado ao banco de dados")
result = db.execute(text("SELECT version()"))
print(result.scalar())
