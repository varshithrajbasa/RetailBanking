from flask import Flask, render_template, request,redirect, url_for
from flask_mysqldb import MySQL 

app = Flask(__name__)
app.secret_key = 'S689Gjysjms0’
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
            session['username'] = request.form.get('uname')
            return redirect(url_for('create_customer'))
        else:
            message = "Wrong username or password"
        mysql.connection.commit()
        cur.close()
 
    return render_template('login.html', message=message)

@app.route('/create_customer', methods=['post', 'get'])
def create_customer():
    message=""
    if request.method == 'POST':
        ssn_id=int(request.form.get('ssn-id'))
        print(ssn_id)
        cust_id=int(request.form.get('cust-id'))
        print(cust_id)
        cname=request.form.get('cname')
        print(cname)
        c_age=int(request.form.get('cage'))
        print(c_age)
        address=request.form.get('address')
        print(address)
        city=request.form.get('secondlist')
        print(city)
        state=request.form.get('listBox')
        print(state)
        curs = mysql.connection.cursor()
        curs.execute('''INSERT INTO customer(ws_ssn, ws_cust_id, ws_name, ws_age, ws_adrs, city, state) values(%s, %s, %s, %s, %s, %s, %s)''',(ssn_id,cust_id,cname,c_age,address,city,state))
        results = curs.fetchall()
        if results:
            message="Done"
        else:
            message = "Error"
    return render_template('create_customer.html',message=message)
@app.route('/view_customer')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM customer")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('view_customer.html',userDetails=userDetails)
@app.route('/update_customer',methods=['post', 'get'])
def update_customer():
    id=int(request.form.get('id'))
    cur = mysql.connection.cursor()
    resultValue = cur.execute("select * from customer where ws_ssn = %s",(id,))
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('update_customer.html',userDetails=userDetails)
