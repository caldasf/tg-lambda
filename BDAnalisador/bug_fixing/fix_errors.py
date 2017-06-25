import csv
import os
import CreateInput

output_dir_base = '/home/luna/TG/tg-lambda/BDAnalisador/output/'
input_base = "/home/luna/TG/tg-lambda/BDAnalisador/input/"
static_jar = os.getcwd() + '/static2.jar'
projects_dir = '/home/luna/TG/java-projects/'



def find_project(project_name_key, sloc_fp):
    aFile = file(sloc_fp, "r")
    reader = csv.reader(aFile)
    for row in reader:
        projectName = row[0][:-4]
        if (projectName == project_name_key):
            return row[1]
    aFile.close()

    return False


def count_lines_code(run_static_file, temp_input_path):
    sloc_file_path = CreateInput.countLinesProjects(projects_dir, 'summary.csv')
    vet = [0 for i in xrange(500)]
    i = 0
    
    with open(temp_input_path, "r") as bFile:       
        projects = csv.reader(bFile, delimiter=";")
        for project in projects:
            vet[i] = find_project(project[2], sloc_file_path)
            i += 1
    bFile.close()   
    
    i = 0
    with open(temp_input_path, "r") as bFile:
        projects = csv.reader(bFile, delimiter=";")
        
        output = open (run_static_file, 'w')

        for project in projects:
            output.write("{};{};{};{};{};{};{};\n".format(project[0], 
                project[1], project[2],project[3], project[4], vet[i], project[6]))
            i += 1

    bFile.close() 
    output.close()

def is_non_zero_file(fpath):  
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0


def find_no_dir():
    day = 01
    month = 06
    year = 2017

    final_input = open("00_final.csv", "w")
    debug_file = open("00_debut.csv", "w")
    while (year > 2012):
        no_output_csv = open("00_no_dir.csv", "w")
        date_before = str(year) + '-' + str(month) + '-' + str(day)
        if (month > 1):
            month -= 1
        else:
            month = 12
            year -= 1

        date_after = str(year) + '-' + str(month) + '-' + str(day)        
        print("after {} & before {}".format(date_after, date_before))

        month_input = input_base + 'input-' + date_after + '_' + date_before + '.csv'

        with open(month_input, "r") as bFile:
            projects = csv.reader(bFile, delimiter=";")
            for row in projects:

                final_input.write("{};{};{};{};{};{};{};\n".format(row[0], 
                    row[1], row[2], row[3], row[4],row[5],row[6]))

                dir_path = os.path.join(output_dir_base, row[2]+'-'+row[3])
                if not os.path.isdir(dir_path):
                    debug_file.write("{};{};{};{};{};{};{};\n".format(row[0], 
                        row[1], row[2], row[3], row[4], row[5],row[6]))

                    if (row[5] != "False"):
                        if (int(row[5]) > 0):
                            no_output_csv.write("{};{};{};{};{};{};{};\n".format(row[0], 
                                row[1], row[2], row[3], row[4], row[5],row[6]))


        bFile.close()
        no_output_csv.close()
        # if (is_non_zero_file("00_no_dir.csv")):    
            
        run_static("00_no_dir.csv") 


def run_static_analysis(run_static_file):
    os.system('java -jar {} {}'.format(static_jar, run_static_file))

def run_static(fp_input):
    static_file = "run_static.csv"

    current_dir = os.getcwd()
    if (is_non_zero_file(fp_input)):
        with open(fp_input, "r") as bFile:
            projects = csv.reader(bFile, delimiter=";")
            for row in projects:
                print ("{} -> {} \n".format(row[4], row[3]))
                os.chdir(row[4])
                os.system("rm -r *")
                os.system("git archive --format=tar  {} | tar xf -".format(row[3]))

        bFile.close()

        os.chdir(current_dir)
        #count_lines_code("run_static.csv", fp_input)
        run_static_analysis(fp_input)



def main():
    find_no_dir()

if __name__ == '__main__':
    main()