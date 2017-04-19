SELECT DISTINCT P.Nome, P.idProjeto, M.idMetodo, M.qtdLambda
FROM Projeto P, Versao V, Classe C, Metodo M 
WHERE P.idProjeto = V.idProjeto 
	AND C.idVersao = V.idVersao
	AND M.idClasse = C.idClasse
	AND P.idProjeto = 7
	AND (M.qtdLambda > 0);

SELECT count(C.idClasse) FROM Versao V, Classe C, Metodo M WHERE
	C.idVersao = V.idVersao
	AND M.idClasse = C.idClasse
	AND P.idProjeto = 7 ;	

SELECT DISTINCT P.Nome
FROM Projeto P, Versao V, Classe C, Metodo M 
WHERE P.idProjeto = V.idProjeto 
	AND C.idVersao = V.idVersao;

---------------------
-- Import
gunzip < BDAnalisador_data.sql.gz  | mysql -u root BDAnalisador

-- Export
mysqldump -u root -p BDAnalisador | gzip > BDAnalisador_data.sql.gz
