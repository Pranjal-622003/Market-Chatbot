import sqlite3

# Connection
connection = sqlite3.connect("clothing.db")

# Creating cursor
cursor = connection.cursor()

# Create the table
table_info = """
CREATE TABLE t_shirts (
    t_shirt_id INTEGER PRIMARY KEY,
    brand TEXT CHECK (brand IN ('Van Huesen', 'Levi', 'Nike', 'Adidas')) NOT NULL,
    color TEXT CHECK (color IN ('Red', 'Blue', 'Black', 'White')) NOT NULL,
    size TEXT CHECK (size IN ('XS', 'S', 'M', 'L', 'XL')) NOT NULL,
    price INTEGER CHECK (price BETWEEN 10 AND 50),
    stock_quantity INTEGER NOT NULL,
    UNIQUE (brand, color, size)
);

-- Create the discounts table
CREATE TABLE discounts (
    discount_id INTEGER PRIMARY KEY,
    t_shirt_id INTEGER NOT NULL,
    pct_discount DECIMAL(5,2) CHECK (pct_discount BETWEEN 0 AND 100),
    FOREIGN KEY (t_shirt_id) REFERENCES t_shirts(t_shirt_id)
);

-- Create a trigger to populate the t_shirts table
CREATE TRIGGER PopulateTShirts AFTER INSERT ON t_shirts
BEGIN
    INSERT INTO t_shirts (brand, color, size, price, stock_quantity)
    SELECT
        CASE (1 + CAST(RANDOM() * 4 AS INTEGER))
            WHEN 1 THEN 'Van Huesen'
            WHEN 2 THEN 'Levi'
            WHEN 3 THEN 'Nike'
            ELSE 'Adidas'
        END,
        CASE (1 + CAST(RANDOM() * 4 AS INTEGER))
            WHEN 1 THEN 'Red'
            WHEN 2 THEN 'Blue'
            WHEN 3 THEN 'Black'
            ELSE 'White'
        END,
        CASE (1 + CAST(RANDOM() * 5 AS INTEGER))
            WHEN 1 THEN 'XS'
            WHEN 2 THEN 'S'
            WHEN 3 THEN 'M'
            WHEN 4 THEN 'L'
            ELSE 'XL'
        END,
        CAST(10 + RANDOM() * 41 AS INTEGER),
        CAST(10 + RANDOM() * 91 AS INTEGER)
    FROM t_shirts
    LIMIT 100 - (SELECT COUNT(*) FROM t_shirts);
END;
"""

# Execute the SQL commands
cursor.executescript(table_info)

# Insert at least 10 records into the discounts table
discounts_data = [
    (1, 10.00),
    (2, 15.00),
    (3, 20.00),
    (4, 5.00),
    (5, 25.00),
    (6, 10.00),
    (7, 30.00),
    (8, 35.00),
    (9, 40.00),
    (10, 45.00)
]

# Insert discount records
cursor.executemany("INSERT INTO discounts (t_shirt_id, pct_discount) VALUES (?, ?)", discounts_data)

# Commit changes and close connection
connection.commit()
connection.close()
