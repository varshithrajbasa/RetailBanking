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
    
    if session=={}:
        return redirect(url_for('login'))
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
    
    if session=={}:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM customer")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('view_customer.html',userDetails=userDetails)

@app.route('/update_customer',methods=['post', 'get'])
def update_customer():
    
    if session=={}:
        return redirect(url_for('login'))
    id=int(request.form.get('id'))
    cur = mysql.connection.cursor()
    resultValue = cur.execute("select * from customer where ws_ssn = %s",(id,))
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('update_customer.html',userDetails=userDetails)

@app.route('/update',methods=['post', 'get'])
def update():
    
    if session=={}:
        return redirect(url_for('login'))
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
    
    if session=={}:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM customer")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('view_customer2.html',userDetails=userDetails)

@app.route('/delete_customer',methods=['post', 'get'])
def delete_customer():
    
    if session=={}:
        return redirect(url_for('login'))
    id=int(request.form.get('id'))
    cur = mysql.connection.cursor()
    resultValue = cur.execute("select * from customer where ws_ssn = %s",(id,))
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('delete_customer.html',userDetails=userDetails)

@app.route('/delete',methods=['post', 'get'])
def delete():
    
    if session=={}:
        return redirect(url_for('login'))
    id=int(request.form.get('id'))
    cur = mysql.connection.cursor()
    cur.execute('''delete from customer  where ws_ssn= %s''',(id,))
    mysql.connection.commit()
    return redirect(url_for('users'))

#For accounts
@app.route('/create_a')
def create_a():
    
    if session=={}:
        return redirect(url_for('login'))
    return render_template('create_account.html')
@app.route('/create_account', methods=['post', 'get'])
def create_account():
    
    if session=={}:
        return redirect(url_for('login'))
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
    
    if session=={}:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM account")
    if resultValue > 0:
        userDetails = cur.fetchall()
    return render_template('delete_account.html',accountDetails=userDetails)

@app.route('/delete_a', methods=['post', 'get'])
def delete_a():
    
    if session=={}:
        return redirect(url_for('login'))
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
#For Cashier
@app.route('/account_details')
def account_details():
    
    if session=={}:
        return redirect(url_for('login'))
    return render_template('account_details.html')
@app.route('/account_details')
def account_details():
    
    if session=={}:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM account")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('account_holders.html',userDetails=userDetails)
@app.route('/deposit_amount', methods=['post', 'get'])
def deposit_amount():
    
    if session=={}:
        return redirect(url_for('login'))
    id=request.form.get('id')
    print(id)
    cur = mysql.connection.cursor()
    resultValue = cur.execute("select * from account where ws_cust_id = %s",(id,))
    if resultValue > 0:
        users = cur.fetchall()
    return render_template('deposit_money.html',user=users)
@app.route('/deposit',methods=['post','get'])
def deposit():
    
    if session=={}:
        return redirect(url_for('login'))
    message=""
    id=int(request.form.get('id'))
    amount=int(request.form.get('deposit'))
    cur = mysql.connection.cursor()
    cur.execute("update account set ws_acct_balance=ws_acct_balance+cast(%s as decimal(16,2)) where ws_cust_id= %s",(amount,id,))
    mysql.connection.commit()
    resultValue = cur.execute("select * from account where ws_cust_id = %s",(id,))
    if resultValue > 0:
        userDetails = cur.fetchall()
        message="Amount deposited successfully"
    today = date.today()
    a_type=userDetails[0][2]
    balance=int(request.form.get('deposit'))
    cur.execute('''INSERT INTO `retailbanking`.`transactions` (`ws_cust_id` ,`ws_accnt_type` ,`ws_amt` ,`ws_trxn_date` ,`ws_src_typ` ,`ws_tgt_typ`)VALUES (%s, %s, %s, %s , %s , %s);''',(id,a_type,balance,today,a_type,a_type))
    mysql.connection.commit()
    return render_template('deposit_money.html',user=userDetails,message=message)
#for transfer
@app.route("/transfer", methods=['post', 'get'])
def transfer():
    if session=={}:
        return redirect(url_for('login'))
    return render_template("transfer_money.html")
@app.route("/transfer_amount", methods=['post', 'get'])
def transfer_amount():
    if session=={}:
        return redirect(url_for('login'))
    cust_id=int(request.form.get('id'))
    print(cust_id)
    tran_id=int(request.form.get('transfer_id'))
    amount=int(request.form.get('transfer'))
    cur = mysql.connection.cursor()
    result=cur.execute('''select * from account where ws_cust_id= %s''',(cust_id,))
    cust=cur.fetchall()
    result1=cur.execute('''select * from account where ws_cust_id= %s''',(tran_id,))
    trans=cur.fetchall()
    today = date.today()
    if result > 0:
        if result1 > 0:
            cust_after=cust[0][3]-amount
            print(trans)
            trans_after=trans[0][3]+amount
            cur.execute('''update account set ws_acct_balance=%s where ws_cust_id=%s''',(cust_after,cust_id,))
            mysql.connection.commit()
            cur.execute('''update account set ws_acct_balance=%s where ws_cust_id=%s''',(trans_after,tran_id,))
            mysql.connection.commit()
            type1=cust[0][2]
            cur.execute('''INSERT INTO `retailbanking`.`transactions` (`ws_cust_id` ,`ws_accnt_type` ,`ws_amt` ,`ws_trxn_date` ,`ws_src_typ` ,`ws_tgt_typ`)VALUES (%s, %s, %s, %s , %s , %s);''',(cust_id,type1,amount,today,type1,type1))
            mysql.connection.commit()
            type2=trans[0][2]
            cur.execute('''INSERT INTO `retailbanking`.`transactions` (`ws_cust_id` ,`ws_accnt_type` ,`ws_amt` ,`ws_trxn_date` ,`ws_src_typ` ,`ws_tgt_typ`)VALUES (%s, %s, %s, %s , %s , %s);''',(tran_id,type2,amount,today,type2,type2))
            mysql.connection.commit()
            message="Amount transfer completed successfully"
            return render_template('transfer_Details.html',message=message,cust=cust,trans=trans,cust_after=cust_after,trans_after=trans_after)

        else:
            message="Enter correct Target ID"
    else:
        message="Enter correct Customer ID"
    return render_template("transfer_money.html",message=message)
#for logout
@app.route('/logout',methods=['post','get'])
def logout():
    if session=={}:
        return redirect(url_for('login'))
    session.pop('username', None)
    print(session)
    return redirect(url_for('login'))
#for  customer search
@app.route('/csearch',methods=['post','get'])
def csearch():
    return render_template('customer_search.html')
@app.route('/customersearch',methods=['post','get'])
def customersearch():
    cust_id=request.form.get('cust-id')
    ssn_id=request.form.get('ssn-id')
    cur = mysql.connection.cursor()
    result=cur.execute('''select * from customer where ws_cust_id= %s or ws_ssn=%s''',(cust_id,ssn_id))
    if result>0:
        sample=cur.fetchall()
        return render_template('customer_detail.html',sample=sample)   
