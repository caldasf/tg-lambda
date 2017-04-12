# 1. List repositories
# 2. Clone Repositories
# 3. Use sloc and save information
# 4. Create file


import requests
from os import system
from os import listdir, remove
from os.path import isdir, abspath
import csv
import os
from subprocess import call


lang = 'Java'
sumFile = 'summary.csv'


def gitToHttps(urlName):
	new_url = urlName[3:]
	new_url = 'https' + new_url
	return new_url

#List_repositories.py
def listRepositories ():
	prefix = 'https://api.github.com/search/repositories?q='
	suffix = '&sort=stars&order=desc&page='

	print '# Listing github projects to use #';
	lang     = raw_input('Language (java, cpp, python,...): ')
	stars    = raw_input('Min. number of stars: ')
	projects = input('Number of projects: ')
	outFile  = raw_input('Output file: ')

	lang  = '+language:' + lang 
	stars = 'stars:%3E'  + stars

	uri   = prefix + stars + lang + suffix


	print 'searching the github API'
	print 'query string:', uri

	response = requests.get(uri + '1')
	data = response.json()

	items = data['items']

	pagination = 0

	f = open(outFile, 'w')

	for item in items:
	#  line = item["name"] + ";" + item["size"] + ";" + item["watchers"] + ";" + item["forks"] + ";" + item["git_url"] + ";" + item["description"] 
	#  print(line)
		pagination += 1 

	pages = 1 + (projects // pagination)

	for i in range(1, pages):
		print uri + str(i + 1)
		response = requests.get(uri + str(i + 1))
		data = response.json()
		if(data.has_key('items')): 
			items = items + data['items']
		else: 
			print data
		break 

	count = 0   
	for item in items: 
		if(count < projects and item != None):
			
			line   = item.get("name", "-") + ","
			line  += str(item.get("size", "-")) + "," 
			line  += str(item.get("watchers", "-")) + "," 
			line  += str(item.get("forks", "-")) + "," 
			line  += gitToHttps(item.get("git_url", "-")) + "," 
			line  += item.get("description", "-")    
			count += 1
			f.write(line.encode('utf8') + '\n')
		elif(count >= projects):  
			break

	f.close()
	print 'Number of projects: ', count

	return outFile;


#clone.py
def cloneRepo(listProjects):

	print '#Cloning listed repositories #'

	inputFile = listProjects
	outputDir = raw_input('Choose the root directory for your cloned projects: ')


	if not os.path.exists(outputDir):
		os.makedirs(outputDir)

	f = open(inputFile, 'rt')

	try:
		reader = csv.reader(f)
		for row in reader:
			os.system('git clone ' + row[4] + ' ' + outputDir + "/" + row[0])
	finally:
		f.close() 
	print outputDir
	return outputDir


#cloc.py
def countLinesProjects(dirProjects, summaryFile):

	print '# Counting # of lines of projects #'
	inputDir = dirProjects
	outputDir = 'sloc/'
	#summaryFile = raw_input('Summary file for sloc: ')
	#keepTempFiles = raw_input('Keep temp files [yes/no] ')
	keepTempFiles = 'no'
	#lang = raw_input('Select the programming language [Java, C++, Python]: ')

	files = listdir(inputDir)

	for f in files:
		s = inputDir + '/' + f 
		if(isdir(s)):
			system('cloc ' + s + ' --csv --out=' + outputDir + "/" + f + ".csv")

	files = [f for f in listdir(outputDir) if f.endswith(".csv")]

	fout = file(summaryFile, "w")  
			
	for f in files:
		fname = outputDir + '/' + f 
		aFile = file(fname, "rt")
		reader = csv.reader(aFile)
		count = 0
		base   = 0
		other = 0
		for row in reader:
			if(count == 0): 
				row.insert(0, 'project')
			else: 
				if(lang == 'C++' and (row[1] == "C++" or row[1].startswith("C/C++"))):
					base += int(row[4])
				elif(row[1] == lang):
					base += int(row[4]) 
				else: 
					other += int(row[4])
				row.insert(0, f)
			count += 1
		
		writer = csv.writer(fout)
		writer.writerow((f, base, other))
		aFile.close()
							
		if(keepTempFiles == 'no'): 
			remove(fname)

	fout.close()

	return summaryFile

#create final input for static-analysis
def createInput(slocFile, dirProjects):
	print '# Creating final input file #'
	#resultFile = raw_input('Your final csv file to be saved: ')
	resultFile = "input_temp.csv"
	#files = listdir(dirProjects)
	fout = file(resultFile, "w")


	aFile = file(slocFile, "rt")
	reader = csv.reader(aFile)

	for row in reader:
		projectName = row[0][:-4]
		print projectName
		projectPath = dirProjects + '/' + projectName + '/'
		#No version checking yet, default at 1 for now
		fout.write(';;'+ projectName + ';1;' +  projectPath + ';' + row[1] + ';\n')

	



def main():

	listProjects = listRepositories()
	dirProjects = cloneRepo(listProjects)
	#dirProjects = '/home/luna/TG/tg-lambda/projects/'
	slocFile = countLinesProjects(dirProjects, sumFile)
	result_file = createInput(slocFile, dirProjects)
	return result_file


###############################################

