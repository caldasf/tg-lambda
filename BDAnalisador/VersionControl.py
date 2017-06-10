#!/usr/bin/python
# https://www.atlassian.com/git/tutorials/git-log


import csv
import os
from subprocess import call

import CreateInput 


#input that came from create_input.py
fname = os.getcwd() + '/input_temp.csv';

#preference folder where will save new inputs for static-analysis
inputs_location = os.getcwd() + '/input/';

#directory where all projects are
projects_dir = '/home/luna/TG/java-projects/'

#jat with static analysis
static_jar = os.getcwd() + '/static2.jar'


final_input = os.getcwd() + "/input.csv"

BDAnalisador = os.getcwd() + '/BDAnalisador.jar'

############################################################################

def runBDAnalisador(month_input_path):
	os.system('java -jar {}'.format(BDAnalisador))


def run_static_analysis(month_input_path):
	os.system('java -jar {} {}'.format(static_jar, month_input_path))


def add_final_input(month_input):
	output = open (final_input, 'a')

	with open(month_input, "r") as bFile:
		projects = csv.reader(bFile, delimiter=";")
		for row in projects:
			output.write("{};{};{};{};{};{};{};\n".format(row[0], 
				row[1], row[2], row[3], row[4], row[5],row[6]))			
	
	output.close()



def find_project(project_name_key, sloc_fp):
	aFile = file(sloc_fp, "r")
	reader = csv.reader(aFile)
	for row in reader:
		projectName = row[0][:-4]
		if (projectName == project_name_key):
			return row[1]
	aFile.close()

	return False


def count_lines_code(month_input_path, temp_input_path):
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
		
 		output = open (month_input_path, 'w')

 		for project in projects:
 			output.write("{};{};{};{};{};{};{};\n".format(project[0], 
 				project[1], project[2],project[3], project[4], vet[i], project[6]))
 			i += 1

 	bFile.close() 
 	output.close()



def is_non_zero_file(fpath):  
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0


def change_input(date_after, date_before):
	month_input = inputs_location + 'input-' + date_after + '_' + date_before + '.csv';
	temp_input_path = os.getcwd() + "/temp1.csv"

	with open(fname, "r") as aFile:
		projects = csv.reader(aFile, delimiter=";")
	
		working_dir_saved = os.getcwd()

		temp_input_file = open(temp_input_path, 'w') # temp file for sloc

		for project in projects:
			path_project = project[4]

			#change working directory to project directory
			os.chdir(path_project)
			os.system('git log --after="{}" --before="{}" -1 \
				--date=format:"%Y-%m-%d" --pretty=format:"%H, %an, %cd, %s" > temp.csv\
				'.format(date_after, date_before))
			
			#if log is not empty = exists a commit in this period   
			if (is_non_zero_file(path_project + 'temp.csv')):

				f = open('temp.csv', 'rt')
		  		git_temp_rows = csv.reader(f) # result from the git command


				for row in git_temp_rows:
					project[3] = row[0] #

				temp_input_file.write("{};{};{};{};{};{};{};\n".format(project[0], 
					project[1], project[2], project[3], project[4], project[5], row[2]))
			
				f.close()

				#change version of repository
				#os.system('git checkout '+ project[3] + ' .')
				os.system("rm -r *")
				os.system("git archive --format=tar  {} | tar xf -".format(project[3]))

		aFile.close()

	os.chdir(working_dir_saved)
	temp_input_file.close()	


	count_lines_code(month_input, temp_input_path)

	run_static_analysis(month_input)

	add_final_input(month_input)



def main():
	day = 01
	month = 06
	year = 2017

	while (year > 2012):

		date_before = str(year) + '-' + str(month) + '-' + str(day)

		if (month > 1):
			month -= 1
		else:
			month = 12
			year -= 1

		date_after = str(year) + '-' + str(month) + '-' + str(day)		
		print("after {} & before {}".format(date_after, date_before))

		change_input(date_after, date_before)
	
	# runBDAnalisador(final_input)



############################################################

output = open (final_input, 'w')
output.close()

#fname = CreateInput.main()

if __name__ == '__main__':
	main()