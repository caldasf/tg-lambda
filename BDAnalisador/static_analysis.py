#!/usr/bin/python
#
#  Script to automatically get last commit of each project
#  for each month until early 2013 and run static_analysis
#  project over it and then generate the output folders.
#
#  Execute:
#  python static_analysis.py <option> -path <projects_path>
#
#  When <options> are not defined, it runs everything. If options are defined:
#    --reset
#    --add
#    --all


import csv
import os
import shutil
import sys
from create_input import CreateInput
from subprocess import call


fname = os.getcwd() + '/input_temp.csv'
inputs_path = os.getcwd() + '/input/'
output_path = os.getcwd() + '/output/'
projects_dir = ''

# jar with static analysis
static_jar = os.getcwd() + '/static2.jar'
final_input = os.getcwd() + "/input.csv"


############################################################################


def run_static_analysis(month_input_path):
    os.system('java -jar {} {}'.format(static_jar, month_input_path))


def add_final_input(month_input):
    output = open(final_input, 'a')

    with open(month_input, "r") as bFile:
        projects = csv.reader(bFile, delimiter=";")

        for row in projects:
            # print row
            output.write("{};{};{};{};{};{};{};\n".format(row[0],
                        row[1], row[2], row[3], row[4], row[5], row[6]))

    output.close()


def find_project(project_name_key, sloc_fp):
    aFile = file(sloc_fp, "r")
    reader = csv.reader(aFile)

    for row in reader:
        projectName = row[0][:-4]
        if (projectName == project_name_key):
            if (row[1] != None and row[1] != "None"):
                return row[1]
            else:
                return 0
    aFile.close()

    return False


def count_lines_code(month_input_path, temp_input_path, create_obj):

    sloc_file_path = create_obj.count_code_lines()
    print sloc_file_path
    vet = [0 for i in xrange(500)]
    i = 0

    with open(temp_input_path, "r") as bFile:
        projects = csv.reader(bFile, delimiter=";")
        for project in projects:
            vet[i] = find_project(project[2], sloc_file_path)
            print vet[i]
            i += 1
    bFile.close()

    i = 0
    with open(temp_input_path, "r") as bFile:
        projects = csv.reader(bFile, delimiter=";")

        output = open(month_input_path, 'w')

        for project in projects:
            output.write("{};{};{};{};{};{};{};\n".format(project[0],
                    project[1], project[2], project[3], project[4], 
                    vet[i], project[6]))
            i += 1

    bFile.close()
    output.close()


def is_non_zero_file(fpath):
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0


def change_input(date_after, date_before, create_obj):
    global projects_dir


    month_input = "{}input-{}_{}.csv".format(inputs_path, date_after, date_before)
    temp_input_path = os.getcwd() + "/temp1.csv"

    with open(fname, "r") as aFile:
        projects = csv.reader(aFile, delimiter=";")
        working_dir_saved = os.getcwd()
        temp_input_file = open(temp_input_path, 'w')  # temp file for sloc

        for project in projects:
            path_project = os.path.join(projects_dir, project[4])
            # print "==========  {}  =========".format(path_project)

            # change working directory to project directory
            os.chdir(path_project)
            temp_result_path = os.path.join(path_project, 'temp.csv')
            os.system('git log --after="{}" --before="{}" -1 \
                --date=format:"%Y-%m-%d" --pretty=format:"%H, %an, %cd, %s" > {}\
                '.format(date_after, date_before, temp_result_path))

            if (is_non_zero_file(temp_result_path)):
                # print temp_result_path
                f = open(temp_result_path, 'rt')
                git_temp_rows = csv.reader(f)

                for row in git_temp_rows:
                    project[3] = row[0]

                temp_input_file.write("{};{};{};{};{};{};{};\n".format(project[0],
                            project[1], project[2], project[3], project[4], project[5], 
                            row[2]))

                f.close()

                os.system("rm -r *")
                os.system(
                    "git archive --format=tar  {} | tar xf -".format(project[3]))

        aFile.close()

    os.chdir(working_dir_saved)
    temp_input_file.close()

    count_lines_code(month_input, temp_input_path, create_obj)
    run_static_analysis(month_input)
    add_final_input(month_input)

    os.remove(temp_input_path)


def version_control(create_obj):
    day = 01
    month = 06
    year = 2017

    while (year > 2016): 
        date_before = str(year) + '-' + str(month) + '-' + str(day)

        if (month > 1):
            month -= 1
        else:
            month = 12
            year -= 1

        date_after = str(year) + '-' + str(month) + '-' + str(day)
        print("after {} & before {}".format(date_after, date_before))

        change_input(date_after, date_before, create_obj)

    os.remove(fname)


def reset():
    output = open(final_input, 'w')
    output.close()

    if (os.path.isdir(inputs_path)):
        shutil.rmtree(inputs_path)

    if (os.path.isdir(output_path)):
        shutil.rmtree(output_path)


def check_args(myargs):
    i = 0
    try:
        for arg in sys.argv:
            if (arg == '--path'):
                myargs["dir_path"] = sys.argv[i + 1]
            elif (arg == '--reset'):
                reset()
            
            elif (arg == '--add'):
                pass
            elif (arg == '--all' or (('--add' not in sys.argv)
                                     and ('--reset' not in sys.argv))):
                reset()
                myargs["run_all"] = True

            i += 1
    except:
        print ("\nError: An unexpected error happened. Did you pass valid arguments?")

    return myargs


##########################################

def create_dir():
    if not os.path.exists(inputs_path):
        os.makedirs(inputs_path)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

def main():
    global projects_dir

    try:
        input = raw_input
    except NameError:
        pass

    myargs = {"dir_path": "",
              "lang": "Java",
              "stars": 200,
              "proj_count": 2,
              "run_all": False
              }

    myargs = check_args(myargs)
       
    try:
        if (os.path.isdir(myargs["dir_path"])):
            projects_dir = myargs["dir_path"]
            c = CreateInput(myargs["dir_path"], myargs["lang"],
                 myargs["proj_count"], myargs["stars"])
            if myargs["run_all"]:
                c.create()
            else:
                pass
            create_dir()
            version_control(c)

        else:
            raise IOError 
    except IOError:
        print("\nError: A directory path for projects should be provided.")


if __name__ == '__main__':
    main()
