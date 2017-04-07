#!/usr/bin/python
# https://www.atlassian.com/git/tutorials/git-log


import csv
import os
from subprocess import call

import CreateInput 


#input that came from create_input.py
fname = '/home/luna/workspace/static-analysis/input.csv';

#preference folder where will save new inputs for static-analysis
inputs_location = '/home/luna/TG/tg-lambda/BDAnalisador/input/';

#directory where all projects are
projects_dir = '/home/luna/TG/java-projects/'

#jat with static analysis
static_jar = '/home/luna/TG/tg-lambda/BDAnalisador/static2.jar'

############################################################################

def runStaticAnalysis(inputFile):
	os.system('java -jar ' + static_jar +' '+inputFile)


def changeLineCount(inputFile, tempFile):
	slocFile = CreateInput.countLinesProjects(projects_dir, 'summary.csv')
	vet = [0 for i in xrange(100)]

	i = 0 

	#open slocFile
	aFile = file(slocFile, "rt")
	reader = csv.reader(aFile)

	with open(tempFile, "r") as bFile:
		projects = csv.reader(bFile, delimiter=";")
		for row in reader:
		#open new input file
			for project in projects:
				projectName = row[0][:-4]
				if (projectName == project[2]):
					vet[i] = row[1]
					i += 1

	bFile.close() 	
 	
	with open(tempFile, "r") as bFile:
		projects = csv.reader(bFile, delimiter=";")

 		output = open (inputFile, 'w')
 		i = 0
 		for project in projects:
 			print vet[i]
 			output.write(project[0] + ';' + project[1] + ';' + project[2]+ ';' + project[3]+ ';' + project[4]+ ';' + vet[i] + '\n');
 			i += 1
 	bFile.close() 

 	output.close()

	aFile.close()




def is_non_zero_file(fpath):  
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0



def changeInput(date_after, date_before):
	
	newInput = inputs_location + 'input-' + date_after + '_' + date_before + '.csv';

	

	with open(fname, "r") as aFile:
		projects = csv.reader(aFile, delimiter=";")
	
		cwd = os.getcwd()

		newFile = open(cwd + 'temp1.csv', 'w');

		for project in projects:
			
			hash_version = ''
			path_project = project[4]

			#change working directory to project directory
			os.chdir(path_project)

			os.system('git log --after="' + date_after + '" --before="' + date_before +'" -1 --date=format:"%Y-%m-%d" > temp.csv')
			

			#if log is not empty = exists a commit in this period
   
			if (is_non_zero_file(path_project + 'temp.csv')):

				f = open('temp.csv', 'rt')
		  		temp = csv.reader(f)


				for row in temp:
					project[3] = row[0]

				#save new row in the new file
				newFile.write(project[0] + ';' + project[1] + ';' + project[2]+ ';' + project[3]+ ';' + project[4]+ ';' + project[5] + '\n');

				f.close()

				#change version of repository
				os.system('git checkout '+ project[3] + ' .')

		aFile.close()

		#remove(path_project + 'temp.csv')

	#return to previous working directory
	os.chdir(cwd)
	newFile.close()	


	#

	#change line count in the new input file
	changeLineCount(newInput, cwd + 'temp1.csv')

	#run static-analysis in new input file
	runStaticAnalysis(newInput)


def main ():


	date_after = '2017-1-1'
	date_before = '2017-2-1'

	day = 01
	month = 04
	year = 2017

	while (year > 2012):

		date_before = str(year) + '-' + str(month) + '-' + str(day)


		if (month > 1):
			month -= 1
		else:
			month = 12
			year -= 1

		date_after = str(year) + '-' + str(month) + '-' + str(day)
		
		print date_after + ' & ' + date_before
		changeInput(date_after, date_before)



main()

