import mysql.connector

# Create connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)

cursor = conn.cursor()

# Create database
cursor.execute("DROP DATABASE IF EXISTS company_db")
cursor.execute("CREATE DATABASE company_db")
cursor.execute("USE company_db")

# Create departments table
cursor.execute("""
    CREATE TABLE departments (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(50)
    )
""")

# Create employees table with foreign key
cursor.execute("""
    CREATE TABLE employees (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100),
        email VARCHAR(100),
        phone VARCHAR(20),
        department_id INT,
        FOREIGN KEY (department_id) REFERENCES departments(id)
    )
""")

# Insert departments
departments = [("IT",), ("HR",), ("Sales",)]
for dept in departments:
    cursor.execute("INSERT INTO departments (name) VALUES (%s)", dept)

# Insert employees
employees = [
    ("John Doe", "john@example.com", "123-456-7890", 1),
    ("Jane Smith", "jane@example.com", "098-765-4321", 2),
    ("Bob Johnson", "bob@example.com", "555-123-4567", 3),
]

for emp in employees:
    cursor.execute(
        "INSERT INTO employees (name, email, phone, department_id) VALUES (%s, %s, %s, %s)",
        emp
    )

conn.commit()
cursor.close()
conn.close()

print("✓ Database created with departments and employees tables!")
