import psycopg2
import os

# URL de Render
RENDER_DB = "postgresql://postgres.inweyblldpimwkbfrffx:vx8HzscNNI9JLYYE@aws-1-sa-east-1.pooler.supabase.com:5432/postgres"

# SQL con los datos a importar
sql = """
SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

CREATE TABLE IF NOT EXISTS public.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    role VARCHAR(20),
    created_at TIMESTAMP,
    is_active BOOLEAN
);

CREATE TABLE IF NOT EXISTS public.products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    quantity INTEGER,
    purchase_price FLOAT NOT NULL,
    sale_price FLOAT NOT NULL,
    min_stock INTEGER,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    is_active BOOLEAN,
    image_url VARCHAR(500) DEFAULT '',
    code VARCHAR(50) DEFAULT ''
);

CREATE TABLE IF NOT EXISTS public.sales (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    total FLOAT,
    total_cost FLOAT,
    profit FLOAT,
    notes VARCHAR(200),
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public.sale_items (
    id SERIAL PRIMARY KEY,
    sale_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price FLOAT NOT NULL,
    purchase_price FLOAT NOT NULL,
    subtotal FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS public.deliveries (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    address VARCHAR(200) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    notes VARCHAR(300),
    total FLOAT,
    status VARCHAR(20),
    user_id INTEGER,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    estimated_time VARCHAR(20) DEFAULT '30 min'
);

CREATE TABLE IF NOT EXISTS public.cash_registers (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    opening_amount FLOAT,
    closing_amount FLOAT,
    sales_total FLOAT,
    expected FLOAT,
    difference FLOAT,
    notes VARCHAR(300),
    status VARCHAR(20),
    user_id INTEGER,
    created_at TIMESTAMP
);

INSERT INTO public.users (id, username, full_name, password_hash, role, created_at, is_active) VALUES
(1, 'admin', 'Administrador', 'scrypt:32768:8:1$EZ6vNLGgYIjLCukq$3d4607b9ec8a584b41b0d5ef38cdf0f79904e158c341ad5d8e5a7eeba4537409f9d8a2c4d5c39d593cde1faa47575f5943045b4e85d1da3b82f3d05743513c2e', 'admin', '2026-06-20 17:31:31.243684', true),
(2, 'empleado', 'Empleado', 'scrypt:32768:8:1$JSyyJyNzVnEHvsxK$bdf59205173d4f22a80e0c47e8343637bf50c40fa8170046451e946b94ee2c1eaf03c56a3e4f972d1e05fbcc729e40a6f51766faad0d18c7a74ec3d96bf83eed', 'empleado', '2026-06-20 17:31:31.296094', true)
ON CONFLICT (id) DO NOTHING;

INSERT INTO public.products (id, name, category, quantity, purchase_price, sale_price, min_stock, created_at, updated_at, is_active, image_url, code) VALUES
(1, 'Águila 330ml', 'Cerveza', 48, 1800, 2500, 12, '2026-06-20 17:31:31.303649', '2026-06-25 23:46:00.250716', true, 'https://tse2.mm.bing.net/th/id/OIP.T62eb31Hpib0V-1rLnlh2gHaHa?r=0&rs=1&pid=ImgDetMain&o=7&rm=3', ''),
(2, 'Club Colombia 330ml', 'Cerveza', 36, 2200, 3000, 12, '2026-06-20 17:31:31.303654', '2026-06-20 23:36:05.255671', true, 'https://tse4.mm.bing.net/th/id/OIP.6gx-c77nncthjE4Hnv6xmwAAAA?r=0&rs=1&pid=ImgDetMain&o=7&rm=3', ''),
(3, 'Poker 330ml', 'Cerveza', 60, 1700, 2200, 12, '2026-06-20 17:31:31.303655', '2026-06-20 23:36:21.204112', true, 'https://tse1.mm.bing.net/th/id/OIP.mqJlI6bvlyFOPtAvKVAA6wHaIB?r=0&rs=1&pid=ImgDetMain&o=7&rm=3', ''),
(4, 'Aguardiente Antioqueño 750ml', 'Aguardiente', 10, 22000, 30000, 5, '2026-06-20 17:31:31.303656', '2026-06-25 23:20:39.062999', true, 'https://resources.sears.com.mx/medios-plazavip/t1/176351387964ea8c0b0ca5438aaae8b95c5e1e3bae', ''),
(5, 'Aguardiente Nectar 750ml', 'Aguardiente', 8, 20000, 28000, 5, '2026-06-20 17:31:31.303657', '2026-06-20 23:35:23.36659', true, 'https://tse1.mm.bing.net/th/id/OIP.KFFdA1noDWd1aCr8ExHGUAHaHa?r=0&rs=1&pid=ImgDetMain&o=7&rm=3', ''),
(6, 'Ron Caldas 750ml', 'Ron', 6, 28000, 38000, 3, '2026-06-20 17:31:31.303658', '2026-06-20 23:37:09.149493', true, 'https://tse3.mm.bing.net/th/id/OIP.AH_QMxQzh9YNGrE1TMxRfwHaHa?r=0&rs=1&pid=ImgDetMain&o=7&rm=3', ''),
(7, 'Ron Medellín 750ml', 'Ron', 4, 30000, 42000, 3, '2026-06-20 17:31:31.303659', '2026-06-20 23:37:32.548663', true, 'https://tse4.mm.bing.net/th/id/OIP.HmZMTeCm-SLKnESUulGJoAHaHa?r=0&rs=1&pid=ImgDetMain&o=7&rm=3', ''),
(8, 'Whisky Old Parr 750ml', 'Whisky', 3, 85000, 120000, 2, '2026-06-20 17:31:31.30366', '2026-07-01 00:59:09.742755', true, 'https://bodegasalianza.vteximg.com.br/arquivos/ids/158193-1000-1000/3347-1.jpg?v=636167415839230000', ''),
(9, 'Vino Gato Negro Tinto', 'Vino', 5, 18000, 26000, 3, '2026-06-20 17:31:31.303661', '2026-06-20 23:38:42.622289', true, 'https://jumbocolombiafood.vteximg.com.br/arquivos/ids/3536989-1000-1000/7804300010638.jpg?v=637341419074970000', ''),
(10, 'Maní Tostado 100g', 'Snacks', 20, 1500, 2500, 10, '2026-06-20 17:31:31.303662', '2026-06-20 23:37:48.464456', true, 'https://tse2.mm.bing.net/th/id/OIP.laLvIzt5VUSS0Xy3tov76gHaHa?r=0&rs=1&pid=ImgDetMain&o=7&rm=3', ''),
(11, 'Papas Margarita 70g', 'Snacks', 15, 2000, 3000, 10, '2026-06-20 17:31:31.303663', '2026-06-20 23:38:22.745026', true, 'https://www.motelvenus.com.co/cdn/shop/products/papasnatural.webp?v=1674974349&width=1445', ''),
(12, 'Cigarrillos Marlboro', 'Otros', 10, 12000, 16000, 5, '2026-06-20 17:31:31.303664', '2026-06-20 23:36:47.645326', true, 'https://tse3.mm.bing.net/th/id/OIP.T3aVpOdGagQQbrucZOWIxwHaHa?r=0&rs=1&pid=ImgDetMain&o=7&rm=3', '')
ON CONFLICT (id) DO NOTHING;

SELECT setval('public.users_id_seq', 2, true);
SELECT setval('public.products_id_seq', 12, true);
SELECT setval('public.sales_id_seq', 13, true);
SELECT setval('public.sale_items_id_seq', 13, true);
SELECT setval('public.deliveries_id_seq', 6, true);
SELECT setval('public.cash_registers_id_seq', 1, false);
"""

try:
    conn = psycopg2.connect(RENDER_DB)
    cur  = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Base de datos importada correctamente en Render!")
except Exception as e:
    print(f"❌ Error: {e}")