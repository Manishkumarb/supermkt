from flask import Flask,render_template,request
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_USER'] = 'manish084'
app.config['MYSQL_PASSWORD'] = '8971072980'
app.config['MYSQL_DB'] = 'supermarket'
app.config['MYSQL_HOST'] = 'localhost'
mysql=MySQL(app)

@app.route('/',methods=['GET','POST'])
def index():
	if request.method=='POST':
		details=request.form
		name=details['username']
		password=details['password']
		cur=mysql.connection.cursor()	
		cur.execute('''SELECT * from admin''')
		data=cur.fetchall()
		cur.execute('''SELECT * from category''')
		data1=cur.fetchall()
		if data[0][0]==name and data[0][1]==password:
			return render_template('home.html',data=data1)
	return render_template('index.html')



@app.route('/emp')
def emp():
	cur=mysql.connection.cursor()
	cur.execute('''call getallemp()''')	
	data=cur.fetchall()
	return render_template('emp.html',data=data)

@app.route('/customers')
def customers():
	cur=mysql.connection.cursor()	
	cur.execute('''SELECT * from customers''')
	data=cur.fetchall()
	return render_template('customers.html',data=data)


@app.route('/home')
def home():
	cur=mysql.connection.cursor()	
	cur.execute('''SELECT * from category''')
	data=cur.fetchall()
	return render_template('home.html',data=data)

@app.route('/Grocery')
def grocery():
	cur=mysql.connection.cursor()	
	cur.execute('''SELECT * from item where cat_id=2''')
	data=cur.fetchall()
	return render_template('Grocery.html',data=data)

@app.route('/Beauty_Products')
def beauty():
	cur=mysql.connection.cursor()	
	cur.execute('''SELECT * from item where cat_id=3''')
	data=cur.fetchall()
	return render_template('Beauty_Products.html',data=data)

@app.route('/Sports_items')
def sports():
	cur=mysql.connection.cursor()	
	cur.execute('''SELECT * from item where cat_id=6''')
	data=cur.fetchall()
	return render_template('Sports_items.html',data=data)

@app.route('/Books')
def books():
	cur=mysql.connection.cursor()	
	cur.execute('''SELECT * from item where cat_id=1''')
	data=cur.fetchall()
	return render_template('Books.html',data=data)

	

@app.route('/Snacks')
def snacks():
	cur=mysql.connection.cursor()	
	cur.execute('''SELECT * from item where cat_id=4''')
	data=cur.fetchall()
	return render_template('Snacks.html',data=data)

@app.route('/Household_Essentials')
def household():
	cur=mysql.connection.cursor()	
	cur.execute('''SELECT * from item where cat_id=5''')
	data=cur.fetchall()
	return render_template('Household_Essentials.html',data=data)

@app.route('/insert_emp',methods=['GET','POST'])
def insert_emp():
	if request.method=='POST':
		details=request.form
		name=details['name']
		email=details['email']
		phone=details['phone']
		salary=details['salary']
		date=details['date']
		address=details['address']
		
		cur=mysql.connection.cursor()	
		cur.execute('''select max(emp_id) from employee''')
		empid=cur.fetchone()
		cur.execute('''INSERT INTO employee (name, emp_id,phone,date_start ,address ,salary ,email_id) VALUES( %s, %s ,%s ,%s, %s, %s, %s)''',(name,empid[0]+1,phone,date,address,salary,email)) 
		mysql.connection.commit()
		cur.execute('''SELECT * from employee''')
		data=cur.fetchall()
		return render_template('emp.html',data=data)

		
	return render_template('insert_emp.html',)

@app.route('/statistics')
def statistics():
	total=[]
	cur=mysql.connection.cursor()	
	cur.execute('''select emp_total_sal from admin''')
	total_sal=str(cur.fetchone())
	total.append(total_sal[1:7])
	cur.execute('''select sum(price) from orders''')
	total_ord=str(cur.fetchone())
	total.append(total_ord[10:-4])
	cur.execute('''select sum(price*quantity) from item''')
	total_stock=str(cur.fetchone())
	total.append(total_stock[10:-4])
	return render_template('statistics.html',data=total)

@app.route('/sales',methods=['GET','POST'])
def sales():
	cur=mysql.connection.cursor()
	cur.execute('''select * from orders''')
	data=cur.fetchall()
	return render_template('sales.html',data=data)

@app.route('/insert_item',methods=['GET','POST'])
def insert_item():
	if request.method=='POST':
		details=request.form
		name=details['name']
		price=details['price']
		quantity=details['quantity']
		url=details['url']
		cat_id=details['cat_id']
		
		cur=mysql.connection.cursor()	
		cur.execute('''select max(item_id) from item''')
		itemid=cur.fetchone()
		cur.execute('''INSERT INTO item (item_id,item_name,cat_id ,price,item_url,quantity) VALUES( %s, %s ,%s ,%s, %s, %s)''',(itemid[0]+1,name,cat_id,price,url,quantity)) 
		mysql.connection.commit()
		cur.execute('''SELECT * from category''')
		data=cur.fetchall()
		return render_template('home.html',data=data)
		

	return render_template('insert_item.html')


@app.route('/orders',methods=['GET', 'POST'])
def orders():	
	if request.method=='POST':
		details=request.form
		order_id=details['order_id']
		item_id=details['item_id']
		cust_id=details['cust_id']
		quantity=details['quantity']
		price=details['price']
		date=details['date']
		emp_id=details['emp_id']
		cur=mysql.connection.cursor()
		cur.execute('SELECT quantity from item where item_id= %s',(item_id,))
		value=str(cur.fetchone())
		value=value[1:-2]
		if value<quantity:
			return "error"
		else:	
			
			cur.execute('''INSERT INTO orders (ord_id,cust_id,item_id ,quantity,price,ord_date,emp_id) VALUES( %s, %s ,%s ,%s, %s, %s,%s)''',(order_id,cust_id,item_id,quantity,price,date,emp_id)) 
			mysql.connection.commit()
			return render_template('orders.html')


	cur=mysql.connection.cursor()	
	cur.execute('''select * from customers''')
	data=cur.fetchall()
	cur.execute('''select * from employee''')
	data1=cur.fetchall()
	return render_template('orders.html',data=data,data1=data1)


@app.route('/order_home')
def order_home():
	return render_template('order_home.html')


@app.route('/insert_cust',methods=['GET', 'POST'])
def insert_cust():
	if request.method=='POST':
		details=request.form
		name=details['name']
		phone=details['phone']
		address=details['address']
		cur=mysql.connection.cursor()	
		cur.execute('''select max(customer_id) from customers''')
		customer_id=cur.fetchone()
		cur.execute('''INSERT INTO customers (customer_id,cust_name,phone,address ) VALUES( %s, %s ,%s ,%s)''',(customer_id[0]+1,name,phone,address)) 
		mysql.connection.commit()
	return render_template('insert_cust.html')

@app.route('/about')
def about():
	
	return render_template('about.html')

@app.route('/services')
def services():
	
	return render_template('services.html')

@app.route('/contact')
def contact():
	
	return render_template('contact.html')


if (__name__ == "__main__"):
	app.run(debug=True)
