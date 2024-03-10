from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas import TransacaoCreate
from backend.sql_app import crud
from backend.sql_app.database import get_session
from backend.sql_app.models import now_in_utc

app = FastAPI(
    title="Rinha 2024/Q1",
    docs_url="/api/docs",
    redoc_url=None,
)


@app.post("/clientes/{cliente_id}/transacoes")
async def insert_transacoes(
    cliente_id: int,
    transacao: TransacaoCreate,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    if cliente_id < 1 or cliente_id > 5:
        raise HTTPException(status_code=404)

    result = await session.execute(
        text(
            f"SELECT limite, saldo_atual FROM cliente WHERE id = {cliente_id} FOR UPDATE"
        )
    )

    limite, saldo = result.one()

    if transacao.tipo == "d":
        transacao.valor = -transacao.valor

    saldo_atual = saldo + transacao.valor

    if saldo_atual + limite < 0:
        raise HTTPException(status_code=422)

    await session.execute(
        text(f"UPDATE cliente SET saldo_atual = {saldo_atual} WHERE id = {cliente_id}")
    )

    await session.execute(
        text(f"INSERT INTO transacao(cliente_id, tipo, valor, descricao, realizada_em) VALUES "
             f"({cliente_id}, '{transacao.tipo}', {transacao.valor}, '{transacao.descricao}', '{now_in_utc()}')")
    )

    return ORJSONResponse(content={"limite": limite, "saldo": saldo_atual})


@app.get("/clientes/{cliente_id}/extrato")
async def get_extrato(
    cliente_id: int, session: AsyncSession = Depends(get_session)
) -> ORJSONResponse:
    if cliente_id < 1 or cliente_id > 5:
        raise HTTPException(status_code=404)

    cliente = await crud.get_cliente(cliente_id, session)
    return ORJSONResponse(content={
        "saldo": {
            "total": cliente.saldo_atual,
            "data_extrato": now_in_utc(),
            "limite": cliente.limite,
        },
        "ultimas_transacoes": [
            {
                "valor": transacao.valor,
                "tipo": transacao.tipo,
                "descricao": transacao.descricao,
                "realizada_em": transacao.realizada_em
            } for transacao in cliente.transacoes
        ]
    })
