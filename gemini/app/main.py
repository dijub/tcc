"""Arquivo principal da aplicação FastAPI."""

from fastapi import FastAPI

from app.api.clientes import router as clientes_router
from app.core.database import Base, engine

# Cria as tabelas no banco de dados (para desenvolvimento)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gerenciamento de Clientes",
    description="Uma API para gerenciar clientes.",
    version="1.0.0",
)

app.include_router(
    clientes_router,
    prefix="/clientes",
    tags=["Clientes"],
)


@app.get("/", summary="Endpoint raiz da API")
def read_root():
    """
    Endpoint raiz que retorna uma mensagem de boas-vindas.
    """
    return {"message": "Bem-vindo à API de Gerenciamento de Clientes"}
