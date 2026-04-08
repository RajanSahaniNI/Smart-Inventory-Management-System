CREATE DATABASE inventory_db;
USE inventory_db;

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    quantity INT DEFAULT 0,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT
);

INSERT IGNORE INTO products (id, name, category, quantity, price, description) VALUES
(1, 'Laptop', 'Electronics', 15, 999.99, 'High performance laptop'),
(2, 'Smartphone', 'Electronics', 50, 599.99, 'Latest model smartphone'),
(3, 'Office Chair', 'Furniture', 30, 149.99, 'Ergonomic office chair'),
(4, 'Desk', 'Furniture', 10, 249.99, 'Wooden office desk'),
(5, 'Keyboard', 'Electronics', 100, 49.99, 'Mechanical keyboard');

CREATE TABLE sales_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    sale_month VARCHAR(7), -- YYYY-MM format
    quantity_sold INT,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

INSERT IGNORE INTO sales_history (product_id, sale_month, quantity_sold) VALUES
(1, '2023-01', 5), (1, '2023-02', 7), (1, '2023-03', 4), (1, '2023-04', 6), (1, '2023-05', 8),
(2, '2023-01', 20), (2, '2023-02', 15), (2, '2023-03', 25), (2, '2023-04', 22), (2, '2023-05', 30);


CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

insert into messages(id,name,email,message,timestamp) values(1,'Rajan','rajan@gmail.com','Hello',now());

