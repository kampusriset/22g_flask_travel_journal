-- Membuat database
CREATE DATABASE travel_journal;

-- Menggunakan database
USE travel_journal;

-- Tabel untuk menyimpan data user
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Tabel untuk menyimpan data perjalanan
CREATE TABLE travels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    place_name VARCHAR(255) NOT NULL,
    description TEXT,
    travel_date DATE,
    cost DECIMAL(10,2),
    rating INT DEFAULT 3,
    username VARCHAR(50),
    FOREIGN KEY (username) REFERENCES users(username)
);