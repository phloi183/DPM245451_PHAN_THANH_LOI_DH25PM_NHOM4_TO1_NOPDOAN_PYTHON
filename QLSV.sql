CREATE DATABASE QLSV
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE QLSV;

CREATE TABLE sinhvien (
    mssv INT PRIMARY KEY,
    holot VARCHAR(100),
    ten VARCHAR(50),
    phai VARCHAR(10),
    ngaysinh DATE,
    lop VARCHAR(50),
    khoa VARCHAR(100)
);
