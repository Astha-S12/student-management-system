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

# ---------------- STUDENTS (CREATE + READ) ----------------
@app.route('/students')
def students():
    return "Flask is working, DB is the issue"

# ---------------- DELETE ----------------
@app.route('/delete/<int:id>')
def delete_student(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id=%s", (id,))

    conn.commit()
    conn.close()

    return redirect('/students')

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)