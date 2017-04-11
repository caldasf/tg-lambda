
DROP DATABASE IF EXISTS BDAnalisador;
CREATE DATABASE BDAnalisador;
USE BDAnalisador;

CREATE TABLE Projeto
(
	idProjeto int NOT NULL AUTO_INCREMENT, 
	nome VARCHAR(200),
	PRIMARY KEY (idProjeto)

);


CREATE TABLE Versao
(
	idVersao int NOT NULL AUTO_INCREMENT,
	idProjeto int NOT NULL,
	numVersao VARCHAR(200),
	data datetime,
	PRIMARY KEY (idVersao)
--	FOREIGN KEY (idProjeto) REFERENCES Projeto(idProjeto)
);

CREATE TABLE Classe
(
	idClasse bigint NOT NULL AUTO_INCREMENT,
	idVersao int NOT NULL,
	nome VARCHAR(200),
	PRIMARY KEY (idClasse)
--	FOREIGN KEY (idVersao) REFERENCES Versao(idVersao)
);

CREATE TABLE Metodo
(
	idMetodo bigint NOT NULL AUTO_INCREMENT,
	idClasse bigint NOT NULL,
	nome VARCHAR(200),
	QtdLambda int,
	QtdForEach int,
	QtdAic int,
	QtdFilter int,
	QtdMaps int,
	linhaFim int,
	linhaInicio int,
	PRIMARY KEY (idMetodo)
--	FOREIGN KEY (idClasse) REFERENCES Classe(idClasse)
);
