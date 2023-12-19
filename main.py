from flask import Flask, render_template, request, g
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange
import sqlite3
from flask_bootstrap import Bootstrap5
from datetime import datetime

app = Flask(__name__)
app.secret_key = "ag45hb235k6b2i3m34"
bootstrap = Bootstrap5(app)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('yoga-class.db')
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS enrollment(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                batch TEXT NOT NULL,
                enrollment_date INTEGER NOT NULL 
            )
        ''')
        cursor.close()


@app.route("/")
def home():
    return render_template('index.html')


class EnrollForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[NumberRange(min=18, max=65), DataRequired()])
    batch = SelectField('Batch', choices=[('6-7AM', '6-7AM'), ('7-8AM', '7-8AM'), ('8-9AM', '8-9AM'), ('5-6PM', '5-6PM')])
    submit = SubmitField('Enroll')


@app.route("/enroll", methods=["GET", "POST"])
def enroll():
    enroll_form = EnrollForm()
    if request.method == 'POST' and enroll_form.validate_on_submit():
        db = get_db()
        cursor = db.cursor()
        name = enroll_form.name.data
        age = enroll_form.age.data
        batch = enroll_form.batch.data
        enrollment_date = int(datetime.now().month)
        cursor.execute('INSERT INTO enrollment (name, age, batch, enrollment_date) VALUES (?, ?, ?, ?)',
                       (name, age, batch, enrollment_date))
        db.commit()
        cursor.close()
        return f"Enrollment successful! Data stored in the database."
    return render_template("enroll.html", form=enroll_form)


class UpdateForm(FlaskForm):
    userId = IntegerField('UserID', validators=[DataRequired()])
    batch = SelectField('Batch', choices=[('6-7AM', '6-7AM'), ('7-8AM', '7-8AM'), ('8-9AM', '8-9AM'), ('5-6PM', '5-6PM')])
    submit = SubmitField('Update')


@app.route("/update", methods=['POST', 'GET'])
def update_batch():
    update_form = UpdateForm()
    if request.method == 'POST' and update_form.validate_on_submit():
        user_id = update_form.userId.data
        new_batch = update_form.batch.data
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT enrollment_date FROM enrollment WHERE id = ?', (user_id,))
        prev_month = cursor.fetchone()
        if prev_month:
            curr_month = datetime.now().month
            print(int(curr_month) - int(prev_month[0]))
            if (int(curr_month) - int(prev_month[0])) == 0:
                return "Try again next month"
            else:
                cursor.execute('UPDATE enrollment SET batch = ? WHERE id = ?', (new_batch, user_id))
                cursor.close()
                db.commit()
                return "Batch updated successfully!"

        else:
            return "User ID does not exist"

    return render_template("update.html", form=update_form)


@app.route("/admin/enrollments")
def admin_enrollments():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM enrollment')
    enrollments = cursor.fetchall()
    cursor.close()
    return render_template("admin.html", enrollments=enrollments)


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)
