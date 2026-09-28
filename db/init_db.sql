CREATE DATABASE IF NOT EXISTS Club_Deportivo;

USE Club_Deportivo;

CREATE TABLE if NOT EXISTS deportes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE if NOT EXISTS canchas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    deporte_id INT NOT NULL,
    precio_hora INT NOT NULL,
    techada BOOLEAN NOT NULL DEFAULT FALSE,
    activa BOOLEAN NOT NULL DEFAULT TRUE, -- estado/activo, disponibilidad de poder reservar
    FOREIGN KEY (deporte_id) REFERENCES deportes(id)
);

CREATE TABLE if NOT EXISTS socios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE if NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    socio_id INT NOT NULL,
    cancha_id INT NOT NULL,                  
    fecha_hora_inicio DATETIME(6) NOT NULL, 
    fecha_hora_fin DATETIME(6) NOT NULL,    
    estado VARCHAR(30) NOT NULL,
    precio_hora INT NOT NULL,
    precio_total INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (socio_id) REFERENCES socios(id),
    FOREIGN KEY (cancha_id) REFERENCES canchas(id)
);

-- EJEMPLO CON DATOS DE PRUEBA
INSERT INTO deportes (nombre) VALUES
    ('Futbol'),
    ('Basketball'),
    ('Tennis');

INSERT INTO canchas (nombre, deporte_id, precio_hora) VALUES
    ('Cancha 1', 1, 1100000),
    ('Cancha 2', 1, 1200000),
    ('Cancha 3', 2, 1300000),
    ('Cancha 4', 2, 1400000),
    ('Cancha 5', 3, 1500000),
    ('Cancha 6', 3, 1600000);

INSERT INTO socios (nombre, email) VALUES
    ('Carlos Gomez', 'carlos.gomez@example.com'),
    ('Maria Lopez', 'maria.lopez@example.com'),
    ('Juan Perez', 'juan.perez@example.com'),
    ('Ana Gomez', 'ana.gomez@example.com'),
    ('Carlos Ruiz', 'carlos.ruiz@example.com'),
    ('Laura Torres', 'laura.torres@example.com'),
    ('Diego Fernandez', 'diego.fernandez@example.com'),
    ('Sofia Martinez', 'sofia.martinez@example.com');

INSERT INTO reservas
    (socio_id, cancha_id, fecha_hora_inicio, fecha_hora_fin, estado, precio_hora, precio_total)
VALUES
    (1, 1, '2026-09-28 10:00:00.000000', '2026-09-28 12:00:00.000000', 'confirmada', 1100000, 2200000),
    (1, 2, '2026-09-22 14:00:00.000000', '2026-09-22 15:00:00.000000', 'confirmada', 1200000, 1200000),
    (2, 3, '2026-09-23 18:00:00.000000', '2026-09-23 21:00:00.000000', 'confirmada', 1300000, 3900000),
    (3, 4, '2026-09-24 16:00:00.000000', '2026-09-24 17:00:00.000000', 'cancelada',  1400000, 1400000),
    (3, 5, '2026-09-24 13:00:00.000000', '2026-09-24 14:00:00.000000', 'finalizada', 1500000, 1500000),
    (6, 6, '2026-09-24 14:00:00.000000', '2026-09-24 15:00:00.000000', 'cancelada',  1600000, 1600000);

-- SELECT socio_id, cancha_id, estado, precio_hora, precio_total,
-- DATE_FORMAT(fecha_hora_inicio, '%Y-%m-%dT%H:%i:%s.%f-03:00') AS fecha_hora_inicio,
-- DATE_FORMAT(fecha_hora_fin, '%Y-%m-%dT%H:%i:%s.%f-03:00') AS fecha_hora_fin
-- FROM reservas;
-- obtenemos lo q el contrato pide