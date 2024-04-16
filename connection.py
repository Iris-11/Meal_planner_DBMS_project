from flask import Flask, render_template,request, redirect, url_for, session
#Flask for- flask module
#render_template for- generating output based on Jinja2 
#request for- communication between client and server
from flask_mysqldb import MySQL,MySQLdb
# to communicate with MySQL db
import re


app = Flask(__name__)
app.secret_key = 'PSI515356'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Root556;'
app.config['MYSQL_DB'] = 'mealbuddy'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('login.html')  
         
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        userName = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            message = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        elif not userName or not password or not email:
            message = 'Please fill out the form!'
        else:
            cursor.execute(
                'INSERT INTO user (username, email, password) VALUES (%s, %s, %s)',
                (userName, email, password))
            mysql.connection.commit()
            message = 'You have successfully registered! Please login.'
            return redirect(url_for('login'))
    elif request.method == 'POST':
        message = 'Please fill out the form!'
    return render_template('signup.html', message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM user WHERE email = %s AND password = %s',
            (email, password))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['username'] = user['username']
            session['email'] = user['email']
            return redirect(url_for('dashboard'))
        else:
            message = 'Please enter correct email / password!'
    return render_template('login.html', message=message)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'loggedin' in session:
        if request.method == 'POST':
            age = request.form['age']
            height = request.form['height']
            weight = request.form['weight']
            gender = request.form['sex']
            # Update the user's information in the database
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'UPDATE user SET age = %s, height = %s, weight = %s, gender = %s WHERE userid = %s',
                (age, height, weight, gender, session['userid'])
            )
            mysql.connection.commit()
    return redirect(url_for('meal_planner'))

@app.route('/meal_planner', methods=['GET', 'POST'])
def meal_planner():
    if request.method == 'POST':
        note = request.form.get('note')
        veg_non = request.form.get('veg/non')
        return redirect(url_for('select_recipes',veg_non=veg_non))
    else:
        return render_template('meal_planner.html')

@app.route('/select_recipes/<veg_non>', methods=['GET', 'POST'])
def select_recipes(veg_non):
    if veg_non=='veg':
        VN = 'V'
        searchQueryBf = "SELECT RecipeName,RecipeID from recipe WHERE tag='B' AND  vegNon = %s ORDER BY RecipeName"
        searchQueryLunch = "SELECT RecipeName,RecipeID from recipe WHERE tag='L/D' AND  vegNon = %s ORDER BY RecipeName"
        searchQueryDinner = "SELECT RecipeName,RecipeID from recipe WHERE tag='L/D' AND  vegNon = %s ORDER BY RecipeName"
        searchQuerySnack = "SELECT RecipeName,RecipeID from recipe WHERE tag='S' AND  vegNon = %s ORDER BY RecipeName"
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(searchQueryBf,VN)
        bfRecipes = cur.fetchall()

        cur.execute(searchQueryLunch,VN)
        lunchRecipes = cur.fetchall()

        cur.execute(searchQueryDinner,VN)
        dinnerRecipes = cur.fetchall()

        cur.execute(searchQuerySnack,VN)
        snackRecipes = cur.fetchall()
    else:
        searchQueryBf = "SELECT RecipeName,RecipeID from recipe WHERE tag='B' ORDER BY RecipeName"
        searchQueryLunch = "SELECT RecipeName,RecipeID from recipe WHERE tag='L/D' ORDER BY RecipeName"
        searchQueryDinner = "SELECT RecipeName,RecipeID from recipe WHERE tag='L/D' ORDER BY RecipeName"
        searchQuerySnack = "SELECT RecipeName,RecipeID from recipe WHERE tag='S' ORDER BY RecipeName"
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
        cur.execute(searchQueryBf)
        bfRecipes = cur.fetchall()

        cur.execute(searchQueryLunch)
        lunchRecipes = cur.fetchall()

        cur.execute(searchQueryDinner)
        dinnerRecipes = cur.fetchall()
        

        cur.execute(searchQuerySnack)
        snackRecipes = cur.fetchall()
    
    return render_template('select_recipes.html',bfRecipes=bfRecipes,lunchRecipes=lunchRecipes,dinnerRecipes=dinnerRecipes,snackRecipes=snackRecipes)

@app.route('/submit_schedule',methods=['GET', 'POST'])
def submit_schedule():
    UID = session.get('userid')
    print(UID)
    date = request.form.get('date')
    bfRID = request.form.get('breakfast')
    lRID = request.form.get('lunch')
    dRID = request.form.get('dinner')
    sRID = request.form.get('Snack')
    print("bfRID:", bfRID)
    print("lRID:", lRID)
    print("dRID:", dRID)
    print("sRID:", sRID)

    print("Form data:", request.form)


    
    searchQueryBf = "INSERT INTO meal(UserID,RecipeID,date,time) VALUES(%s,%s,%s,'B')"
    searchQueryLunch = "INSERT INTO meal(UserID,RecipeID,date,time) VALUES(%s,%s,%s,'L')"
    searchQueryDinner = "INSERT INTO meal(UserID,RecipeID,date,time) VALUES(%s,%s,%s,'D')"
    searchQuerySnack = "INSERT INTO meal(UserID,RecipeID,date,time) VALUES(%s,%s,%s,'S')"
    

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    message = "Schedule added!"
    try:
        cur.execute(searchQueryBf,(UID,bfRID,date))

        cur.execute(searchQueryLunch,(UID,lRID,date))

        cur.execute(searchQueryDinner,(UID,dRID,date))

        cur.execute(searchQuerySnack,(UID,sRID,date))
        print("Inserted into meal table")
        cur.close()
        mysql.connection.commit()
    except:
        message = "This schedule already exists"

    return render_template('meal_planner.html',message=message) 


if __name__ == '__main__':
    app.run(debug=True)
