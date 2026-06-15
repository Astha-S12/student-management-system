from flask import Flask, render_template, request, redirect
from db import get_db_connection

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/students', methods=['GET', 'POST'])
def students():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        cursor.execute(
            "INSERT INTO students (name, email) VALUES (%s, %s)",
            (name, email)
        )
        conn.commit()

        return redirect('/students')

    cursor.execute("SELECT * FROM students")
    students_list = cursor.fetchall()

    conn.close()

    return render_template('students.html', students=students_list)


@app.route('/delete/<int:id>')
def delete_student(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id=%s", (id,))

    conn.commit()
    conn.close()

    return redirect('/students')


import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)