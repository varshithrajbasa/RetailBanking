from flask import Flask, render_template, request,redirect, url_for,session
from flask_mysqldb import MySQL 

app = Flask(__name__)
app.secret_key = "S689Gjysjms0"
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
            session['username'] = username
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
        cust_id=int(request.form.get('cust-id'))
        cname=request.form.get('cname')
        c_age=int(request.form.get('cage'))
        address=request.form.get('address')
        city=request.form.get('secondlist')
        state=request.form.get('listBox')
        if(mysql):
            cursor= mysql.connection.cursor()
            #cursor.execute("select * from customer")
            cursor.execute('''INSERT INTO customer(ws_ssn, ws_cust_id, ws_name, ws_age, ws_adrs, city, state) values(%s, %s, %s, %s, %s, %s, %s)''',(ssn_id,cust_id,cname,c_age,address,city,state))
            mysql.connection.commit()
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
@app.route('/update',methods=['post', 'get'])
def update():
    id=int(request.form.get('id'))
    cname=request.form.get('cname')
    address=request.form.get('address')
    c_age=int(request.form.get('cage'))
    cur = mysql.connection.cursor()
    cur.execute('''UPDATE  customer Set ws_age= %s ,ws_adrs= %s,ws_name= %s where ws_ssn= %s''',(c_age,address,cname,id))
    mysql.connection.commit()
    return redirect(url_for('users'))
@app.route('/view_customer2')
def users1():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM customer")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('view_customer2.html',userDetails=userDetails)
@app.route('/delete_customer',methods=['post', 'get'])
def delete_customer():
    id=int(request.form.get('id'))
    cur = mysql.connection.cursor()
    resultValue = cur.execute("select * from customer where ws_ssn = %s",(id,))
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('delete_customer.html',userDetails=userDetails)
@app.route('/delete',methods=['post', 'get'])
def delete():
    id=int(request.form.get('id'))
    cur = mysql.connection.cursor()
    cur.execute('''delete from customer  where ws_ssn= %s''',(id,))
    mysql.connection.commit()
    return redirect(url_for('users'))
#For accouts
@app.route('/create_account', methods=['post', 'get'])
def create_account():
    message=""
    id=int(request.form.get('cust-id'))
    a_type=request.form.get('account_type')
    print(a_type)
    balance=request.form.get('deposit_amount')
    today = date.today()
    cur = mysql.connection.cursor()
    cur.execute('''select * from customer where ws_cust_id= %s''',(id,))
    result_value=cur.fetchall()
    if result_value:
        account_id=result_value[0][0]
        cur.execute('''INSERT INTO `retailbanking`.`account` (`ws_cust_id` ,`ws_acct_id` ,`ws_acct_type` ,`ws_acct_balance` ,`ws_acct_crdate` ) VALUES (%s, %s, %s, %s, %s)''',(id,account_id,a_type,balance,today,))
        mysql.connection.commit()
        message="Account created"
    return render_template('create_account.html',message=message)
@app.route('/delete_account')
def delete_account():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM account")
    if resultValue > 0:
        userDetails = cur.fetchall()
    return render_template('delete_account.html',accountDetails=userDetails)
@app.route('/delete_a', methods=['post', 'get'])
def delete_a():
    account_id=int(request.form.get('account_id'))
    account_type=request.form.get('account_type')
    cur = mysql.connection.cursor()
    cur.execute('''select * from account where ws_acct_type= %s && ws_acct_id= %s''',(account_type,account_id,))
    result_value=cur.fetchall()
    print(result_value)
    if result_value:
        cur.execute('''delete from account where ws_acct_id= %s''',(account_id,))
        mysql.connection.commit()
    return redirect(url_for('delete_account'))
