from typing import Any

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

from backend.schemas import TransacaoCreate, Transacao, Extrato, Saldo, TransacaoLista
from backend.sql_app import crud
from backend.sql_app.database import engine, get_session, Base
from backend.sql_app.models import now_in_utc

app = FastAPI(
    title="Rinha 2024/Q1",
    docs_url="/api/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_methods=["*"],
    allow_origins=["*"],
    allow_headers=["*"],
)


# @app.on_event("startup")
# async def startup() -> None:
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


@app.middleware("http")
async def http_middleware(request: Request, call_next: Any) -> Response:
    session_maker = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
    async with session_maker.begin() as session:
        request.state.db_session = session

        response: Response = await call_next(request)
        if response.status_code >= status.HTTP_400_BAD_REQUEST:
            await session.rollback()

    return response


@app.post("/clientes/{cliente_id}/transacoes", response_model=Transacao)
async def insert_transacoes(cliente_id: int, transacao: TransacaoCreate, db: AsyncSession = Depends(get_session)) -> Transacao:
    cliente = await crud.get_cliente(cliente_id, db)
    await crud.create_transacao(cliente_id, transacao, db)
    if transacao.tipo == "c":
        saldo_atual = cliente.saldo_atual + transacao.valor
    else:
        saldo_atual = cliente.saldo_atual - transacao.valor
        if saldo_atual + cliente.limite < 0:
            raise HTTPException(status_code=422)

    await crud.update_saldo(cliente, saldo_atual)

    return Transacao(limite=cliente.limite, saldo=saldo_atual)


@app.get("/clientes/{cliente_id}/extrato")
async def extrato(cliente_id: int, db: AsyncSession = Depends(get_session)) -> Extrato:
    cliente = await crud.get_cliente(cliente_id, db, with_transactions=True)
    return Extrato(
        saldo=Saldo(total=cliente.saldo_atual, data_extrato=now_in_utc(), limite=cliente.limite),
        ultimas_transacoes=[
            TransacaoLista(
                valor=transacao.valor,
                tipo=transacao.tipo,
                descricao=transacao.descricao,
                realizada_em=transacao.realizada_em
            ) for transacao in cliente.transacoes
        ]
    )
