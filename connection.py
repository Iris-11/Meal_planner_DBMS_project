from flask import Flask, render_template,request, redirect, url_for
#Flask for- flask module
#render_template for- generating output based on Jinja2 
#request for- communication between client and server
from flask_mysqldb import MySQL,MySQLdb
# to communicate with MySQL db


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Root556;'
app.config['MYSQL_DB'] = 'mealbuddy'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')


# Route to handle form submission
@app.route('/get_shopping_list', methods=['POST','GET'])
def get_shopping_list():
    selected_recipes = request.form.getlist('recipe')
    # Process selected recipes and generate shopping list
    # Here, you can perform any required database operations or calculations
    # to generate the shopping list based on the selected recipes
    shopping_list = []
    for recipe_name in selected_recipes:
        # Fetch recipe details from database and add to shopping list
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM ingredient WHERE IngName = %s", (recipe_name,))
        recipe_data = cur.fetchone()
        shopping_list.append(recipe_data)
        cur.close()
    return render_template('shopping_list.html', shopping_list=shopping_list)

'''
@app.route('/meal_planner',methods=['POST','GET'])
def search():
    veg_non = 'nonveg'
    if request.method == 'POST':
        veg_non = request.form.get('veg/non')  

    if veg_non=='veg':
        VN = 'V'
    else:
        VN = 'N'

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    searchQueryBf = "SELECT RName from recipe WHERE tag='B' AND  vegNon = %s ORDER BY RName"
    searchQueryLunch = "SELECT RName from recipe WHERE tag='L/D' AND  vegNon = %s ORDER BY RName"
    searchQueryDinner = "SELECT RName from recipe WHERE tag='L/D' AND  vegNon = %s ORDER BY RName"
    searchQuerySnack = "SELECT RName from recipe WHERE tag='S' AND  vegNon = %s ORDER BY RName"
    cur.execute(searchQueryBf,VN)
    bfRecipes = cur.fetchall()

    cur.execute(searchQueryLunch,VN)
    lunchRecipes = cur.fetchall()

    cur.execute(searchQueryDinner,VN)
    dinnerRecipes = cur.fetchall()

    cur.execute(searchQuerySnack,VN)
    snackRecipes = cur.fetchall()


    
    return render_template('meal_planner.html',bfRecipes=bfRecipes,lunchRecipes=lunchRecipes,dinnerRecipes=dinnerRecipes,snackRecipes=snackRecipes)
'''
@app.route('/meal_planner', methods=['GET', 'POST'])
def meal_planner():
    if request.method == 'POST':
        date = request.form.get('date')
        note = request.form.get('note')
        veg_non = request.form.get('veg/non')
        return redirect(url_for('select_recipes', veg_non=veg_non))
    else:
        return render_template('meal_planner.html')

@app.route('/select_recipes/<veg_non>', methods=['GET', 'POST'])
def select_recipes(veg_non):
    if veg_non=='veg':
        VN = 'V'
        searchQueryBf = "SELECT RName from recipe WHERE tag='B' AND  vegNon = %s ORDER BY RName"
        searchQueryLunch = "SELECT RName from recipe WHERE tag='L/D' AND  vegNon = %s ORDER BY RName"
        searchQueryDinner = "SELECT RName from recipe WHERE tag='L/D' AND  vegNon = %s ORDER BY RName"
        searchQuerySnack = "SELECT RName from recipe WHERE tag='S' AND  vegNon = %s ORDER BY RName"
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
        searchQueryBf = "SELECT RName from recipe WHERE tag='B' ORDER BY RName"
        searchQueryLunch = "SELECT RName from recipe WHERE tag='L/D' ORDER BY RName"
        searchQueryDinner = "SELECT RName from recipe WHERE tag='L/D' ORDER BY RName"
        searchQuerySnack = "SELECT RName from recipe WHERE tag='S' ORDER BY RName"
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



if __name__ == '__main__':
    app.run(debug=True)
