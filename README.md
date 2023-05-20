## L7 HOMEWORK ASSIGNMENT

### AUTHOR
Rachid Ounit

### DATE
05/15/2023

### DESCRIPTION
This project contains the Python-based web application useful to determine whether a set of data (integers) follows the Benford's law.

### SYSTEM REQUIREMENTS & VERSION
Python 3.8.9 (or earlier) and Django 4.2.1 (or earlier) are required. 
In addition, the necessary python packages are:
```
matplotlib>=3.7.1
scipy>=1.10.1
```

### DATA REQUIREMENTS
The user should prepare a text file (.txt or .csv format) with a one-line header containing one or several columns describing the data.
The column used by this solution is the last column and must contain only integers.

### INSTALLATION & EXECUTION

1. Create a directory and move in it.
2. Create a virtual environment and activate it:
```
python3 -m venv .
source ./bin/activate
```
3. Copy this repo into your directory and move into the directory "HW-L7-*" 
4. Install the required dependencies using the requirements.txt file:
```
 pip install -r requirements.txt
```
5. Launch the webserver:
```
python webserver/manage.py runserver
```
6. Then open "localhost:8000/benford" from your favorite browser, and follow the instructions provided on it!


### QUESTIONS
Any questions or feedback? please reach out at rachid.ounit@gmail.com
