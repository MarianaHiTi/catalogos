CREATE DATABASE catalogos;
use catalogos;

CREATE TABLE user_type (
  id_type int(11) AUTO_INCREMENT PRIMARY KEY,
  type_description VARCHAR(20)
);


CREATE TABLE users (
  id_user int(11) AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50),
  password VARCHAR(80),
  first_name VARCHAR(30),
  second_name VARCHAR(30),
  user_type int(11),
  FOREIGN KEY(user_type) REFERENCES user_type(id_type)
);

CREATE TABLE catalogs (
  id_catalog int(11) AUTO_INCREMENT PRIMARY KEY,
  catalog_name VARCHAR(50),
  catalog_description VARCHAR(1000),
  file LONGBLOB,
  filename VARCHAR(50),
  id_user int(11) NOT NULL,
  FOREIGN KEY(id_user) REFERENCES users(id_user)
);

INSERT INTO user_type
  (type_description)
VALUES
  ("Admin");

INSERT INTO user_type
  (type_description)
VALUES
  ("Normal");

INSERT INTO users
  (id_user, username, password, first_name, second_name, user_type)
VALUES
  (1, "admin", "aad0ef68340263392332ec8ed8bd8166", "Admin", "Admin",1);

INSERT INTO users
  (id_user, username, password, first_name, second_name, user_type)
VALUES
  (2, "mariana", "5b9dc1ca6c4160be36ad121ab0cf7331", "Mariana", "Hinojosa",2);

INSERT INTO users
  (id_user, username, password, first_name, second_name, user_type)
VALUES
  (3, "fher", "351b5579d6de6fbf9bd5b8053f4347d4", "Fher", "Torres",2);

