from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Database configuration
def get_conn():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="company_db"
    )


# HOME - VIEW EMPLOYEES
@app.route("/")
def index():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.id, e.name, e.email, e.phone, d.name 
        FROM employees e 
        LEFT JOIN departments d ON e.department_id = d.id
    """)
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    # print(employees)
    return render_template("index.html", employees=employees)


# GET DEPARTMENTS
def get_departments():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM departments")
    departments = cursor.fetchall()
    cursor.close()
    conn.close()
    return departments


# ADD EMPLOYEE
@app.route("/add", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        department_id = request.form["department_id"]

        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO employees (name, email, phone, department_id) VALUES (%s, %s, %s, %s)",
            (name, email, phone, department_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect("/")

    departments = get_departments()
    return render_template("add.html", departments=departments)


# EDIT EMPLOYEE
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_employee(id):
    conn = get_conn()
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        department_id = request.form["department_id"]

        cursor.execute(
            "UPDATE employees SET name=%s, email=%s, phone=%s, department_id=%s WHERE id=%s",
            (name, email, phone, department_id, id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect("/")

    cursor.execute("SELECT id, name, email, phone, department_id FROM employees WHERE id=%s", (id,))
    employee = cursor.fetchone()
    cursor.close()
    conn.close()

    departments = get_departments()
    return render_template("edit.html", employee=employee, departments=departments)


# DELETE EMPLOYEE
@app.route("/delete/<int:id>")
def delete_employee(id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
