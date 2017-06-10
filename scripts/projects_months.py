#!/usr/bin/python


import MySQLdb
import datetime
import csv


def generate_projects_csv(cursor):
    cursor.execute("""
    SELECT DISTINCT p.Nome, p.idProjeto from Projeto p;
    """)

    projects = cursor.fetchall()

    for project in projects:
        out = open('results/'+str(project[0])+'.csv', 'w')

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
                    project[1], version[0], version[1], version[2], q[0], q[1], q[2], q[3]))

        out.close()
            




def main():
    db = MySQLdb.connect(host="localhost", user="root", passwd="",
    db="BDAnalisador")
    
    try:
        cursor = db.cursor()
        generate_projects_csv(cursor)

    finally:
        db.close()

if __name__ == '__main__':
    main()