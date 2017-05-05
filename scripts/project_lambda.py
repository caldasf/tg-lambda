#!/usr/bin/python


import MySQLdb
import datetime
import csv



db = MySQLdb.connect(host="localhost", user="root", passwd="",
	db="BDAnalisador")


try:
	cursor = db.cursor()

	cursor.execute("""
	SELECT DISTINCT p.Nome, v.idVersao, v.numVersao, v.data from Versao v, Projeto p 
	where p.idProjeto = v.idProjeto and v.idVersao = (select min(vr.idVersao) from Versao vr where vr.idProjeto = v.idProjeto) 
	order by v.data desc;
	""")

	rows = cursor.fetchall()

	for row in rows:
		res = cursor.execute("""
		SELECT count(m.qtdLambda)from Metodo m, Classe c where c.idVersao = %d and c.idClasse = m.idClasse
		""" % (row[1]))


		lambda_count = cursor.fetchone()

		if (lambda_count > 0):
			print row[0]



finally:
	db.close()