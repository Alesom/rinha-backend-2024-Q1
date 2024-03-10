import datetime as dt
from pydantic import BaseModel, Field, ConfigDict, TypeAdapter

from backend.sql_app.models import ClienteDB, now_in_utc

FromAttributes = ConfigDict(from_attributes=True)


class TransacaoCreate(BaseModel):
    valor: int
    tipo: str = Field(..., max_length=1, min_length=1)
    descricao: str = Field(..., max_length=10, min_length=1)


class Transacao(BaseModel):
    limite: int
    saldo: int


class Saldo(BaseModel, **FromAttributes):
    total: int
    data_extrato: dt.datetime
    limite: int


class TransacaoLista(BaseModel, **FromAttributes):
    valor: int
    tipo: str
    descricao: str
    realizada_em: dt.datetime


Transacoes = TypeAdapter(list[TransacaoLista])
