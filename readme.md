# SCHOOL  MANAGEMENT REGISTER 

School Management register intergrates directly into the school admin register where the adminstration office now has access to Student, Teachers and Class.This project is made to implement a flask app that returns data from a database and executes without breaking.

It provides the admininstration  officer to sign into the application to have acess to the application for the database which gives information about the students that are attending the class and the teachers responsible for the class. It also have the edit option where an entry can be edited example to add new student or to add new teacher or to add a class. 

This app has been designed to work both on front and back end  API of the same server. The users are authenticated on the front end vis flask-login

## Technology Used :
- Python - Coding language
- Flask  - The framework that allows interaction with data through http
- SQLAlchemy - The ORM that interacts with python and the database
- Jinja - Templating language for interacting with the framework

## Prerequisites
Prerequisites is to have python 3.7+, pip and pip-env installed

## Installation
```
git clone https://github.com/dhanyavittaldas/School_Management_Register.git
cd src
python -m venv env
source venv/bin/activate
pip3 install -r requirements.txt
export FLASK_APP=app.py
```
## Features
-  Possible to view all the students in the class
- Possible to get the details of the teacher of the house
- Search for a student and will show the total results
- Edit the current information
- User log in for security 

## Usage
Setup the db:
```
flask db-custom create
```
There is already a data base created with some entries

Open your browser to http://127.0.0.1:5000/


## Wireframes

![Login](Docs\login_page.PNG)

![Register](Docs\register_page.PNG)

![Home](Docs\home_page.PNG)

![Student](Docs\Student_page.PNG)
![Teacher](Docs\Teacher.PNG)
![Class](Docs\Class.PNG)


## ERD Diagram

In this project as a requirement I have created 4 class as well as have more than 1 relation between the tables

![ERD](Docs\ERD.PNG)


## R2 and R3 Questions ( The part of the project)

This has been added as a report.md file in Docs folder
