from flask import Flask, jsonify,request, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, DateField,IntegerField,FloatField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import uuid
import datetime as dt
from flask_cors import CORS



#print(uuid.uuid4())
app = Flask(__name__) #creating the Flask class object 
CORS(app, resources={r"/product/*": {"origins": "http://127.0.0.1:5000"}})




# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] =''
app.config['MYSQL_DB'] = 'peams'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

# Index
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
     return render_template('about.html')    

# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

    # User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

         # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO admin(admin_name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')


         
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM admin WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')

# Inventory Form Class
class InventoryForm(Form):
    inventory_id= StringField('inventory_id', [validators.Length(min=1, max=50)])
    quantity= IntegerField('quantity')
    brand= StringField('brand', [validators.Length(min=4, max=50)])
    category= StringField('category', [validators.Length(min=4, max=50)])
    expiry_date= DateField('expiry date', format='%Y-%m-%d', default=dt.datetime.now())
    shelf_no= StringField('shelf_no', [validators.Length(min=4, max=50)])
    

    # inventory
@app.route('/inventory/add', methods=['GET', 'POST'])
def inventory():
    form = InventoryForm(request.form)
    if request.method == 'POST':
        inventory_id = uuid.uuid4()
        quantity = form.quantity.data
        brand = form.brand.data
        category = form.category.data
        expiry_date= form.expiry_date.data
        shelf= form.shelf_no.data
        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO inventory VALUES(%s, %s, %s, %s, %s, %s)", (inventory_id,quantity,brand, category, expiry_date, shelf))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('New batch added', 'success')


         
        return redirect(url_for('dashboard'))
    return render_template('inventory.html', form=form)

# Product Form Class
class ProductForm(Form):
    
    product_name= StringField('product name',[validators.Length(min=4, max=50)])
    description= StringField('description', [validators.Length(min=4, max=50)])
    price= FloatField('price')
    inv_id= StringField('inventory Id',[validators.Length(min=4, max=50)])


    # Product
@app.route('/product/add', methods=['GET', 'POST'])
def product():
    form = ProductForm(request.form)
    if request.method == 'POST':
        product_id = uuid.uuid4()
        product_name= form.product_name.data
        description = form.description.data
        price= form.price.data
        inventory_id= form.inv_id.data
        

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO product VALUES(%s ,%s, %s, %s, %s)", (product_id,product_name,description,price,inventory_id))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('New product added', 'success')


         
        return redirect(url_for('dashboard'))
    return render_template('product.html', form=form)

@app.route('/product/get/allProducts', methods=['GET'])
def product_summary():
    # Create cursor
    cur = mysql.connection.cursor()

    # Query to get total number of products
    # TODO: Check if not expired
    cur.execute("SELECT COUNT(*) AS product_count FROM product")
    total_products = cur.fetchone()
    print(f"Total products : {total_products}")

    product = {
        "no_of_products":total_products
    }

    return jsonify(product)

@app.route('/product/get/productExpiringsoon', methods=['GET'])
def product_expiringsoon():
    # Create cursor
    cur = mysql.connection.cursor()

    # Query to get total number of products
    cur.execute("SELECT COUNT(*) AS product_count FROM inventory WHERE expiry_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 1 MONTH)")
    product_expiringsoon = cur.fetchone()
    print(f"Products Expiringsoon : {product_expiringsoon}")

    product = {
        "no_of_products":product_expiringsoon
    }

    return jsonify(product)

@app.route('/product/get/expiredProducts', methods=['GET'])
def expired_products():
    # Create cursor
    cur = mysql.connection.cursor()

    # Query to get total number of expired products
    cur.execute("SELECT COUNT(*) AS product_count FROM inventory WHERE expiry_date < CURDATE()")
    expired_products = cur.fetchone()
    print(f"Expired Products: {expired_products}")

    product = {
        "no_of_products": expired_products
    }

    return jsonify(product)

@app.route('/product/get/datePicker', methods=['POST'])
def date_picker():
    data = request.get_json()
    months = data.get('months')
    weeks = data.get('weeks')
    days = data.get('days')
    hours = data.get('hours')
    date = data.get('date')

    cur = mysql.connection.cursor()

    query = ""
    
    if months:
        query = """
        SELECT  
        `product`.`product_id`,
        `product`.`product_name`,
        `product`.`price`,
        `inventory`.`expiry_date` 
        FROM 
            `product`
        INNER JOIN 
            `inventory` 
        ON  
            `product`.`inventory_id` = `inventory`.`inventory_id`
        WHERE 
            `inventory`.`expiry_date` <= DATE_ADD(NOW(), INTERVAL %s MONTH);

        """
        cur.execute(query, (months,))
        products = cur.fetchall()
        product_list={
            "months":months,
            "no_of_products":len(products),
            "search_result":products
        }
        return jsonify(product_list)
    
    elif weeks:
        query = """
                SELECT 
                `product`.`product_id`, 
                `product`.`product_name`, 
                `product`.`price`, 
                `inventory`.`expiry_date` 
            FROM 
                `product` 
            INNER JOIN 
                `inventory` 
            ON 
                `product`.`inventory_id` = `inventory`.`inventory_id` 
            WHERE 
                `inventory`.`expiry_date` BETWEEN DATE_SUB(CURDATE(), INTERVAL %s WEEK) AND CURDATE();
            """
        cur.execute(query, (weeks,))
        products = cur.fetchall()
        product_list={
            "weeks":weeks,
            "no_of_products":len(products),
            "search_result":products
        }
        return jsonify(product_list)
    elif days:
        query = """
                SELECT  
        `product`.`product_id`,
        `product`.`product_name`,
        `product`.`price`,
        `inventory`.`expiry_date` 
        FROM 
            `product`
        INNER JOIN 
            `inventory` 
        ON  
            `product`.`inventory_id` = `inventory`.`inventory_id`
        WHERE 
            `inventory`.`expiry_date` <= DATE_ADD(NOW(), INTERVAL %s DAY);
            """
        cur.execute(query, (days,))
        products = cur.fetchall()
        product_list={
            "days":days,
            "no_of_products":len(products),
            "search_result":products
        }
        return jsonify(product_list)
    elif hours:
        query = """
                SELECT  
        `product`.`product_id`,
        `product`.`product_name`,
        `product`.`price`,
        `inventory`.`expiry_date` 
        FROM 
            `product`
        INNER JOIN 
            `inventory` 
        ON  
            `product`.`inventory_id` = `inventory`.`inventory_id`
        WHERE 
            `inventory`.`expiry_date` <= DATE_ADD(NOW(), INTERVAL %s HOUR);
            """
        cur.execute(query, (hours,))
        products = cur.fetchall()
        product_list={
            "hours":hours,
            "no_of_products":len(products),
            "search_result":products
        }
        return jsonify(product_list)
    elif date:
        query = """
                SELECT p.*, i.expiry_date FROM inventory i
                JOIN product p ON i.inventory_id = p.inventory_id
                WHERE i.expiry_date <= %s
            """
        cur.execute(query, (date,))
        products = cur.fetchall()
        product_list={
            "date":date,
            "no_of_products":len(products),
            "search_result":products
        }
        return jsonify(product_list)
    
@app.route('/product/get/counts', methods=['GET'])
def product_counts():
    # Create cursor
    cur = mysql.connection.cursor()

    # Query to get total number of products
    # TODO: Check if not expired
    cur.execute("SELECT SUM(quantity) AS qty,category FROM inventory GROUP BY category;")
    product_list = cur.fetchall()
    

    products = {
        "chart_products":product_list
    }

    return jsonify(products)

@app.route('/product/get/counts/expiry', methods=['GET'])
def product_chart_expiry():
    # Create cursor
    cur = mysql.connection.cursor()

    # Query to get total number of products
    # TODO: Check if not expired
    cur.execute("SELECT SUM(quantity) AS qty,category FROM inventory  WHERE expiry_date BETWEEN CURRENT_DATE() AND DATE_ADD(CURRENT_DATE(), INTERVAL 30 DAY) GROUP BY category;")
    product_list = cur.fetchall()
    

    products = {
        "chart_products":product_list
    }

    return jsonify(products)

@app.route('/product/get/counts/expired', methods=['GET'])
def product_chart_expired():
    # Create cursor
    cur = mysql.connection.cursor()

    # Query to get total number of products
    # TODO: Check if not expired
    cur.execute("SELECT brand ,SUM(quantity) as qty FROM inventory  WHERE expiry_date<CURRENT_DATE() GROUP BY brand;")
    product_list = cur.fetchall()
    

    products = {
        "chart_products":product_list
    }

    return jsonify(products)


@app.route('/product/get/counts/months/products', methods=['GET'])
def product_chart_months():
    # Create cursor
    cur = mysql.connection.cursor()

    # Query to get total number of products
    # TODO: Check if not expired
    cur.execute("SELECT DATE_FORMAT(expiry_date, '%M') AS month,SUM(quantity) AS qty FROM inventory WHERE expiry_date <= DATE_ADD(CURRENT_DATE(), INTERVAL 1 YEAR) GROUP BY DATE_FORMAT(expiry_date, '%M') ORDER BY DATE_FORMAT(expiry_date, '%m');")
    product_list = cur.fetchall()
    

    products = {
        "chart_products":product_list
    }

    return jsonify(products)

@app.route('/product/get/layout', methods=['GET'])
def productlayout():
    # Create cursor
    cur = mysql.connection.cursor()

    # Query to get total number of products
    # TODO: Check if not expired
    cur.execute("SELECT shelf FROM inventory WHERE expiry_date<CURRENT_DATE() GROUP BY category;")
    product_list = cur.fetchall()
    

    products = {
        "chart_products":product_list
    }

    return jsonify(products)

@app.route('/product/get/layout/shelf-approved', methods=['GET'])
def product_shelfed():
    # Create cursor
    cur = mysql.connection.cursor()

    # Query to get total number of products
    # TODO: Check if not expired
    cur.execute("SELECT shelf FROM inventory WHERE expiry_date>CURRENT_DATE() GROUP BY category;")
    product_list = cur.fetchall()
    

    products = {
        "chart_products":product_list
    }

    return jsonify(products)
                  
                    
        


if __name__ =='__main__':
    app.secret_key='secret123'  
    app.run(debug = True) 