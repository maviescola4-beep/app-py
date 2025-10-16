# MODELS DO PROJETO

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, Numeric, CheckConstraint

)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Base para criar as classes como tabela do banco de dados 
base = declarative_base()


# =========== MODELS ===========

class Cliente(base): #Model que representa o cliente 
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(120), nullable=False)
    telefone = Column(String(15), nullable=False)

    #Relacionamento: um cliente pode ter muitos pedidos
    pedidos = relationship("Pedido", back_populates= "cliente", cascade="all, delte-orphan")

    def __repr__(self):
        return f"<ClienteId={self.id}, Nome do Cliente={self.nome!r}, emailCliente={self.email!r}>"
    
    #=================== Conexões e sessões ===================

def get_engine(db_ur1: str = "sqlite:///loja_jogos.db"):
        return create_engine(db_ur1, echo=False, future=True)
    
def create_session(db_ur1: str = "sqlite:///loja_jogos.db"):
        engine = get_engine(db_ur1)
        base.metadata.create_all(engine)
        Sessionlocal = sessionmaker(bind=engine, autoflush=False, autocomit=False, future=True)
        return Sessionlocal()
