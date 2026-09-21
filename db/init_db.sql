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
    estado VARCHAR(30) NOT NULL,

    FOREIGN KEY (deporte_id) REFERENCES deportes(id)
);

CREATE TABLE if NOT EXISTS socios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    dni VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    telefono VARCHAR(20) NOT NULL
);

CREATE TABLE if NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    socio_id INT NOT NULL,
    cancha_id INT NOT NULL,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    precio_hora DECIMAL(10, 2) NOT NULL,
    estado VARCHAR(30) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (socio_id) REFERENCES socios(id),
    FOREIGN KEY (cancha_id) REFERENCES canchas(id)
);

-- EJEMPLO CON DATOS DE PRUEBA
INSERT INTO deportes (nombre) VALUES
    ('Futbol'),
    ('Basketball'),
    ('Tennis');

INSERT INTO canchas (nombre, deporte_id, precio_hora, estado) VALUES
    ('Cancha 1', 1, 100.00, 'Disponible'),
    ('Cancha 2', 1, 120.00, 'Disponible'),
    ('Cancha 3', 2, 80.00, 'Disponible'),
    ('Cancha 4', 3, 90.00, 'Disponible');

INSERT INTO socios (nombre, apellido, dni, email, telefono) VALUES
    ('Carlos', 'Gomez', '12345678', 'carlos.gomez@example.com', '123456789'),
    ('Maria', 'Lopez', '23456789', 'maria.lopez@example.com', '987654321'),
    ('Juan', 'Perez', '34567890', 'juan.perez@example.com', '112233445');

INSERT INTO reservas
    (socio_id, cancha_id, fecha, hora_inicio, hora_fin, precio_hora, estado)
VALUES
    (1, 1, '2026-09-21', '10:00:00', '11:00:00', 100.00, 'Confirmada'),
    (1, 2, '2026-09-22', '14:00:00', '15:30:00', 120.00, 'Confirmada'),
    (2, 3, '2026-09-23', '18:00:00', '19:00:00', 80.00, 'Confirmada'),
    (3, 4, '2026-09-24', '16:00:00', '17:00:00', 90.00, 'Cancelada');