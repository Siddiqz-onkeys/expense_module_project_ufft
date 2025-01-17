import mysql.connector
from datetime import datetime 
from flask import Flask,request,render_template,jsonify,redirect,url_for
import os,time
from werkzeug.utils import secure_filename

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

cursor.execute("SELECT * FROM expenses")
exps=cursor.fetchall()
for exp in exps:
    print(exp)