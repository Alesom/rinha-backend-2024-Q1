import datetime as dt
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy_utc import UtcDateTime


class Base(DeclarativeBase):
    pass


def now_in_utc() -> dt.datetime:
    return dt.datetime.now(tz=dt.timezone.utc)


class ClienteDB(Base):
    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(primary_key=True)
    limite: Mapped[int]
    saldo_inicial: Mapped[int]
    saldo_atual: Mapped[int]

    transacoes = relationship(
        "TransacaoDB", lazy="raise", uselist=True, back_populates="cliente"
    )


class TransacaoDB(Base):
    __tablename__ = "transacao"

    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id"))
    tipo: Mapped[str] = mapped_column(String(1))
    valor: Mapped[int]
    descricao: Mapped[str] = mapped_column(String(10))
    realizada_em: Mapped[dt.datetime] = mapped_column(
        UtcDateTime, nullable=False, default=now_in_utc
    )

    cliente = relationship(
        "ClienteDB", lazy="raise", uselist=False, back_populates="transacoes"
    )
