CREATE DATABASE lavandb;

USE lavandb;

CREATE TABLE vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicleNumber VARCHAR(255) NOT NULL,
    ownerName VARCHAR(255) NOT NULL,
    vehicleType VARCHAR(255) NOT NULL,
    imageUrl VARCHAR(255) NOT NULL
);
