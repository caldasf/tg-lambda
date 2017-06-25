# BDAnalisador
## About


### create_input.py
This script is called automatically by statis_analysis if no do the following tasks


### static_analysis.py
For each month until early 2013 and run static_analysis project over it and then generate the output folders.
TBA

Execute:
```sh
python static_analysis.py <option> -path <projects_path>
```

When options are not defined, it runs everything, including downloading all projects again. 
If options are defined, we have:

* _--reset_ : it will reset everything, the final input file that BDAnalisador is going to use in the end, remove everything from _output_ folder and _input_ folder and start over again, but will consider that create_input.py was ran previously and will try to open its result file and assume that the path for the projects also have the projects on it already.

* _--add_ : it will just append into the final input file for BDAnalisador if it exists and not delete anything from _output_ and _input_ folders, also taking into consideration that create_input.py was already executed.

* _--all_ : run it all, from create_input script with default values (as described before), to static analysis specific activites that include:
	** for each project and each month (from April 2017 to December 2012), find the most recent commit for that month, checkout that version, count its lines of Java code and run static_analysis over all of them, generating output files. Static analysis activies will be described on its section.

You should take into consideration that <input_file> is the temporary input file created by create_input.py script.

### Static Analysis
TBA

### BDAnalisador
After downloading all projects, running static analysis and generating the final input.csv file along with output/ folder that contains all output for each project in the format
