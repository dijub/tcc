"""
Aplicação principal FastAPI para o sistema de gestão de clientes.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from database_config import init_database, close_database
from routes import router as cliente_router
from models import Cliente

# Criar aplicação FastAPI
app = FastAPI(
    title="Sistema de Gestão de Clientes",
    description="API REST para gerenciamento de clientes com FastAPI, SQLAlchemy e PostgreSQL",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar roteadores
app.include_router(cliente_router)


@app.on_event("startup")
async def startup_event():
    """
    Evento executado na inicialização da aplicação.
    Inicializa a conexão com o banco de dados e cria as tabelas.
    """
    await init_database()


@app.on_event("shutdown")
async def shutdown_event():
    """
    Evento executado no encerramento da aplicação.
    Fecha as conexões com o banco de dados.
    """
    await close_database()


@app.get("/", tags=["root"])
async def root():
    """
    Endpoint raiz da API.
    
    Returns:
        dict: Informações básicas da API
    """
    return {
        "message": "Sistema de Gestão de Clientes",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """
    Endpoint para verificação de saúde da aplicação.
    
    Returns:
        dict: Status da aplicação
    """
    return {"status": "healthy", "service": "cliente-api"}


if __name__ == "__main__":
    # Executar aplicação com Uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )