"""
Camada de serviço/repositório CRUD para a entidade Cliente.
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from models import Cliente
from schemas import ClienteCreate, ClienteUpdate
from fastapi import HTTPException, status


class ClienteService:
    """
    Serviço CRUD para operações com a entidade Cliente.
    
    Implementa as operações básicas de Create, Read, Update e Delete
    com tratamento de erros e validações específicas do domínio.
    """
    
    @staticmethod
    def create(db: Session, cliente_create: ClienteCreate) -> Cliente:
        """
        Cria um novo cliente no banco de dados.
        
        Args:
            db (Session): Sessão do banco de dados
            cliente_create (ClienteCreate): Dados do cliente para criação
            
        Returns:
            Cliente: Cliente criado com ID gerado
            
        Raises:
            HTTPException: 409 se email já existir, 400 para outros erros
        """
        try:
            # Criar nova instância do modelo
            db_cliente = Cliente(
                nome=cliente_create.nome,
                email=cliente_create.email,
                telefone=cliente_create.telefone
            )
            
            # Adicionar à sessão e fazer commit
            db.add(db_cliente)
            db.commit()
            db.refresh(db_cliente)
            
            return db_cliente
            
        except IntegrityError as e:
            db.rollback()
            # Verificar se é erro de email duplicado
            if "uq_cliente_email" in str(e.orig) or "unique constraint" in str(e.orig).lower():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Cliente com email '{cliente_create.email}' já existe"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Erro de integridade dos dados"
                )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao criar cliente: {str(e)}"
            )
    
    @staticmethod
    def get_by_id(db: Session, cliente_id: int) -> Optional[Cliente]:
        """
        Busca um cliente pelo ID.
        
        Args:
            db (Session): Sessão do banco de dados
            cliente_id (int): ID do cliente
            
        Returns:
            Optional[Cliente]: Cliente encontrado ou None
        """
        return db.query(Cliente).filter(Cliente.id == cliente_id).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[Cliente]:
        """
        Busca um cliente pelo email.
        
        Args:
            db (Session): Sessão do banco de dados
            email (str): Email do cliente
            
        Returns:
            Optional[Cliente]: Cliente encontrado ou None
        """
        return db.query(Cliente).filter(Cliente.email == email).first()
    
    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100) -> List[Cliente]:
        """
        Lista clientes com paginação.
        
        Args:
            db (Session): Sessão do banco de dados
            skip (int): Número de registros para pular (offset)
            limit (int): Número máximo de registros para retornar
            
        Returns:
            List[Cliente]: Lista de clientes
        """
        return db.query(Cliente).offset(skip).limit(limit).all()
    
    @staticmethod
    def update(db: Session, cliente_id: int, cliente_update: ClienteUpdate) -> Optional[Cliente]:
        """
        Atualiza um cliente existente.
        
        Args:
            db (Session): Sessão do banco de dados
            cliente_id (int): ID do cliente a ser atualizado
            cliente_update (ClienteUpdate): Dados para atualização
            
        Returns:
            Optional[Cliente]: Cliente atualizado ou None se não encontrado
            
        Raises:
            HTTPException: 409 se email já existir, 400 para outros erros
        """
        try:
            # Buscar cliente existente
            db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
            
            if not db_cliente:
                return None
            
            # Atualizar apenas campos fornecidos
            update_data = cliente_update.model_dump(exclude_unset=True)
            
            for field, value in update_data.items():
                setattr(db_cliente, field, value)
            
            db.commit()
            db.refresh(db_cliente)
            
            return db_cliente
            
        except IntegrityError as e:
            db.rollback()
            # Verificar se é erro de email duplicado
            if "uq_cliente_email" in str(e.orig) or "unique constraint" in str(e.orig).lower():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Cliente com email '{cliente_update.email}' já existe"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Erro de integridade dos dados"
                )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao atualizar cliente: {str(e)}"
            )
    
    @staticmethod
    def delete(db: Session, cliente_id: int) -> bool:
        """
        Remove um cliente do banco de dados.
        
        Args:
            db (Session): Sessão do banco de dados
            cliente_id (int): ID do cliente a ser removido
            
        Returns:
            bool: True se removido com sucesso, False se não encontrado
            
        Raises:
            HTTPException: 400 para erros durante a remoção
        """
        try:
            # Buscar cliente existente
            db_cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
            
            if not db_cliente:
                return False
            
            # Remover cliente
            db.delete(db_cliente)
            db.commit()
            
            return True
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao deletar cliente: {str(e)}"
            )


# Instância do serviço para uso nas rotas
cliente_service = ClienteService()
