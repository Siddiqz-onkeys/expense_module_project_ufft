import mysql.connector
from datetime import datetime 
from flask import Flask,request,render_template,jsonify,redirect,url_for
import os
from werkzeug.utils import secure_filename

## initializing the flask application
app=Flask(__name__)


########## DEFINING A PATH TO SAVE THE UPLOADED FILES ##########
UPLOAD_FOLDER = 'static/uploads/receipts'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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



########### ESTABLISHING A ROUTE FOR THE HTML REQUEST ##########

@app.route('/') #creates a root route for the flask application
 #index function that returnrs the HTML content from the file and sends it to the user as a response for accessing the root URL
def index():
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    cursor.execute("SELECT expense_id,date,name,amount,description,receipt FROM expenses e1 JOIN categories c1 where e1.category_id=c1.category_id ORDER BY expense_id DESC")
    expenses=cursor.fetchall()
    
    expense_records=[
        {
            'expense_id':exp[0],
            'date_in':exp[1],
            'category':exp[2],            
            'amount':exp[3],
            'desc':exp[4],
            'receipt':exp[5]            
        }
        for exp in expenses
    ]
    return render_template('index.html', expenses=expense_records, max_date=current_date) #Flask by default looks for templkate forlder to render the html file


########## SAVING THE UPLOADED FILES IN A FOLDER ############
@app.route('/upload_receipt', methods=['POST'])
def upload_receipt():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))


###### getting the form data and calling the add expense function
@app.route('/get_form_data',methods=['POST'])
def get_form_data():
    
    user_id=1
    
    family_id=1
    
    category=request.form.get('category')
    #print("Category being queried:", category)

    cursor.execute("SELECT category_id FROM categories WHERE name=%s",(category,))
    res=cursor.fetchone()
    category_id=res[0]
    
    
    date_in=request.form.get('date')
    #print(date_in)
        
    amount=float(request.form.get('amount'))
    #print(amount)
    
    description=request.form.get('desc')
    if not description :
        description=""
    #print(description)
        
    # Handle the receipt file upload
    receipt_file = request.files['file']
    receipt_filename = None
    receipt=""
    if receipt_file:
        receipt_filename = secure_filename(receipt_file.filename)
        receipt_file.save(os.path.join(app.config['UPLOAD_FOLDER'], receipt_filename))
        receipt = receipt_filename
    
    # Add the expense to the database
    add_expense(user_id, family_id, category_id, amount, date_in, description, receipt)
    
    return redirect(url_for('index')) ##### this returns a success message 


####### ADD EXPENSE ###########
def add_expense(user_id,family_id,category_id,amount,date_in,description,receipt):
   
    cursor.execute("INSERT INTO EXPENSES (user_id,category_id,date,amount,description,family_id,receipt) VALUES (%s,%s,%s,%s,%s,%s,%s)",(user_id,category_id,date_in,amount,description,family_id,receipt,))
    connect_.commit() #reflects in our database
   
   
########## DELETE EXPENSE  #######
@app.route('/delete_expense/<int:expense_id>',methods=["POST"])
def delete_expense(expense_id):
    cursor.execute("DELETE FROM expenses WHERE expense_id=%s",(expense_id,))
    connect_.commit()
    return redirect(url_for('index'))


############ EDIT EXPENSE #######
@app.route('/edit_expense/<int:expense_id>', methods=["POST"])
def edit_expense(expense_id):
    ##### old values ####
    cursor.execute("SELECT amount,date,category_id,description,receipt FROM expenses WHERE expense_id=%s",(expense_id,))
    res=cursor.fetchone()
    old_amount=res[0]
    old_date=res[1]
    old_cat_id=res[2]
    cursor.execute("SELECT name FROM categories WHERE category_id=%s",(old_cat_id,))
    old_cat=cursor.fetchone()[0]
    old_desc=res[3]
    old_receipt=res[4]
    
    #### fetching new values fromthe form
    new_amount=request.form.get('amount')
    if not new_amount:
        new_amount=old_amount
        
    new_date=request.form.get('date')
    if not new_date:
        new_date=old_date
        
    new_category=request.form.get('category')
    if not new_category:
        new_category=old_cat
    
    cursor.execute("SELECT category_id FROM categories WHERE name=%s",(new_category,))
    new_cat_id=cursor.fetchone()[0]
    
    new_desc=request.form.get('desc')
    
    new_receipt = request.files['file']
    new_receipt_filename = None
    receipt = None  # Initialize receipt

    if new_receipt:
        new_receipt_filename = secure_filename(new_receipt.filename)
        new_receipt.save(os.path.join(app.config['UPLOAD_FOLDER'], new_receipt_filename))
        receipt = new_receipt_filename
        
        # Check if old_receipt is valid and different from new receipt
        if old_receipt and receipt != old_receipt:
            old_receipt_path = os.path.join(app.config['UPLOAD_FOLDER'], old_receipt)
            if os.path.exists(old_receipt_path):  # Ensure old_receipt_path is valid
                os.remove(old_receipt_path)

    else:
        receipt = old_receipt  # Keep the old receipt if no new file is uploaded

        
    cursor.execute("UPDATE expenses SET category_id=%s,amount=%s,description=%s,date=%s,receipt=%s WHERE expense_id=%s",(new_cat_id,new_amount,new_desc,new_date,receipt,expense_id,))
    connect_.commit()
    return redirect(url_for('index'))
           

###### ADD AMOUNT #####    
@app.route('/add_amount/<int:expense_id>',methods=["POST"])
def add_amount(expense_id):
    cursor.execute("SELECT amount FROM expenses WHERE expense_id=%s",(expense_id,))
    old_amount=cursor.fetchone()[0]
    
    new_amount=request.form.get('add_amount')
    sum=float(new_amount)+float(old_amount)
    
    cursor.execute("UPDATE expenses SET amount=%s WHERE expense_id=%s",(sum,expense_id,))
    connect_.commit()
    return redirect(url_for('index'))


@app.route('/sort_expenses', methods=["GET"])
def sort_expenses():
    sort_by = request.form.get('sort_by')  # Get sorting criterion from the frontend ('amount' or 'date')
    sort_order = request.form.get('sort_order')  # Get sorting order ('asc' or 'desc')
    
    if sort_by not in ['amount', 'date']:
        sort_by = 'date'  # Default to 'date' if invalid input is provided

    if sort_order not in ['asc', 'desc']:
        sort_order = 'asc'  # Default to ascending if invalid input is provided

    query = f"SELECT * FROM expenses ORDER BY {sort_by} {sort_order.upper()}"
    cursor.execute(query)
    sorted_expenses = cursor.fetchall()
    
    # Return the sorted expenses data for rendering on the frontend
    return render_template('index.html', expenses=sorted_expenses)

@app.route('/filter_expenses', methods=["GET"])
def filter_expenses():
    min_amount = request.args.get('filter_amount_range_min')  # Minimum amount input from the frontend
    max_amount = request.args.get('filter_amount_range_max')  # Maximum amount input from the frontend
    category = request.args.get('filter_category')  # Category input from the frontend
    print("called")

    # Initialize base query and parameters
    query = "SELECT e.expense_id,e.date,c.name,e.amount,e.description,e.receipt FROM expenses e JOIN categories c ON e.category_id = c.category_id WHERE "
    params = []

    # Filter by amount range if both min and max values are provided and also category
    if min_amount and max_amount and category:
        query=query+"c.name=%s AND e.amount BETWEEN %s AND %s "
        params+=[category,min_amount,max_amount]

    # Filter by category if a valid category is provided but not min and max
    elif category and not max_amount and not min_amount:
        query=query+" LOWER(c.name) = %s"
        params.append(category.lower())
    
    #category and min value is given
    elif category and min_amount and not max_amount:
        query+="c.name=%s AND e.amount>=%s"
        params+=([category.lower(),min_amount])
    
    #max and min given but not category
    elif max_amount and  min_amount and not category:
        query+="e.amount BETWEEN %s AND %s"
        params+=([min_amount,max_amount])
    
    # only min amount
    elif min_amount and not max_amount and not category:
        query+="e.amount<=%s"
        params+=([min_amount])
    
    #only max amount
    elif max_amount and not max_amount and not category:
        query+="e.amount>=%s"
        params+=([max_amount])

    #category and min amount
    else:
        query+="c.name=%s AND e.amount<=%s"
        params+=([category.lower(),max_amount])

    
    
    
    cursor.execute(query, tuple(params))
    filtered_expenses = cursor.fetchall()
    
    filtered_expenses_list=[
        {
            'expense_id':exp[0],
            'date_in':exp[1],
            'category':exp[2],            
            'amount':exp[3],
            'desc':exp[4],
            'receipt':exp[5]            
        }
        for exp in filtered_expenses
    ]
    
    current_date = datetime.now().strftime('%Y-%m-%d')
    return render_template('index.html', expenses=filtered_expenses_list, max_date=current_date)

###### route to reset the view ########
@app.route('/reset_filters')
def reset_filters():
    # Redirect to the root route, where the unfiltered data is displayed
    return redirect('/')



if __name__=="__main__":
    app.run(debug=True)
