from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import join
import os


app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))


    def __init__(self, name, email, password):

        self.name = name
        self.email = email
        self.password = password

#Creating model table for our CRUD database
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))

    def __init__(self, name, email, phone,class_id):

        self.name = name
        self.email = email
        self.phone = phone
        self.class_id = class_id

class Class(db.Model):
    __tablename__ = 'class'
    id = db.Column(db.Integer, primary_key = True)
    std = db.Column(db.String(10))
    division = db.Column(db.String(10))

    def __init__(self, std, division):

        self.std = std
        self.division = division

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(100))
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'))


    def __init__(self, name, email,address, phone,class_id):

        self.name = name
        self.email = email
        self.address = address
        self.phone = phone
        self.class_id = class_id

#This is the index route where we are going to
#query on all our employee data
@app.route('/', methods = ['GET', 'POST'])
def Index():
    if 'user_id' in session:
        students = Student.query.all()
        if request.method == 'POST' and 'tag' in request.form:
            tag = request.form["tag"]
            search = "%{}%".format(tag)
            students = Student.query.filter(Student.name.like(search)).all()
            if(students):
                return render_template('home.html', students=students,cnt = len(students), tag=tag)
            else:
                return render_template('home.html', students=students,cnt = 0, tag=tag)
        return render_template("home.html",students=students,cnt = len(students))
    else:
        return redirect('/login')

@app.route('/login')
def Login():

    return render_template("login.html")

@app.route('/login_validation', methods = ['POST'])
def LoginValidation():
    if request.method == 'POST':
        email1 = request.form['email']
        password1 = request.form['password']
        user_data = User.query.filter_by(email = email1, password = password1).all()
        for row in user_data:
            if(row.id):
                session['user_id'] = row.id
                return redirect(url_for('Index'))
        else:
            return redirect(url_for('Login'))

@app.route('/register')
def Register():

    return render_template("register.html")

@app.route('/add_user', methods = ['POST'])
def AddUser():
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']


        my_data = User(name, email, password)
        db.session.add(my_data)
        db.session.commit()

        flash("User created Successfully")

        return redirect(url_for('Login'))

@app.route('/logout')
def Logout():
    session.pop('user_id')
    return redirect(url_for('Login'))

@app.route('/teacher')
def TeacherW():
    if 'user_id' in session:
        all_data = Teacher.query.all()
        classes = Class.query.all()
        return render_template("teacher.html", teachers = all_data,classes=classes)
    else:
        return redirect('/login')
    

#this route is for inserting data to mysql database via html forms
@app.route('/tinsert', methods = ['POST'])
def tinsert():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        class_id = request.form['class_id']

        my_data = Teacher(name, email, phone,class_id)
        db.session.add(my_data)
        db.session.commit()

        flash("Teacher Inserted Successfully")

        return redirect(url_for('TeacherW'))


#this is our update route where we are going to update our employee
@app.route('/tupdate', methods = ['GET', 'POST'])
def tupdate():

    if request.method == 'POST':
        my_data = Teacher.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        my_data.class_id = request.form['class_id']
        db.session.commit()
        flash("Teacher Updated Successfully")

        return redirect(url_for('TeacherW'))




#This route is for deleting our employee
@app.route('/tdelete/<id>/', methods = ['GET', 'POST'])
def tdelete(id):
    my_data = Teacher.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Teacher Deleted Successfully")

    return redirect(url_for('TeacherW'))


@app.route('/class')
def ClassW():
    if 'user_id' in session:
        all_data = Class.query.all()
        return render_template("class.html", classes = all_data)
    else:
        return redirect('/login')
    

#this route is for inserting data to mysql database via html forms
@app.route('/cinsert', methods = ['POST'])
def cinsert():

    if request.method == 'POST':

        std = request.form['std']
        division = request.form['division']
      
        my_data = Class(std, division)
        db.session.add(my_data)
        db.session.commit()

        flash("Class Inserted Successfully")

        return redirect(url_for('ClassW'))


#this is our update route where we are going to update our employee
@app.route('/cupdate', methods = ['GET', 'POST'])
def cupdate():

    if request.method == 'POST':
        my_data = Class.query.get(request.form.get('id'))

        my_data.std = request.form['std']
        my_data.division = request.form['division']
   
        db.session.commit()
        flash("Class Updated Successfully")

        return redirect(url_for('ClassW'))




#This route is for deleting our employee
@app.route('/cdelete/<id>/', methods = ['GET', 'POST'])
def cdelete(id):
    my_data = Class.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Class Deleted Successfully")

    return redirect(url_for('ClassW'))


@app.route('/student')
def StudentW():
    if 'user_id' in session:
        all_data = Student.query.all()
        classes = Class.query.all()
        return render_template("student.html",students = all_data,classes = classes)
    else:
        return redirect('/login')
    
@app.route('/sinsert', methods = ['POST'])
def sinsert():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        phone = request.form['phone']
        class_id = request.form['class_id']

        my_data = Student(name, email,address, phone,class_id)
        db.session.add(my_data)
        db.session.commit()

        flash("Student Inserted Successfully")

        return redirect(url_for('StudentW'))


#this is our update route where we are going to update our employee
@app.route('/supdate', methods = ['GET', 'POST'])
def supdate():

    if request.method == 'POST':
        my_data = Student.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.address = request.form['address']
        my_data.phone = request.form['phone']
        my_data.class_id = request.form['class_id']

        db.session.commit()
        flash("Student Updated Successfully")

        return redirect(url_for('StudentW'))




#This route is for deleting our employee
@app.route('/sdelete/<id>/', methods = ['GET', 'POST'])
def sdelete(id):
    my_data = Student.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Student Deleted Successfully")

    return redirect(url_for('StudentW'))

if __name__ == "__main__":
    app.run(debug=True)