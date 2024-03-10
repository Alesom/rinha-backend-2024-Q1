from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from backend.sql_app.models import ClienteDB, TransacaoDB


async def get_cliente(
    cliente_id: int, db: AsyncSession
) -> ClienteDB:
    query = (
        select(ClienteDB)
        .join(ClienteDB.transacoes, isouter=True)
        .options(contains_eager(ClienteDB.transacoes))
        .where(ClienteDB.id == cliente_id)
        .order_by(TransacaoDB.id.desc())
        .limit(10)
    )

    result = await db.execute(query)

    if cliente := result.unique().scalars().one():
        return cliente
    raise HTTPException(status_code=404)
