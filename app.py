from flask import Flask, render_template, request,redirect, url_for
from flask_mysqldb import MySQL 

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'tiger'
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

@app.route('/create_customer', methods=['post', 'get'])
def create_customer():
    message=""
    if request.method == 'POST':
        ssn_id=request.form.get('ssn_id')
        cust_id=request.form.get('cust_id')
        cname=request.form.get('cname')
        c_age=request.form.get('c_age')
        address=request.form.get('address')
        city=request.form.get('city')
        state=request.form.get('state')
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO CUSTOMER values(%s,%s,%s,%s,%s,%s,%s)',(ssn_id,cust_id,cname,c_age,address,city,state))
        results = cur.fetchall()
        if results:
            message="Done"
        else:
            message = "Error"
    return render_template('create_customer.html',message=message)
