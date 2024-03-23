from flask import Flask, render_template, request, json
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MySQL connection configuration
mysql = mysql.connector.connect(user='web', password='webPass',
                                 host='127.0.0.1',
                                 database='student')

# Define routes
@app.route("/")
def hello():
    cur = mysql.cursor()
    cur.execute('''SELECT * FROM students''')
    rv = cur.fetchall()
    students = [{'Name': row[0].replace('\n', ' '), 'Email': row[1], 'ID': row[2]} for row in rv]
    return render_template('index.html', students=students)

# Add route for adding a student
@app.route("/add", methods=['POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cur = mysql.cursor()
        query = '''INSERT INTO students(studentName, email) VALUES('{}','{}');'''.format(name, email)
        cur.execute(query)
        mysql.commit()
        return json.dumps({"Result": "Success"})
    else:
        return "Invalid request"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')
