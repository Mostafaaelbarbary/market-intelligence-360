CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    country VARCHAR(50),
    created_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price NUMERIC(10,2)
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    quantity INT,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

INSERT INTO customers (customer_id, first_name, last_name, email, country, created_at) VALUES
(1, 'Alice', 'Johnson', 'alice@example.com', 'USA', NOW()),
(2, 'Bob', 'Smith', 'bob@example.com', 'UK', NOW()),
(3, 'Charlie', 'Brown', 'charlie@example.com', 'Canada', NOW());

INSERT INTO products (product_id, product_name, category, price) VALUES
(101, 'Laptop', 'Electronics', 1200.00),
(102, 'Headphones', 'Electronics', 150.00),
(103, 'Office Chair', 'Furniture', 300.00);

INSERT INTO orders (order_id, customer_id, product_id, quantity, order_date) VALUES
(1001, 1, 101, 1, CURRENT_DATE),
(1002, 1, 102, 2, CURRENT_DATE),
(1003, 2, 103, 1, CURRENT_DATE),
(1004, 3, 102, 1, CURRENT_DATE);