#!/usr/bin/python

import MySQLdb
import datetime
import csv
import os

results_path = os.getcwd() + "/results/"
method_path = os.getcwd() + "/method_size/"


def create_prject_list():
    avg_file = "average_lambda.csv"
    projects_dict = {}

    with open(avg_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            if int(row[2]) > 0:
                projects_dict[row[0]] = row[1]

    f.close()

    return projects_dict


def find_months(proj, id):
    result_file = os.path.join(results_path, proj + '.csv')
    month_dict = {}

    with open(result_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)

        month_dict["before"] = []
        for row in reader:
            if int(row[5]) == 0:
                month_dict["before"] = row
            elif int(row[5]) > 0:
                month_dict["after"] = row
                break

        return month_dict


def get_methods_size(cursor, version, flag):
    method_dict = {}
    method = None
    if flag:
        cursor.execute("""
        SELECT DISTINCT c.idClasse, c.Nome, m.idMetodo, m.Nome, m.linhaInicio, m.linhaFim 
        from Metodo m, Classe c 
        where m.idClasse = c.idClasse and c.idVersao = %d and m.qtdLambda > 0;
        """ % int(version[2]))

        methods = cursor.fetchall()
    
    elif flag == False and len(version) > 0:
        cursor.execute("""
        SELECT DISTINCT c.idClasse, c.Nome, m.idMetodo, m.Nome, m.linhaInicio, m.linhaFim 
        from Metodo m, Classe c 
        where m.idClasse = c.idClasse and c.idVersao = %d;
        """ % int(version[2]))

        methods = cursor.fetchall()

    else:
        return False

    for method in methods:
        method_dict[int(method[2])] = [
                                method[1], 
                                method[3], 
                                int(int(method[5]) - int(method[4])),
                                method[0],
                                method[2]
                                ]
    return method_dict


def add_project_file(after_list, before_list, project):
    out_file = os.path.join(method_path, project + ".csv")
    
    if os.path.isfile(out_file):
        fp = open(out_file, "a")
    else:
        fp = open(out_file, "w")
        fp.write("class, method, before_id, after_id, before_size, after_size\n")

    fp.write("{}, {}, {}, {}, {}, {}\n".format(after_list[0], 
        after_list[1], before_list[4], after_list[4], before_list[2], after_list[2]))


def verify_refactor(cursor):
    proj_dict = create_prject_list()

    for key in proj_dict:
        print ("\n\n"+key)
        months_dict = find_months(key, proj_dict[key])

        after_dict = get_methods_size(cursor, months_dict["after"], True)
        before_dict = get_methods_size(cursor, months_dict["before"], False)

        if before_dict:
            for after_id in after_dict:
                for before_id in before_dict:
                    if after_dict[after_id][0] == before_dict[before_id][0]:
                        if after_dict[after_id][1] == before_dict[before_id][1]:
                            if after_dict[after_id][2] < before_dict[before_id][2]:
                                add_project_file(after_dict[after_id], 
                                before_dict[before_id], key)
                                break



                        
                            






def main():
    db = MySQLdb.connect(host="localhost", user="root", passwd="",
                         db="BDAnalisador")

    try:
        cursor = db.cursor()
        verify_refactor(cursor)

    # except:
    #     print("Error: An unexpected error happened. \
    #         Possibly a database connection error?")

    finally:
        db.close()

if __name__ == '__main__':
    main()
