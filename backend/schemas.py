import datetime as dt
from pydantic import BaseModel, Field


class TransacaoCreate(BaseModel):
    valor: int
    tipo: str = Field(..., max_length=1, min_length=1)
    descricao: str = Field(..., max_length=10, min_length=1)


class Transacao(BaseModel):
    limite: int
    saldo: int


class Saldo(BaseModel):
    total: int
    data_extrato: dt.datetime
    limite: int


class TransacaoLista(BaseModel):
    valor: int
    tipo: str
    descricao: str
    realizada_em: dt.datetime


class Extrato(BaseModel):
    saldo: Saldo
    ultimas_transacoes: list[TransacaoLista]
