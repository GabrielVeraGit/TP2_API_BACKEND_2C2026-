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
    precio_hora DECIMAL(10, 2) NOT NULL,
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
    cancha_id INT NOT NULL,                 -- cliente (manda la ISO 8601) -> API (la descompone) -> DB (recibe) ,nunca se guarda la ISO literal como str. 
    fecha_hora_inicio DATETIME(6) NOT NULL, -- DB (manda formateando) -> API -> cliente (recibe la ISO como en el contrato)
    fecha_hora_fin DATETIME(6) NOT NULL,    -- ej '2026-10-15 18:00:00.000000' 'DATE TIME(6)' instruccion SELECT DATE_FORMAT(fecha_hora_prueba, '%Y-%m-%dT%H:%i:%s.%f-03:00') retorna ISO 8601
    estado VARCHAR(30) NOT NULL,
    precio_hora DECIMAL(10, 2) NOT NULL,
    precio_total DECIMAL(10, 2) NOT NULL,
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
    ('Cancha 1', 1, 100.00),
    ('Cancha 2', 1, 120.00),
    ('Cancha 3', 2, 80.00),
    ('Cancha 4', 3, 90.00);

INSERT INTO socios (nombre, email) VALUES
    ('Carlos Gomez', 'carlos.gomez@example.com'),
    ('Maria Lopez', 'maria.lopez@example.com'),
    ('Juan Perez', 'juan.perez@example.com');

INSERT INTO reservas
    (socio_id, cancha_id, fecha_hora_inicio, fecha_hora_fin, estado, precio_hora, precio_total)
VALUES
    (1, 1, '2026-09-21 10:00:00', '2026-09-21 12:00:00', 'Confirmada', 100.00, 200.00),
    (1, 2, '2026-09-22 14:00:00', '2026-09-22 15:00:00', 'Confirmada', 120.00, 120.00),
    (2, 3, '2026-09-23 18:00:00', '2026-09-23 21:00:00', 'Confirmada', 80.00, 240.00),
    (3, 4, '2026-09-24 16:00:00', '2026-09-24 17:00:00', 'Cancelada', 90.00, 90.00);

-- SELECT socio_id, cancha_id, estado, precio_hora, precio_total,
-- DATE_FORMAT(fecha_hora_inicio, '%Y-%m-%dT%H:%i:%s.%f-03:00') AS fecha_hora_inicio,
-- DATE_FORMAT(fecha_hora_fin, '%Y-%m-%dT%H:%i:%s.%f-03:00') AS fecha_hora_fin
-- FROM reservas;
-- obtenemos lo q el contrato pide