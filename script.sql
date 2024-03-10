CREATE UNLOGGED TABLE cliente (
	id SERIAL PRIMARY KEY,
	limite INTEGER NOT NULL,
    saldo_inicial INTEGER NOT NULL,
    saldo_atual INTEGER NOT NULL
);

CREATE UNLOGGED TABLE transacao (
	id SERIAL PRIMARY KEY,
	cliente_id INTEGER NOT NULL,
	valor INTEGER NOT NULL,
	tipo VARCHAR(1) NOT NULL,
	descricao VARCHAR(10) NOT NULL,
	realizada_em TIMESTAMP NOT NULL DEFAULT NOW(),
	CONSTRAINT fk_clientes_transacoes_id
		FOREIGN KEY (cliente_id) REFERENCES cliente(id)
);


DO $$
BEGIN

INSERT INTO cliente(id, limite, saldo_atual, saldo_inicial) values
(1, 100000, 0, 0),
(2, 80000, 0, 0),
(3, 1000000, 0, 0),
(4, 10000000, 0, 0),
(5, 500000, 0, 0);

END;
$$
