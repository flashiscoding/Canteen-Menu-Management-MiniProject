-- Run this in MySQL Workbench (File > Open SQL Script > Execute / lightning bolt)

CREATE DATABASE IF NOT EXISTS canteen_db;
USE canteen_db;

CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS menu_items (
    item_id     INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    price       DECIMAL(6,2) NOT NULL CHECK (price > 0),
    category_id INT NOT NULL,
    available   BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
        ON DELETE RESTRICT
);

INSERT IGNORE INTO categories (category_id, name) VALUES
    (1, 'Breakfast'), (2, 'Lunch'), (3, 'Snacks'), (4, 'Beverages');

INSERT INTO menu_items (name, price, category_id, available) VALUES
    ('Poha',          25.00, 1, TRUE),
    ('Veg Thali',     70.00, 2, TRUE),
    ('Samosa',        15.00, 3, TRUE),
    ('Masala Chai',   10.00, 4, TRUE),
    ('Cold Coffee',   40.00, 4, FALSE);

-- Handy query for your report/viva (JOIN):
-- SELECT m.item_id, m.name, m.price, c.name AS category, m.available
-- FROM menu_items m JOIN categories c ON m.category_id = c.category_id;
