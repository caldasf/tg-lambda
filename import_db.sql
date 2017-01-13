
DROP TABLE IF EXISTS Projeto;

CREATE TABLE Projeto
(
	idProjeto int NOT NULL, 
	nome VARCHAR(200),
	PRIMARY KEY (idProjeto)

);


CREATE TABLE Versao
(
	idVersao int NOT NULL,
	idProjeto int NOT NULL,
	nome VARCHAR(200),
	PRIMARY KEY (idVersao),
	FOREIGN KEY (idProjeto) REFERENCES Projeto(idProjeto)
);

CREATE TABLE Classe
(
	idClasse int NOT NULL,
	idProjeto int NOT NULL,
	nome VARCHAR(200),
	PRIMARY KEY (idClasse),
	FOREIGN KEY (idProjeto) REFERENCES Projeto(idProjeto)
);

CREATE TABLE Metodo
(
	idMetodo int NOT NULL,
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
