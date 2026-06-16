from flask import Flask, render_template, request, redirect, session, url_for
from db import get_db_connection
app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')


# ---------------- ABOUT ----------------
@app.route('/about')
def about():
    return render_template('about.html')


# ---------------- STUDENTS DASHBOARD ----------------
@app.route('/students', methods=['GET', 'POST'])
def students():

    # 🔐 LOGIN CHECK (must be first)
    if not session.get('logged_in'):
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    # ADD STUDENT
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

    # GET ALL STUDENTS
    cursor.execute("SELECT * FROM students")
    students_list = cursor.fetchall()

    # ANALYTICS
    total_students = len(students_list)
    gmail_users = sum(1 for s in students_list if "@gmail.com" in s["email"].lower())
    total_records = total_students

    conn.close()

    return render_template(
        'students.html',
        students=students_list,
        total_students=total_students,
        gmail_users=gmail_users,
        total_records=total_records
    )

# ---------------- DELETE STUDENT ----------------
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


# ---------------- UPDATE STUDENT ----------------
@app.route('/update/<int:id>', methods=['POST'])
def update_student(id):

    name = request.form['name']
    email = request.form['email']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE students
        SET name=%s,
            email=%s
        WHERE id=%s
        """,
        (name, email, id)
    )

    conn.commit()
    conn.close()

    return redirect('/students')

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM admin WHERE username=%s AND password=%s",
            (username, password)
        )

        admin = cursor.fetchone()
        conn.close()

        if admin:
            session['logged_in'] = True
            session['username'] = username
            return redirect('/students')   # IMPORTANT FIX
        else:
            return "Invalid credentials"

    return render_template('login.html')

# ---------------- TEST DATABASE ----------------
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

    app.run(
        host="0.0.0.0",
        port=port
    )