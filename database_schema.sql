-- =========================================
-- INVENTORY MANAGEMENT SYSTEM DATABASE
-- =========================================
-- Author: Your Name
-- Description: Complete database schema + queries

-- =========================================
-- CREATE DATABASE
-- =========================================

CREATE DATABASE IF NOT EXISTS inventory_management_system;
USE inventory_management_system;

-- =========================================
-- USERS TABLE
-- =========================================

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'staff') DEFAULT 'staff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- CATEGORIES TABLE
-- =========================================

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default categories
INSERT INTO categories (name, description) VALUES
('Electronics', 'Electronic items'),
('Machinery', 'Machines and equipment'),
('Raw Materials', 'Basic materials'),
('Packaging', 'Packaging items'),
('Tools', 'Tools and instruments');

-- =========================================
-- PRODUCTS TABLE
-- =========================================

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    sku VARCHAR(50) UNIQUE NOT NULL,
    category_id INT,
    quantity INT DEFAULT 0,
    unit VARCHAR(30) DEFAULT 'pcs',
    price DECIMAL(10,2),
    reorder_level INT DEFAULT 10,
    location VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- =========================================
-- TRANSACTIONS TABLE
-- =========================================

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    type ENUM('IN', 'OUT'),
    quantity INT NOT NULL,
    reference VARCHAR(100),
    supplier_customer VARCHAR(150),
    note TEXT,
    user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- =========================================
-- USER QUERIES
-- =========================================

-- View all users
SELECT * FROM users;

-- View users with selected fields
SELECT id, username, email, role, created_at FROM users;

-- View Admin users
SELECT id, username, email FROM users WHERE role = 'admin';

-- View Staff users
SELECT id, username, email FROM users WHERE role = 'staff';

-- =========================================
-- PRODUCT & INVENTORY QUERIES
-- =========================================

-- View all products with category
SELECT 
    p.name, 
    p.sku, 
    c.name AS category, 
    p.quantity, 
    p.price
FROM products p
JOIN categories c ON p.category_id = c.id;

-- Low stock products
SELECT 
    name, 
    quantity, 
    reorder_level
FROM products
WHERE quantity <= reorder_level;

-- Total inventory value
SELECT 
    SUM(quantity * price) AS total_value
FROM products;

-- =========================================
-- TRANSACTION QUERIES
-- =========================================

-- Transactions history
SELECT 
    t.id, 
    p.name, 
    t.type, 
    t.quantity, 
    t.created_at
FROM transactions t
JOIN products p ON t.product_id = p.id
ORDER BY t.created_at DESC;

-- Transactions with user details
SELECT 
    t.id,
    p.name AS product_name,
    t.type,
    t.quantity,
    u.username,
    u.role,
    t.created_at
FROM transactions t
JOIN products p ON t.product_id = p.id
JOIN users u ON t.user_id = u.id
ORDER BY t.created_at DESC;

-- =========================================
-- ANALYTICS QUERIES
-- =========================================

-- Stock movement by category
SELECT 
    c.name AS category, 
    t.type, 
    SUM(t.quantity) AS total
FROM transactions t
JOIN products p ON t.product_id = p.id
JOIN categories c ON p.category_id = c.id
GROUP BY c.name, t.type;

-- Stock movement by category + user role
SELECT 
    c.name AS category,
    u.role,
    t.type,
    SUM(t.quantity) AS total
FROM transactions t
JOIN products p ON t.product_id = p.id
JOIN categories c ON p.category_id = c.id
JOIN users u ON t.user_id = u.id
GROUP BY c.name, u.role, t.type;

-- Admin vs Staff activity
SELECT 
    u.role,
    COUNT(t.id) AS total_transactions
FROM transactions t
JOIN users u ON t.user_id = u.id
GROUP BY u.role;
