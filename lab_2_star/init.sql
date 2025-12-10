<<<<<<< HEAD
-- init.sql без синтаксических ошибок
CREATE DATABASE IF NOT EXISTS app_db;

CREATE USER IF NOT EXISTS 'app_user'@'%' 
IDENTIFIED WITH mysql_native_password BY 'secure_app_pass'
REQUIRE NONE;

GRANT ALL PRIVILEGES ON app_db.* TO 'app_user'@'%';

FLUSH PRIVILEGES;

USE app_db;

CREATE TABLE IF NOT EXISTS analysis_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    sentiment VARCHAR(20) NOT NULL,
    probability FLOAT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
=======
CREATE DATABASE IF NOT EXISTS 2_app_db;
USE 2_app_db;

CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(10),
    value INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO items (name, value) VALUES 
('Item A', 15),
('Item B', 42),
('Item C', 77),
('Item D', 23),
('Item E', 56),
('Item F', 89),
('Item G', 34),
('Item H', 61);
>>>>>>> ca446489986f96836931b840444164ef50378bd6
