#!/usr/bin/python
# Old script, not used

import pymysql
import datetime
import csv
import os

#	globals

projects_w_lambda = {}
qtd_lambda = 0
qtd_aic = 0
qtd_filter = 0
qtd_maps = 0





def updateQuantities(qtdLambda, qtdAic, qtdFilter, qtdMaps, restart_values):
	global  qtd_lambda
	global 	qtd_aic
	global	qtd_filter
	global	qtd_maps 
	if restart_values:
		qtd_lambda = 0
		qtd_aic = 0
		qtd_filter = 0
		qtd_maps = 0
	
	else:
		qtd_lambda += qtdLambda
		qtd_aic += qtdAic
		qtd_filter += qtdFilter
		qtd_maps += qtdMaps



def updateFile(proj_name, proj_ver, p_file, date, m_path):
	string_file = ("{}, {}, {}, {}, {}, {}, {} , \n".format(proj_name, proj_ver,qtd_lambda, qtd_aic, qtd_filter, qtd_maps, date ))
	p_file.write()



#####################################
# Get projects

def getProjectsLambda(cursor):

	cursor.execute("""
		SELECT DISTINCT p.Nome, v.idVersao, v.numVersao, v.data from Versao v, Projeto p 
		where p.idProjeto = v.idProjeto and v.idVersao = (select min(vr.idVersao) from Versao vr 
		where vr.idProjeto = v.idProjeto) 
		order by v.data desc;
		""")

	rows = cursor.fetchall()

	out = open('lambda_count.csv', 'w')
	out.write('Projeto, idVersao, Versao, Data, Qtd Metodos com Expressao Lambda' + '\n')

	print("Got the projects. \n")
	for row in rows:
		print ("{}, {}. \n".format(row[1], row[0]))
		res = cursor.execute("""
		SELECT count(m.idMetodo) from Metodo m, Classe c where c.idVersao = %d and c.idClasse = m.idClasse and m.qtdLambda > 0;
		""" % (row[1]))


		lambda_count = cursor.fetchone()

		# at least one method has lambda expression
		if (lambda_count[0] > 0):
			print (lambda_count[0])
			#save id version of each project with lambda
			projects_w_lambda[row[0]] = row[1]

			# save as csv
			#print (row[0] + ',' + str(row[1]) + ',' + str(row[2]) + ',' + str(row[3]) + ',' + str(lambda_count[0]))
			out.write(row[0] + ',' + str(row[1]) + ',' + str(row[2]) + ',' + str(row[3]) + ',' + str(lambda_count[0]) + '\n')


	out.close()




##################################
# For each project with lambda, get their monthly count of lambda & etc

def projectsByMonth(cursor):

	for vproject in projects_w_lambda:

		cursor.execute("""
		SELECT DISTINCT c.idClasse, c.Nome, m.qtdLambda, m.qtdAic, m.qtdFilter, m.QtdMaps, v.Data
		from Metodo m, Classe c, Versao v
		where m.idClasse = c.idClasse and c.idVersao = v.idVersao and v.idVersao = %d and m.qtdLambda > 0
		order by v.data;
		""" % int(projects_w_lambda[vproject]))

		rows = cursor.fetchall()

		prev_date = ''
		m_path = (str(vproject)+'.csv')
		monthly_file = open(m_path, 'w')

		
		for row in rows: 
			current_date = row[6].strftime("%Y-%m-%d")
			#print (current_date + ' = ' + prev_date + ': ' + )
########### finish here
			if (current_date == prev_date):
				updateQuantities(row[2], row[3], row[4], row[5], False)

			else:
				if prev_date != '':
					string_file = ("{}, {}, {}, {}, {}, {}, {} , \n".format(vproject, proj_ver,projects_w_lambda[vproject], qtd_aic, qtd_filter, qtd_maps, prev_date ))
					monthly_file.write()
				updateQuantities(row[2], row[3], row[4], row[5], True)
				updateQuantities(row[2], row[3], row[4], row[5], False)

			prev_date = current_date 

		monthly_file.close()

def openLambdaProject():
	with open('lambda_count.csv', 'r') as f:
		reader = csv.reader(f)
		count = 0
		for row in reader:
			if count == 0:
				count += 1
				pass
			else:
				projects_w_lambda[row[0]] = row[1]
	f.close()


##############################
def main():
	pymysql.install_as_MySQLdb()
	db = pymysql.connect(host="localhost", user="root", passwd="",
	db="BDAnalisador")
	
	try:

		cursor = db.cursor()
		getProjectsLambda(cursor)
		openLambdaProject()
		print (projects_w_lambda)
		#projectsByMonth(cursor)

	finally:
		db.close()

###########################

if __name__ == '__main__':
	main()