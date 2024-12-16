CREATE DATABASE InventoryServiceDB;

USE InventoryServiceDB;

CREATE TABLE rooms (
    room_id INT IDENTITY(1,1) PRIMARY KEY,
    room_number INT,
    room_type NVARCHAR(50),
    status NVARCHAR(20)
);

-- Datos de prueba iniciales
INSERT INTO rooms (room_number, room_type, status)
VALUES 
(101, 'Single', 'Disponible'),
(102, 'Double', 'Disponible');
