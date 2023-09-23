from datetime import date

from flask import request, render_template, redirect, flash
from flask_login import current_user, login_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from models import University, app, db, Student, User
from flask_login import login_user
from flask_login import logout_user


@app.route('/api')
def info():
    return render_template('api_info.html')


@app.route('/api/university/create', methods=['post', 'get'])
@login_required
def create_university():
    if request.method == 'GET':
        return render_template(
            'createUniversity.html',
            university=University(full_name="", short_name="", date_of_creation=date.today())
        )
    if request.method == 'POST':
        full_name = request.form['full_name']
        short_name = request.form['short_name']
        date_of_creation = request.form['date_of_creation']
        university = University(full_name=full_name, short_name=short_name, date_of_creation=date_of_creation)
        db.session.add(university)
        db.session.commit()
        return redirect('/api/university')


@app.get('/api/university/delete/<int:id>')
@login_required
def delete_university_by_id(id):
    university = University.query.filter_by(university_id=id).first()
    db.session.delete(university)
    db.session.commit()
    return redirect('/api/university')


@app.route('/api/university/edit/<int:id>', methods=['post', 'get'])
@login_required
def edit_university_by_id(id):
    university = University.query.filter_by(university_id=id).first()
    if request.method == 'POST':
        if university:
            db.session.delete(university)
            full_name = request.form['full_name']
            short_name = request.form['short_name']
            date_of_creation = request.form['date_of_creation']
            university = University(full_name=full_name, short_name=short_name, date_of_creation=date_of_creation)
            db.session.add(university)
            db.session.commit()
            return redirect('/api/university')
        return f"University with id = {id} Does nit exist"
    return render_template(
        'createUniversity.html',
        university=university
    )


@app.get('/api/university')
def get_all_university():
    universities = University.query.all()
    return render_template('allUniversity.html', universities=universities)


@app.route('/api/student/create', methods=['post', 'get'])
@login_required
def create_student():
    if request.method == 'GET':
        return render_template(
            'createStudent.html',
            student=Student(FCs="", date_of_birth=date.today(), year_of_admission=date.today()),
            available_university_list=University.query.all()
        )
    if request.method == 'POST':
        university = request.form['university']
        FCs = request.form['FCs']
        date_of_birth = request.form['date_of_birth']
        year_of_admission = request.form['year_of_admission']
        student = Student(university=university, FCs=FCs, date_of_birth=date_of_birth,
                          year_of_admission=year_of_admission)
        db.session.add(student)
        db.session.commit()
        return redirect('/api/student')


@app.get('/api/student/delete/<int:id>')
@login_required
def delete_student_by_id(id):
    student = Student.query.filter_by(student_id=id).first()
    db.session.delete(student)
    db.session.commit()
    return redirect('/api/student')


@app.route('/api/student/edit/<int:id>', methods=['post', 'get'])
@login_required
def edit_student_by_id(id):
    student = Student.query.filter_by(student_id=id).first()
    if request.method == 'POST':
        if student:
            db.session.delete(student)
            university = request.form['university']
            FCs = request.form['FCs']
            date_of_birth = request.form['date_of_birth']
            year_of_admission = request.form['year_of_admission']
            student = Student(university=university, FCs=FCs, date_of_birth=date_of_birth,
                              year_of_admission=year_of_admission)
            db.session.add(student)
            db.session.commit()
            return redirect('/api/student')
        return f"Student with id = {id} Does nit exist"
    return render_template(
        'createStudent.html',
        student=student,
        available_university_list=University.query.all()
    )


@app.get('/api/student')
def get_all_student():
    students = Student.query.all()
    return render_template('allStudent.html', students=students)


@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect("/api/login")
        login_user(user, remember=remember)
        return redirect("/api")
    if request.method == 'GET':
        return render_template('login.html')


@app.route('/api/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists')
            return redirect("/api/signup")
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        return redirect("/api")
    if request.method == 'GET':
        return render_template('signup.html')


@app.route('/api/logout')
@login_required
def logout():
    logout_user()
    return redirect('/api')


if __name__ == '__main__':
    app.run()
