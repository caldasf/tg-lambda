#!/usr/bin/python
# https://www.atlassian.com/git/tutorials/git-log

import csv
import os
from subprocess import call

#input from static-analysis
fname = '/home/luna/workspace/static-analysis/input.csv';

def changeInput(newFile, date_after, date_before):
	
	with open(fname, "rt") as aFile:
		projects = csv.reader(aFile, delimiter=",")
	cwd = os.getcwd()

	for project in projects:
		
		hash_version = ''
		path_project = project[4]

		#change working directoryto rin git command
		os.chdir(path_project)
		os.system('git log --after="' + date_after + '" --before="' + date_before +'" -1 --pretty=format:"%H, %an, %cd, %s" | tee temp.csv')
			
		f = open('temp.csv', 'r')
	  	fp = csv.reader(f)

		linef = next(fp)
		project[3] = linef[0]

		#save new row in the 

		print linef
		print project

		f.close()

	aFile.close()

	#remove(path_project + 'temp.csv')

	#return to previous working 
	os.chdir(cwd)

def main ():
		date_after = '2017-1-1'
		date_before = '2017-2-1'


		changeInput('')

