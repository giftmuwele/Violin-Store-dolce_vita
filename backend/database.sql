IF EXISTS(SELECT name FROM master.dbo.sysdatabases WHERE name = 'music_store')
DROP DATABASE music_store;
CREATE DATABASE music_store;
GO
USE music_store;
GO

-- ---------------------------------------------------
-- USERS TABLE
-- ---------------------------------------------------
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    google_id VARCHAR(255) UNIQUE,
    profile_pic VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- ---------------------------------------------------
-- PRODUCTS TABLE (CREATE BEFORE order_items)
-- ---------------------------------------------------
CREATE TABLE products (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10,2) NOT NULL,
    description TEXT,
    stock_quantity INT DEFAULT 0,
    image_url VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_category ON products(category);
CREATE INDEX idx_price ON products(price);


-- ---------------------------------------------------
-- CART TABLE (ONE CART PER USER)
-- ---------------------------------------------------
CREATE TABLE cart (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


-- ---------------------------------------------------
-- CART ITEMSTABLE
-- ---------------------------------------------------
CREATE TABLE cart_items (
    id INT IDENTITY(1,1) PRIMARY KEY,
    cart_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT DEFAULT 1,
    FOREIGN KEY (cart_id) REFERENCES cart(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    UNIQUE(cart_id, product_id)
);


-- ---------------------------------------------------
-- ORDERS TABLE
-- ---------------------------------------------------
CREATE TABLE orders (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'Completed',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE INDEX idx_user ON orders(user_id);


-- ---------------------------------------------------
-- ORDER ITEMS TABLE
-- ---------------------------------------------------
CREATE TABLE order_items (
    id INT IDENTITY(1,1) PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);
CREATE INDEX idx_order ON order_items(order_id);
CREATE INDEX idx_product ON order_items(product_id);
