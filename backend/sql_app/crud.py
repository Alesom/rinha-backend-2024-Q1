from typing import Annotated

from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.sql_app.models import ClienteDB, TransacaoDB
from backend.schemas import TransacaoCreate


async def get_cliente(cliente_id: int, db: AsyncSession, with_transactions: bool = False) -> ClienteDB:
    query = select(ClienteDB)

    if with_transactions:
        query = query.options(joinedload(ClienteDB.transacoes)).limit(10).order_by(TransacaoDB.realizada_em.desc())

    query = query.where(ClienteDB.id == cliente_id)

    result = await db.execute(query)

    if cliente := result.scalars().first():
        return cliente
    raise HTTPException(status_code=404)


async def create_transacao(cliente_id: int, transacao: TransacaoCreate, db: AsyncSession) -> TransacaoDB:
    transacao = TransacaoDB(
        cliente_id=cliente_id,
        tipo=transacao.tipo,
        valor=transacao.valor,
        descricao=transacao.descricao,
    )
    db.add(transacao)
    return transacao


async def update_saldo(cliente: ClienteDB, saldo: int) -> None:
    setattr(cliente, "saldo_atual", saldo)


# def update_saldo(client_id: int, saldo: int):
#     return Cliente.update().values(saldo=saldo).where(Cliente.id == client_id)
#
#
# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()
#
#
# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()
#
#
# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()
#
#
# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
#
#
# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()
#
#
# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
