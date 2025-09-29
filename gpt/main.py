from fastapi import FastAPI
from app.api import api_router
from app.db.base import Base
from app.db.session import engine

# Garante criação das tabelas (apenas para dev/prototipagem)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TCC API")
app.include_router(api_router)

# Execução direta: `python -m app`
if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
