CREATE SCHEMA catalog;
CREATE SCHEMA warehouse;
CREATE SCHEMA employees;
CREATE SCHEMA operations;


CREATE TABLE catalog.units
(
    id        serial PRIMARY KEY,
    code      text,
    name      text,
    precision integer
);

CREATE TABLE catalog.products
(
    id          serial PRIMARY KEY,
    name        text,
    description text,
    unit_id     integer   NOT NULL,
    create_at   TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_products_units
        FOREIGN KEY (unit_id) REFERENCES catalog.units (id) ON DELETE RESTRICT
);

CREATE TABLE catalog.prices
(
    id         serial PRIMARY KEY,
    product_id integer   NOT NULL,
    price      numeric(18, 3),
    create_at  TIMESTAMP NOT NULL DEFAULT now(),
    CONSTRAINT fk_prices_products
        FOREIGN KEY (product_id) REFERENCES catalog.products ON DELETE RESTRICT
);



CREATE TABLE warehouse.stock_movements
(
    id             serial PRIMARY KEY,
    product_id     integer NOT NULL,
    quantity_delta numeric(18, 3),
    CONSTRAINT fk_stock_movements_products
        FOREIGN KEY (product_id) REFERENCES catalog.products (id) ON DELETE RESTRICT
);

CREATE TABLE warehouse.product_stocks
(
    product_id integer NOT NULL,
    quantity   numeric(18, 3),
    CONSTRAINT fk_product_stocks_products
        FOREIGN KEY (product_id) REFERENCES catalog.products (id) ON DELETE CASCADE
);



CREATE TABLE operations.transactions
(
    id        serial PRIMARY KEY,
--     employe_id INTEGER
    create_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE operations.goods_receipts
(
    id                serial PRIMARY KEY,
    transaction_id    INTEGER NOT NULL,
    stock_movement_id INTEGER NOT NULL,
    cost_price        NUMERIC(18, 3),
    CONSTRAINT fk_goods_receipts_transactions
        FOREIGN KEY (transaction_id) REFERENCES operations.transactions (id),
    CONSTRAINT fk_goods_receipts_stock_movement
        FOREIGN KEY (stock_movement_id) REFERENCES warehouse.stock_movements (id)
);

CREATE TABLE operations.supplier_returns
(
    add_stock_id      integer NOT NULL,
    transaction_id    integer NOT NULL,
    stock_movement_id integer NOT NULL,
    CONSTRAINT fk_supplier_returns_goods_receipts
        FOREIGN KEY (add_stock_id)
            REFERENCES operations.goods_receipts (id) ON DELETE RESTRICT,
    CONSTRAINT fk_supplier_returns_transactions
        FOREIGN KEY (transaction_id)
            REFERENCES operations.transactions (id) ON DELETE RESTRICT,
    CONSTRAINT fk_supplier_returns_stock_movements
        FOREIGN KEY (stock_movement_id)
            REFERENCES warehouse.stock_movements (id) ON DELETE RESTRICT
);

CREATE TABLE operations.revaluations
(
    price_id       integer NOT NULL,
    transaction_id integer NOT NULL,
    CONSTRAINT fk_revaluations_prices
        FOREIGN KEY (price_id) REFERENCES catalog.prices (id),
    CONSTRAINT fk_revaluations_transactions
        FOREIGN KEY (transaction_id) REFERENCES operations.transactions (id)
);

CREATE TABLE operations.write_offs
(
    stock_movement_id integer NOT NULL,
    transaction_id    integer NOT NULL,
    CONSTRAINT fk_write_offs_stock_movements
        FOREIGN KEY (stock_movement_id) REFERENCES warehouse.stock_movements (id),
    CONSTRAINT fk_write_offs_transactions
        FOREIGN KEY (transaction_id) REFERENCES operations.transactions (id)
);

CREATE TABLE operations.sales
(
    id                serial PRIMARY KEY,
    stock_movement_id integer NOT NULL,
    price_id          integer NOT NULL,
    transaction_id    integer NOT NULL,
    final_price       numeric(18, 3),
    CONSTRAINT fk_sales_stock_movements
        FOREIGN KEY (stock_movement_id)
            REFERENCES warehouse.stock_movements (id) ON DELETE RESTRICT,
    CONSTRAINT fk_sales_prices
        FOREIGN KEY (price_id)
            REFERENCES catalog.prices (id) ON DELETE RESTRICT,
    CONSTRAINT fk_sales_transactions
        FOREIGN KEY (transaction_id)
            REFERENCES operations.transactions (id) ON DELETE RESTRICT
);

CREATE TABLE operations.sale_returns
(
    sale_id           integer NOT NULL,
    stock_movement_id integer NOT NULL,
    transaction_id    integer NOT NULL,
    CONSTRAINT fk_sale_returns_sales
        FOREIGN KEY (sale_id)
            REFERENCES operations.sales (id) ON DELETE RESTRICT,
    CONSTRAINT fk_sale_returns_stock_movements
        FOREIGN KEY (stock_movement_id)
            REFERENCES warehouse.stock_movements (id) ON DELETE RESTRICT,
    CONSTRAINT fk_sale_returns_transactions
        FOREIGN KEY (transaction_id)
            REFERENCES operations.transactions (id) ON DELETE RESTRICT
);
