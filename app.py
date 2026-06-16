from flask import Flask, render_template, request, redirect
from db import get_db_connection
import os

app = Flask(__name__)

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')


# ---------------- ABOUT ----------------
@app.route('/about')
def about():
    return render_template('about.html')


# ---------------- STUDENTS (CREATE + READ + SEARCH) ----------------
@app.route('/students', methods=['GET', 'POST'])
def students():

    conn = get_db_connection()
    cursor = conn.cursor()

    # CREATE
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        cursor.execute(
            "INSERT INTO students (name, email) VALUES (%s, %s)",
            (name, email)
        )

        conn.commit()
        conn.close()

        return redirect('/students')

    # SEARCH
    search = request.args.get('search')

    if search:
        cursor.execute(
            "SELECT * FROM students WHERE name LIKE %s",
            (f"%{search}%",)
        )
    else:
        cursor.execute("SELECT * FROM students")

    students_list = cursor.fetchall()

    conn.close()

    return render_template(
        'students.html',
        students=students_list
    )


# ---------------- DELETE ----------------
@app.route('/delete/<int:id>')
def delete_student(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=%s",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/students')


# ---------------- EDIT PAGE ----------------
@app.route('/edit/<int:id>')
def edit_student(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE id=%s",
        (id,)
    )

    student = cursor.fetchone()

    conn.close()

    return render_template(
        'edit_student.html',
        student=student
    )


# ---------------- UPDATE ----------------
@app.route('/update/<int:id>', methods=['POST'])
def update_student(id):

    name = request.form['name']
    email = request.form['email']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE students
        SET name=%s, email=%s
        WHERE id=%s
        """,
        (name, email, id)
    )

    conn.commit()
    conn.close()

    return redirect('/students')


# ---------------- TEST ----------------
@app.route('/test')
def test():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    conn.close()

    return str(data)


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)