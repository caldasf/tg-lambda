SELECT DISTINCT P.Nome, P.idProjeto, M.idMetodo, M.qtdLambda
FROM Projeto P, Versao V, Classe C, Metodo M 
WHERE P.idProjeto = V.idProjeto 
	AND C.idVersao = V.idVersao
	AND M.idClasse = C.idClasse
	AND P.idProjeto = 7
	AND (M.qtdLambda > 0);

SELECT count(C.idClasse) FROM Projeto P, Versao V, Classe C, Metodo M WHERE P.idProjeto = V.idProjeto 
	AND C.idVersao = V.idVersao
	AND M.idClasse = C.idClasse
	AND P.idProjeto = 7 ;	

SELECT DISTINCT P.Nome
FROM Projeto P, Versao V, Classe C, Metodo M 
WHERE P.idProjeto = V.idProjeto 
	AND C.idVersao = V.idVersao;