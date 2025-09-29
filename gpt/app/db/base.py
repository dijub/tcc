from sqlalchemy.orm import declarative_base

__all__ = ["Base"]

# SQLAlchemy Declarative Base
# Central Base class that all ORM models in the application should inherit from.
Base = declarative_base()
