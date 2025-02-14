CREATE DATABASE IF NOT EXISTS student_db;
USE student_db;
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    grade VARCHAR(50)
);

-- Insert Sample Data
INSERT INTO students (name, age, grade) VALUES 
    ('Alice Johnson', 14, '8th Grade'),
    ('Bob Smith', 13, '7th Grade'),
    ('Charlie Brown', 15, '9th Grade'),
    ('David White', 12, '6th Grade'),
    ('Emma Wilson', 14, '8th Grade'),
    ('Frank Green', 16, '10th Grade'),
    ('Grace Lee', 13, '7th Grade'),
    ('Henry Miller', 15, '9th Grade'),
    ('Ivy Carter', 12, '6th Grade'),
    ('Jack Turner', 14, '8th Grade');

CREATE TABLE auth (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(320) NOT NULL UNIQUE,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(512) NOT NULL,
    phone_number VARCHAR(20),
    role VARCHAR(50)
);

INSERT INTO auth (email, username, password_hash, phone_number, role)  
VALUES ('wbl@example.com', 'admin', 'wbl', '1234567890', 'admin');

