from flask import Flask, render_template, request,redirect, url_for
from flask_mysqldb import MySQL 

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'retailbanking'
mysql = MySQL(app)
@app.route('/', methods=['post', 'get'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form.get('uname')  # access the data inside 
        password = request.form.get('password')
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM userstore WHERE login = %s AND password = %s', (username, password,))
        results = cur.fetchall()
        if results:
            return redirect(url_for('create_customer'))
        else:
            message = "Wrong username or password"
 
    return render_template('login.html', message=message)

@app.route('/create_customer')
def create_customer():
    return render_template('create_customer.html')
