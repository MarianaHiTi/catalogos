CREATE DATABASE catalogos;
use catalogos;

CREATE TABLE usuarios (
  id_usuario int(11) NOT NULL,
  nombre_usuario VARCHAR(20),
  password_usuario VARCHAR(20)
);

INSERT INTO usuarios
  (id_usuario, nombre_usuario, password_usuario)
VALUES
  (1, "admin", "admin123");

INSERT INTO usuarios
  (id_usuario, nombre_usuario, password_usuario)
VALUES
  (2, "mariana", "mariana123");

INSERT INTO usuarios
  (id_usuario, nombre_usuario, password_usuario)
VALUES
  (3, "fher", "fher123");