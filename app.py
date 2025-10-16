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

#app.py

from decimal import Decimal
from models import create_session, Cliente, Produto, Pedido, ItemPedido

DB_URL = "sqlite:///loja_jogos.db"
session = create_session(DB_URL)

def cadastrar_cliente():
    nome = input("Nome do cliente: ").strip()
    email = input("Email do cliente: ").strip()
    telefone = input("Telefone do cliente: ")strip() or nome

    cliente = Cliente(nome=nome, email=email, telefone=telefone)
    session.add(cliente)
    session.commit()
    print(f"Cliente cadastrado: {cliente}")


def cadastrar_produto():
    nome_produto = input("Nome do produto: ").strip()
    preco = Decimal(input("Preço do Produto (ex: 199.99): ")).replace(",",".")
    estoque = int(input("Estoque: "))

    produto = Produto(nome_produto=nome_produto, preco=preco, estoque=estoque)
    session.add(produto)
    session.commit()
    print(f"Produto Cadastrado: {nome_produto}")

def criar_pedido():
    cliente_id = int(input("Digite o ID do Cliente: "))
    pedido = Pedido(cliente_id=cliente_id)
    session.add(pedido)
    session.flush() # garante o id do pedido antes de inserir itens 

    print("Adicione itens (Enter em produto_id parafinalizar). ")
    while True:
         val = input("Produto ID(Enter para sair): ").strip()
         if not val:
              break
         Produto_id = int(val)
         quantidade = int(input("Quantidade: "))

         # Buscar produto para pegar preço e validar o estoque 
         produto = session.get(Produto, Produto_id)
         if produto is Nome:
              print("Produto não encontrado. ")
              continue
         
         if produto.estoque < quantidade:
              print(f"Estoque insuficiente. Quantidade Disponível: {produto.estoque}")

        # Debita do estoque 
         produto.estoque -= quantidade

         item = ItemPedido(
              pedido_id = pedido.id,
              produto_id = Produto_id
              quantidade = quantidade,
              preco_unit = produto.preco
         )
         session.add(item)

    session.commit()