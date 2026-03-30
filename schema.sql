-- Schema gerado automaticamente do inventario_v2.xlsx
-- 138 produtos | 10 categorias

PRAGMA foreign_keys = ON;

CREATE INDEX idx_movimentacoes_criado ON movimentacoes(criado_em)
CREATE INDEX idx_movimentacoes_produto ON movimentacoes(produto_id)
CREATE INDEX idx_produtos_categoria ON produtos(categoria_id)
CREATE TABLE categorias (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT NOT NULL UNIQUE,
    criado_em   TEXT NOT NULL DEFAULT (datetime('now','localtime'))
)
CREATE TABLE estoque (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id      INTEGER NOT NULL UNIQUE REFERENCES produtos(id),
    quantidade      REAL    NOT NULL DEFAULT 0,
    atualizado_em   TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
)
CREATE TABLE movimentacoes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id      INTEGER NOT NULL REFERENCES produtos(id),
    tipo            TEXT    NOT NULL CHECK(tipo IN ('entrada','saida','ajuste')),
    quantidade      REAL    NOT NULL CHECK(quantidade > 0),
    observacao      TEXT,
    criado_em       TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
)
CREATE TABLE produtos (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    sku             TEXT NOT NULL UNIQUE,
    descricao       TEXT NOT NULL,
    categoria_id    INTEGER NOT NULL REFERENCES categorias(id),
    unidade_medida  TEXT NOT NULL,
    estoque_minimo  REAL NOT NULL DEFAULT 0,
    ativo           INTEGER NOT NULL DEFAULT 1 CHECK(ativo IN (0,1)),
    criado_em       TEXT NOT NULL DEFAULT (datetime('now','localtime')),
    atualizado_em   TEXT NOT NULL DEFAULT (datetime('now','localtime'))
)
CREATE TABLE sqlite_sequence(name,seq)
CREATE TRIGGER trg_movimentacao_ajuste
AFTER INSERT ON movimentacoes
WHEN NEW.tipo = 'ajuste'
BEGIN
    INSERT INTO estoque (produto_id, quantidade)
    VALUES (NEW.produto_id, NEW.quantidade)
    ON CONFLICT(produto_id) DO UPDATE
    SET quantidade = NEW.quantidade,
        atualizado_em = datetime('now','localtime');
END
CREATE TRIGGER trg_movimentacao_entrada
AFTER INSERT ON movimentacoes
WHEN NEW.tipo = 'entrada'
BEGIN
    INSERT INTO estoque (produto_id, quantidade)
    VALUES (NEW.produto_id, NEW.quantidade)
    ON CONFLICT(produto_id) DO UPDATE
    SET quantidade = quantidade + NEW.quantidade,
        atualizado_em = datetime('now','localtime');
END
CREATE TRIGGER trg_movimentacao_saida
AFTER INSERT ON movimentacoes
WHEN NEW.tipo = 'saida'
BEGIN
    INSERT INTO estoque (produto_id, quantidade)
    VALUES (NEW.produto_id, -NEW.quantidade)
    ON CONFLICT(produto_id) DO UPDATE
    SET quantidade = quantidade - NEW.quantidade,
        atualizado_em = datetime('now','localtime');
END
