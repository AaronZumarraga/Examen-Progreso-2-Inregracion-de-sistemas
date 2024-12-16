CREATE DATABASE RESTServiceDB;

USE RESTServiceDB;

CREATE TABLE reservations (
    reservation_id INT IDENTITY(1,1) PRIMARY KEY,
    room_number INT,
    customer_name NVARCHAR(100),
    start_date DATE,
    end_date DATE,
    status NVARCHAR(20)
);

-- Datos de prueba iniciales
INSERT INTO reservations (room_number, customer_name, start_date, end_date, status)
VALUES 
(101, 'John Doe', '2024-12-20', '2024-12-22', 'Activa');
