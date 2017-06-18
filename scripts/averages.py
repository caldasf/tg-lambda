#!/usr/bin/python


import MySQLdb
import datetime
import csv

avg_file = "average_lambda.csv"

def calculate_average (qtd, n):
    if n != 0:
        return float(qtd/n)
    else:
        return 0

def average_per_project(project_file, project_name, project_id):
    fp = open(avg_file, "a")


    with open(project_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        qtd_lambda, qtd_aic, qtd_maps, qtd_filter = 0, 0, 0, 0
        n_lambda = 0.0
        n_maps = 0.0
        n_filter = 0.0
        n_aic = 0.0


        for row in reader:
            if int(row[5]) > 0:
                n_lambda += 1
            if int(row[6]) > 0:
                n_aic += 1
            if int(row[7]) > 0:
                n_maps += 1
            if int(row[8]) > 0:
                n_filter += 1

            qtd_lambda += int(row[5])
            qtd_aic += int(row[6])
            qtd_maps += int(row[7])
            qtd_filter += int(row[8])


    fp.write("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n".format(project_name, project_id, qtd_lambda, 
        qtd_aic, qtd_maps, qtd_filter, calculate_average(qtd_lambda, n_lambda),
        calculate_average(qtd_aic, n_aic),calculate_average(qtd_maps, n_maps), 
        calculate_average(qtd_filter, n_filter)))

    fp.close()
    f.close()

def check_integer(key):
    if key == "None" or key == None:
        return 0
    else:
        return key

def generate_projects_csv(cursor):
    cursor.execute("""
    SELECT DISTINCT p.Nome, p.idProjeto from Projeto p;
    """)

    projects = cursor.fetchall()

    for project in projects:
        print (project[0])

        project_name = project[0]
        project_id = project[1]

        proj_results = 'results/'+str(project[0])+'.csv'
        out = open(proj_results, 'w')

        out.write('Projeto, idProjeto, idVersao, Versao, Data, qtd_lambda, qtd_aic, qtd_maps, qtd_filter\n')

        cursor.execute("""
        SELECT DISTINCT  v.idVersao, v.numVersao, v.data
        from Versao v, Projeto p 
        where p.idProjeto = v.idProjeto 
        and v.idProjeto = %d group by v.data;
        """ % int(project[1]))

        versions = cursor.fetchall()

        for version in versions:
            cursor.execute("""
            SELECT SUM(m.qtdLambda), sum(m.qtdAic), sum(m.qtdMaps), sum(m.qtdFilter) 
            from Metodo m, Classe c where c.idVersao = %d and m.idClasse = c.idClasse;
            """ % int(version[0])) 

            quantities = cursor.fetchall()
            for q in quantities:

                out.write("{}, {}, {}, {}, {}, {}, {}, {}, {}\n".format(project[0], 
                    project[1], version[0], version[1], version[2], check_integer(q[0]),
                     check_integer(q[1]), check_integer(q[2]), check_integer(q[3])))

        out.close()

        average_per_project(proj_results, project_name, project_id)
            




def main():
    db = MySQLdb.connect(host="localhost", user="root", passwd="",
    db="BDAnalisador")
    
    fp = open(avg_file, "w")
    fp.write("project, id, qtdlambda, qtdaic, qtdmaps, qtdfilter, avg_lambda, avg_aic, avg_maps, avg_filter\n")
    fp.close()

    try:
        cursor = db.cursor()
        generate_projects_csv(cursor)

    finally:
        db.close()

if __name__ == '__main__':
    main()