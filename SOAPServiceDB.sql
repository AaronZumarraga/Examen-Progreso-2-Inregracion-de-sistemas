CREATE DATABASE SOAPServiceDB;

USE SOAPServiceDB;

CREATE TABLE availability (
    room_id INT PRIMARY KEY,
    room_type NVARCHAR(50),
    available_date DATE,
    status NVARCHAR(20)
);

-- Datos de prueba iniciales
INSERT INTO availability (room_id, room_type, available_date, status)
VALUES 
(1, 'Single', '2024-12-20', 'Disponible'),
(2, 'Double', '2024-12-20', 'Disponible'),
(3, 'Suite', '2024-12-20', 'Mantenimiento');
