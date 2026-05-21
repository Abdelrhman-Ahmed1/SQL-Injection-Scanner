# app.py
# Vulnerable SQL Injection Demo Lab
# FOR EDUCATIONAL PURPOSES ONLY

from flask import Flask, render_template_string, request
import sqlite3

app = Flask(__name__)

# =========================
# CREATE DATABASE
# =========================

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    # Sample user
    cursor.execute("DELETE FROM users")

    cursor.execute("""
    INSERT INTO users(username, password)
    VALUES('admin', '1234')
    """)

    conn.commit()
    conn.close()


# =========================
# HTML PAGE
# =========================

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SQL Injection Lab</title>

    <style>
        body{
            background:#111;
            color:white;
            font-family:Arial;
            display:flex;
            justify-content:center;
            align-items:center;
            height:100vh;
        }

        .box{
            background:#1e1e1e;
            padding:30px;
            border-radius:10px;
            width:300px;
        }

        input{
            width:100%;
            padding:10px;
            margin-top:10px;
            border:none;
            border-radius:5px;
        }

        button{
            width:100%;
            padding:10px;
            margin-top:15px;
            border:none;
            background:#00aaff;
            color:white;
            border-radius:5px;
            cursor:pointer;
        }

        .msg{
            margin-top:15px;
            color:#00ff99;
        }

        .error{
            margin-top:15px;
            color:red;
        }
    </style>
</head>

<body>

<div class="box">
    <h2>Login</h2>

    <form method="POST">

        <input type="text"
               name="username"
               placeholder="Username">

        <input type="password"
               name="password"
               placeholder="Password">

        <button type="submit">Login</button>

    </form>

    {% if message %}
        <div class="msg">{{message}}</div>
    {% endif %}

    {% if error %}
        <div class="error">{{error}}</div>
    {% endif %}
</div>

</body>
</html>
"""


# =========================
# VULNERABLE LOGIN
# =========================

@app.route("/", methods=["GET", "POST"])
def login():

    message = ""
    error = ""

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # ======================================
        # INTENTIONALLY VULNERABLE QUERY
        # ======================================

        query = f"""
        SELECT * FROM users
        WHERE username='{username}'
        AND password='{password}'
        """

        print("\n[QUERY]")
        print(query)

        try:
            result = cursor.execute(query).fetchone()

            if result:
                message = "Logged in successfully!"
            else:
                error = "Invalid username or password"

        except Exception as e:
            error = str(e)

        conn.close()

    return render_template_string(
        HTML,
        message=message,
        error=error
    )


# =========================
# RUN APP
# =========================

if __name__ == "__main__":

    init_db()

    app.run(debug=True)