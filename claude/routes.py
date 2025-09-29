"""
Rotas FastAPI para a entidade Cliente.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from database_config import get_database_session
from schemas import ClienteCreate, ClienteUpdate, ClienteRead
from crud import cliente_service


# Criar roteador para clientes
router = APIRouter(
    prefix="/clientes",
    tags=["clientes"],
    responses={404: {"description": "Cliente não encontrado"}}
)


@router.post(
    "/",
    response_model=ClienteRead,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo cliente",
    description="Cria um novo cliente no sistema com os dados fornecidos."
)
async def create_cliente(
    cliente_create: ClienteCreate,
    db: Session = Depends(get_database_session)
) -> ClienteRead:
    """
    Criar um novo cliente.
    
    Args:
        cliente_create: Dados do cliente para criação
        db: Sessão do banco de dados (injetada automaticamente)
        
    Returns:
        ClienteRead: Cliente criado com ID e data_criacao
        
    Raises:
        HTTPException: 
            - 409: Email já existe
            - 400: Dados inválidos
            - 422: Erro de validação dos dados de entrada
    """
    cliente = cliente_service.create(db=db, cliente_create=cliente_create)
    return ClienteRead.model_validate(cliente)


@router.get(
    "/",
    response_model=List[ClienteRead],
    summary="Listar clientes",
    description="Lista todos os clientes cadastrados com paginação opcional."
)
async def list_clientes(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros para retornar"),
    db: Session = Depends(get_database_session)
) -> List[ClienteRead]:
    """
    Listar clientes com paginação.
    
    Args:
        skip: Número de registros para pular (offset)
        limit: Número máximo de registros para retornar
        db: Sessão do banco de dados (injetada automaticamente)
        
    Returns:
        List[ClienteRead]: Lista de clientes
    """
    clientes = cliente_service.list(db=db, skip=skip, limit=limit)
    return [ClienteRead.model_validate(cliente) for cliente in clientes]


@router.get(
    "/{cliente_id}",
    response_model=ClienteRead,
    summary="Buscar cliente por ID",
    description="Busca um cliente específico pelo seu identificador único."
)
async def get_cliente(
    cliente_id: int,
    db: Session = Depends(get_database_session)
) -> ClienteRead:
    """
    Buscar cliente por ID.
    
    Args:
        cliente_id: ID do cliente
        db: Sessão do banco de dados (injetada automaticamente)
        
    Returns:
        ClienteRead: Dados do cliente
        
    Raises:
        HTTPException: 404 se cliente não for encontrado
    """
    cliente = cliente_service.get_by_id(db=db, cliente_id=cliente_id)
    
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente com ID {cliente_id} não encontrado"
        )
    
    return ClienteRead.model_validate(cliente)


@router.put(
    "/{cliente_id}",
    response_model=ClienteRead,
    summary="Atualizar cliente",
    description="Atualiza os dados de um cliente existente. Campos não fornecidos permanecerão inalterados."
)
async def update_cliente(
    cliente_id: int,
    cliente_update: ClienteUpdate,
    db: Session = Depends(get_database_session)
) -> ClienteRead:
    """
    Atualizar cliente existente.
    
    Args:
        cliente_id: ID do cliente a ser atualizado
        cliente_update: Dados para atualização (campos opcionais)
        db: Sessão do banco de dados (injetada automaticamente)
        
    Returns:
        ClienteRead: Cliente atualizado
        
    Raises:
        HTTPException: 
            - 404: Cliente não encontrado
            - 409: Email já existe para outro cliente
            - 400: Dados inválidos
            - 422: Erro de validação dos dados de entrada
    """
    # Verificar se há dados para atualizar
    update_data = cliente_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum campo fornecido para atualização"
        )
    
    cliente = cliente_service.update(
        db=db, 
        cliente_id=cliente_id, 
        cliente_update=cliente_update
    )
    
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente com ID {cliente_id} não encontrado"
        )
    
    return ClienteRead.model_validate(cliente)


@router.delete(
    "/{cliente_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar cliente",
    description="Remove um cliente do sistema permanentemente."
)
async def delete_cliente(
    cliente_id: int,
    db: Session = Depends(get_database_session)
) -> None:
    """
    Deletar cliente.
    
    Args:
        cliente_id: ID do cliente a ser removido
        db: Sessão do banco de dados (injetada automaticamente)
        
    Raises:
        HTTPException: 
            - 404: Cliente não encontrado
            - 400: Erro durante a remoção
    """
    success = cliente_service.delete(db=db, cliente_id=cliente_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente com ID {cliente_id} não encontrado"
        )
    
    # Retorno vazio com status 204 No Content
