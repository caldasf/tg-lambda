
DROP TABLE IF EXISTS Projeto;

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
	PRIMARY KEY (idVersao),
	FOREIGN KEY (idProjeto) REFERENCES Projeto(idProjeto)
);

CREATE TABLE Classe
(
	idClasse int NOT NULL AUTO_INCREMENT,
	idVersao int NOT NULL,
	nome VARCHAR(200),
	PRIMARY KEY (idClasse),
	FOREIGN KEY (idVersao) REFERENCES Versao(idVersao)
);

CREATE TABLE Metodo
(
	idMetodo int NOT NULL AUTO_INCREMENT,
	idClasse int NOT NULL,
	nome VARCHAR(200),
	QtdLambda int,
	QtdForEach int,
	QtdAic int,
	QtdFilter int,
	QtdMaps int,
	PRIMARY KEY (idMetodo),
	FOREIGN KEY (idClasse) REFERENCES Classe(idClasse)
);
