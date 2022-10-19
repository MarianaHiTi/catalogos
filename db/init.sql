CREATE DATABASE catalogos;
use catalogos;

CREATE TABLE usuarios (
  id_usuario int(11) NOT NULL PRIMARY KEY,
  nombre_usuario VARCHAR(20),
  password_usuario VARCHAR(20)
);

CREATE TABLE catalogos (
  id_catalogo INT AUTO_INCREMENT PRIMARY KEY,
  nombre_catalogo VARCHAR(20),
  descripcion_catalogo VARCHAR(1000),
  archivo_catalogo LONGBLOB,
  archivo_nombre VARCHAR(100),
  usuario_catalogo VARCHAR(20)
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
