import mysql.connector
from datetime import datetime 
from flask import Flask,request,render_template,jsonify

## initializing the flask application
app=Flask(__name__)

#configuring the connection with the database

db_config={
    'host':'localhost',
    'user':'root',
    'password':'$9Gamb@098',
    'database':'project_ufft',
    'port':3306
}

#establishing a conenction with the database using the configuration
connect_=mysql.connector.connect(**db_config)
cursor=connect_.cursor()

########### ESTABLISHING A ROUTE FOR THE HTML REQUEST

@app.route('/') #creates a root route for the flask application
 #index function that returnrs the HTML content from the file and sends it to the user as a response for accessing the root URL
def index():
    current_date = datetime.now().strftime('%Y-%m-%d')
    return render_template('index.html', max_date=current_date) #Flask by default looks for templkate forlder to render the html file



###### getting the form data and calling the add expense function
@app.route('/add_expense',methods=['POST'])
def get_form_data():
    print("called it")
    user_id=1
    
    family_id=1
    
    category=request.form.get('category')
    print("Category being queried:", category)

    cursor.execute("SELECT category_id FROM categories WHERE name=%s",(category,))
    res=cursor.fetchone()
    category_id=res[0]
    
    
    date_in=request.form.get('date')
    print(date_in)
        
    amount=float(request.form.get('amount'))
    print(amount)
    
    description=request.form.get('desc')
    if not description :
        description="null"
    print(description)
    
    add_expense(user_id,family_id,category_id,amount,date_in,description)
    
    return jsonify ( {'message': ' New expense sucessfully added into your records!!!!!!!'} ) ##### this returns a success message 
####### ADD EXPENSE 

def add_expense(user_id,family_id,category_id,amount,date_in,description):
   
    cursor.execute("INSERT INTO EXPENSES (user_id,category_id,date,amount,description,family_id) VALUES (%s,%s,%s,%s,%s,%s)",(user_id,category_id,date_in,amount,description,family_id,))
    connect_.commit() #reflects in our database
    



if __name__=="__main__":
    app.run(debug=True)