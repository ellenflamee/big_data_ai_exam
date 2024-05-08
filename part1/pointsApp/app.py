import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Fetch environment variables for database configuration
db_user = os.getenv('POSTGRES_USER', 'myuser')
db_password = os.getenv('POSTGRES_PASSWORD', 'mypassword')
db_name = os.getenv('POSTGRES_DB', 'mydatabase')
db_host = 'db'  # Database service hostname in Docker Compose
db_port = 5432

# Flask application setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
db = SQLAlchemy(app)

# Define a model representing the database table
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.Integer, default=0)

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/create', methods=['POST'])
def create_student():
    name = request.form.get('name')
    if name:
        student = Student(name=name)
        db.session.add(student)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/assign/<int:student_id>', methods=['POST'])
def assign_grade(student_id):
    grade = int(request.form.get('grade', 0))
    student = Student.query.get(student_id)
    if student:
        student.grade = grade
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
