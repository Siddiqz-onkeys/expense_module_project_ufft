import mysql.connector
from datetime import datetime
from flask import Flask,request,render_template,jsonify,redirect,url_for
import os,time
from werkzeug.utils import secure_filename
import smtplib

db_config={
    'host':'localhost',
    'user':'root',
    'password':'$9Gamb@098',
    'database':'project_ufft',
    'port':3306
}


GMAIL_ID='dum31555@gmail.com'
GMAIL_PSWD='dweg wzyz mbfa wvkv'

def sendEmail(to, sub, msg):
    print(f"Email to {to} sent with sub:{sub} and message {msg}")
    s=smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(GMAIL_ID,GMAIL_PSWD)
    s.sendmail(GMAIL_ID, to, f"Subject: {sub}\n\n{msg}")
    s.quit()


#establishing a conenction with the database using the configuration
connect_=mysql.connector.connect(**db_config)
cursor=connect_.cursor()
curr_date=datetime.now()
cursor.execute("""
SELECT 
    users.user_name, 
    users.email, 
    recc_expenses.amount, 
    recc_expenses.description,
    recc_expenses.start_date,
    recc_expenses.end_date 
FROM 
    users 
JOIN 
    recc_expenses 
ON 
    users.user_id = recc_expenses.user_id 
WHERE 
    CONCAT(MONTH(start_date), '-', DAY(start_date)) 
    BETWEEN CONCAT(MONTH(CURDATE()), '-', DAY(CURDATE())) 
    AND CONCAT(MONTH(CURDATE()), '-', DAY(CURDATE() + INTERVAL 3 DAY));
""")
res = cursor.fetchall()

recs=[{
    'user_name':exp[0],
    'email':exp[1],
    'amount':exp[2],
    'description':exp[3],
    'start_date':exp[4],
    'end_date':exp[5]
}for exp in res]
subject="remainder for the upcoming reccuring expense"
 ########################### SHOULD CHANGE THE CODE TO ADD A NEW RECCURING EXPENSE AND ALSO RECC TO EXPENSES AS WELL.
 ########################### SHOULD CHECK IF THERE IS AN END DATE -- IF THERE IS AN END DATE THEN CHECK IF THE END DATE IS LESS THAN THE CURRENT DATE AND SEND THE MAIL IF ITS COMMING IN NEXT 3 DAYS
 ########################### ELSE JUST SEND THE MAIL TO THE RECURRING EXPENSES COMMING IN THE NEXT THREE DAYS
for exp in recs:
    if (exp['end_date'] and exp['end_date']<curr_date.date() )or not exp['user_name']:        
        msg=(
            f"Hey {exp['user_name']},\n\n"
            f"This is just a remainder for your upcoming recurring expense:\n"
            f"Expense: {exp['description']}\n"
            f"Amount: ${exp['amount']}\n"
            f"Regards,\n Expense Management Team,\n Famora"
        )
        sendEmail(exp['email'],subject,msg)