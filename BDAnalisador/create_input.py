#!/usr/bin/python
# Script that can list and clone most popular git repositories. 
# In the end, it also generates a temporary input file so static_analysis.py
# can work with it.
#   1. List repositories
#   2. Clone Repositories
#   3. Use sloc and save information
#   4. Create file


import requests
import csv
import os
import sys
from os import listdir, remove, system
from os.path import isdir, abspath
from subprocess import call


class CreateInput():
    def __init__ (self, projects_dir, lang="Java", 
                n_proj=100, n_stars=200):

        self.lang = lang
        self.projects_file = "{}.projects".format(self.lang)
        self.n_projects = n_proj
        self.n_stars = n_stars
        self.projects_dir = projects_dir

    def __git_to_https(url_name):
        try:
            new_url = url_name[3:]
            new_url = 'https' + new_url
            return new_url
        except:
            print ("Error: url'{}' in wrong format or does not exist.\
                \n".format(new_url))


    def list_repositories(self):
        prefix = 'https://api.github.com/search/repositories?q='
        suffix = '&sort=self.stars&order=desc&page='

        print ('\n# Listing github self.projects to use #')

        self.lang  = '+language:' + self.lang 
        self.n_stars = 'stars:%3E'  + str(self.n_stars)
        uri   = prefix + self.n_stars + self.lang + suffix

        print ('searching the github API')
        print ('query string: {}'.format(uri))

        response = requests.get(uri + '1')
        data = response.json()
        items = data['items']
        
        f = open(self.projects_file, 'w')
        pagination = 0
        for item in items:
            pagination += 1 

        pages = 1 + (self.n_projects / pagination)
        
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
            if(count < self.n_projects and item != None):
                line   = item.get("name", "-") + ","
                line  += str(item.get("size", "-")) + "," 
                line  += str(item.get("watchers", "-")) + "," 
                line  += str(item.get("forks", "-")) + "," 
                line  += item.get("git_url", "-") #+ "," 
                #line  += item.get("description", "-")    
                count += 1
                f.write(line.encode('utf8') + '\n')
            elif(count >= self.n_projects):  
                break

        f.close()
        print ('Number of projects: {}'.format(count))

        #return (self.projects_file)


    def clone_repos(self):
        print('\n# Cloning listed repositories #')
        input_file = self.projects_file
        clone_dir = self.projects_dir

        if not os.path.exists(clone_dir):
            os.makedirs(clone_dir)

        f = open(input_file, 'rt')
        try:
            reader = csv.reader(f)
            for row in reader:
                if os.listdir(work_path):
                    os.system('git clone {} {}/{}'.format(row[4], clone_dir, row[0]))
                else:
                    print ("Error: {}/{} is not an empty \
                        repository.".format(clone_dir, row[0]))
        except:
            print("Error: Unexpected error happened while cloning repositories.")
        finally:
            f.close() 

        #return clone_dir


    #cloc.py
    def count_code_lines(self):
        print ('\n# Counting # of lines of projects #')

        summary_file = "summary.csv"
        projects_dir = self.projects_dir
        sloc_dir = 'sloc/'
        keepTempFiles = 'no'
        files = listdir(projects_dir)

        if not os.path.exists(sloc_dir):
            os.makedirs(sloc_dir)

        for f in files:
            print (f)
            print (projects_dir)
            s = projects_dir + '/' + f 
            if(isdir(s)):
                system('cloc ' + s + ' --csv --out=' + sloc_dir + "/" + f + ".csv")

        files = [f for f in listdir(sloc_dir) if f.endswith(".csv")]
        fout = file(summary_file, "w")  
                
        for f in files:
            fname = sloc_dir + '/' + f 
            aFile = file(fname, "rt")
            reader = csv.reader(aFile)
            count = 0
            base   = 0
            other = 0
            for row in reader:
                if(count == 0): 
                    row.insert(0, 'project')
                else: 
                    if(self.lang == 'C++' and (row[1] == "C++" or row[1].startswith("C/C++"))):
                        base += int(row[4])
                    elif(row[1] == self.lang):
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
        os.rmdir(sloc_dir) 
        return summary_file


    def create_input(self):
        print ('\n# Creating final input file #')

        sloc_file = "summary.csv"
        result_file = "input_temp.csv"

        fout = file(result_file, "w")


        aFile = file(sloc_file, "rt")
        reader = csv.reader(aFile)

        for row in reader:
            project_name = row[0][:-4]
            print project_name
            cur_project_path = os.path.join(self.projects_dir, project_name)
            # No version checking yet, default at 1 for now
            fout.write(';;{};1;{};{};\n'.format(project_name, cur_project_path, row[1]))

        return (result_file)        

    def create(self):
        self.list_repositories()
        self.clone_repos()
        self.count_code_lines()
        self.create_input()


def check_args(my_args):
    i = 0
    try:
        for arg in sys.argv:
            if (arg == '-p'):
                my_args['dir_path'] = sys.argv[i+1] 
            elif (arg == '-l'):
                my_args['lang'] = sys.argv[i+1]
            elif (arg == '-s'):
                my_args['stars'] = int(sys.argv[i+1])
            elif (arg == '-n'):
                my_args['proj_count'] = int(sys.argv[i+1])
            i += 1
    except:
        print ("Error: An unexpected error happened.")

    
    return my_args

def main():
    try:
        input = raw_input
    except NameError:
        pass

    myargs = {"dir_path": "", 
             "lang" : "Java", 
             "stars" : 200,
             "proj_count" : 100,
            }

    myargs = check_args(myargs)

    c = CreateInput(myargs["dir_path"], myargs["lang"], 
                myargs["proj_count"], myargs["stars"])

    c.create()

###############################################

if __name__ == '__main__':
    main()
