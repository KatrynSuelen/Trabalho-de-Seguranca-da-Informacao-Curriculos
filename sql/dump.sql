CREATE DATABASE sistema_curriculos;
use sistema_curriculos;
CREATE TABLE curriculo (
	id INT AUTO_INCREMENT NOT NULL,
    nome VARCHAR(255) NOT NULL,
    telefone VARCHAR(15),
    email VARCHAR(255) NOT NULL,
    site_url VARCHAR(255),
    experiencia_profissional TEXT NOT NULL,
    PRIMARY KEY (id)
);