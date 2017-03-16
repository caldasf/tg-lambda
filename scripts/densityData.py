#!/usr/bin/python
from __future__ import division

import MySQLdb
import datetime
import csv

#input from static-analysis
fname = '/home/luna/workspace/static-analysis/input.csv';

#projects name and lines count
projects = {}


with open(fname, "rt") as aFile:
	reader = csv.reader(aFile, delimiter=";")

	for row in reader:
		projects[row[2]] = row[5]

# open connection to database
# fill up with needed credentials


db = MySQLdb.connect(host="localhost", user="root", passwd="",
 db="BDAnalisador")


idProjeto = 1;

# # 
try:
	cursor = db.cursor() # cursor to manipulate database

	out = open('out.csv', 'w')
	out.write('Project;Total Lines; QtdLambda;Lambda Density;qtdAic;Aic Density;qtdFilter;Filter Density; qtdMaps; Maps Density\n')

 	for key,value in projects.items():

	# sql query
 		cursor.execute("""
 		SELECT DISTINCT P.Nome, P.idProjeto, M.idMetodo, M.qtdLambda, M.qtdAic, M.qtdFilter, M.qtdMaps
 		FROM Projeto P, Versao V, Classe C, Metodo M 
 		WHERE P.idProjeto = V.idProjeto 
 		AND C.idVersao = V.idVersao
 		AND M.idClasse = C.idClasse
 		AND P.idProjeto = %d
		AND (M.qtdLambda > 0 or M.qtdAic > 0 or M.qtdFilter > 0 or M.qtdMaps > 0);
		""" % (idProjeto))

 		

# 		#fetch | save the result
		rows = cursor.fetchall()

#			lambda # aic # filter # maps
		counting_totals =  [0, 0, 0, 0]
		counting_density = [0.0, 0.0, 0.0, 0.0 ]


 		for row in rows:
 			counting_totals[0] += row[3]
 			counting_totals[1] += row[4]
 			counting_totals[2] += row[5]
 			counting_totals[3] += row[6]

 		#aic bug
 		counting_totals[1] = counting_totals[1]/2.0
 		print value
 		#calc Density
 		counting_density[0] = (counting_totals[0]/float(value));
 		counting_density[1] = counting_totals[1]/float(value);
 		counting_density[2] = counting_totals[2]/float(value);
 		counting_density[3] = counting_totals[3]/float(value);


 		#write output
 		out.write('%s;%s;' % (rows[0][0], projects[rows[0][0]]))
 		out.write('%d;%d;' % (counting_totals[0], counting_density[0]))  #lambda
 		out.write('%d;%d;' % (counting_totals[1], counting_density[1])) #aic
 		out.write('%d;%d;' % (counting_totals[2], counting_density[2]))  #filter
 		out.write('%d;%d;' % (counting_totals[3], counting_density[3]))  #map
 		out.write('\n')

 		idProjeto += 1
 	#}


# ##########
##########

	out.close()
#close database
finally:
	db.close()