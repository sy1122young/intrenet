from flask import Flask, render_template, flash, request, redirect, url_for, session,abort, send_file
from werkzeug.utils import secure_filename
import news
from pathlib import Path
import contact
import json
import datetime as dt
# from flask_session import Session
import os
from os import listdir
import csv
from fileinput import filename
import files
import helpers
from flask_session import Session
from cs50 import SQL
import mysql.connector
# this is where images get uploaded to 
UPLOAD_FOLDER = './static'
#allowed extensions for uploading files
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','csv'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(12)
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# Configure CS50 Library to use SQLite database
#for sqllite data base
db = SQL("sqlite:///logins.db")
# if you want to use sql database
# db = mysql.connector.connect(
#     host = "localhost",
#     user = "somthing",
#     password = "you password"
# )

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect to home
    return redirect("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return redirect('/')
        # Ensure password was submitted
        elif not request.form.get("password"):
            return redirect('/')
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        password = request.form.get("password")
        # Ensure username exists and password is correct
        if len(rows) != 1 or not rows[0]["hash"] == password:
            return apology("invalid username and/or password", 403)
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # Redirect user to home page
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/update-link", methods=['POST'])
def updatelink():
    webname = request.form.get("webname")
    webURL = request.form.get("webURL")
    with open("files/links.csv", "a") as file:
        writer = csv.DictWriter(file, fieldnames=["name","linkurl"])
        writer.writerow({"name": webname,"linkurl": webURL})
    return redirect("/")

@app.route("/deletenews/<string:index>")
def deletenews(index):
    #get file 
    with open('files/news.json', 'r') as file:
        data = json.load(file)
    # Find and remove the entry with the specified title
    new_data = [entry for entry in data['data'] if entry['title'] != index]
    # Update the JSON data with the modified list
    data['data'] = new_data
    # Write the modified JSON data back to the file
    with open('files/news.json', 'w') as file:
        json.dump(data, file, indent=2)
    return redirect("/")
@app.route("/editnews/<string:index>")
def editnews(index):
    #get file 
    with open('files/news.json', 'r') as file:
        data = json.load(file)

# delete link
@app.route("/delete/<int:index>")
def delete(index):
    filepath = "files/links.csv"
    with open(filepath, 'r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)
    # Delete the row at the specified index
    del data[index+1]
    # Write the updated data back to the CSV file
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    return redirect("/")
# home page
@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'POST':
      # upload file flask
        f = request.files.get('file')
        # Extracting uploaded file name
        data_filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],data_filename))
        session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'],data_filename)
        new = news.readFile()
        return render_template('index.html',news=new)
    new = news.readFile()
    links = helpers.get_links()
    return render_template("index.html",news=new,links=links,title="Whats new")
    #return render_template("layout.html")

@app.route("/staff-contacts", methods=['GET','POST'])
def Contacts():
    links = helpers.get_links()
    rows = db.execute("SELECT * FROM contacts ORDER BY LOWER(name) ASC")
    return render_template("contacts.html",contacts=rows,links=links,title="Contacts")
# delete a single contact
@app.route("/deletecontact/<int:index>")
def deletecontact(index):
    db.execute("DELETE FROM contacts WHERE id = ?",index)
    return redirect("/staff-contacts")
#delete all contacts
@app.route("/deleteallcontacts")
def deleteallcontacts():
    db.execute("DELETE FROM contacts")
    return redirect("/staff-contacts")

#table sorting first name
@app.route("/sortcontactFN")
def sortcontactFN():
    sort = request.args.get("q")
    if sort == "ASC":
        query = "SELECT * FROM contacts ORDER BY LOWER(name) ASC"
    else:
        query = "SELECT * FROM contacts ORDER BY LOWER(name)  DESC"
    contacts = db.execute(query)
    return render_template("search.html",contacts=contacts,title="contacts")
#table sorting last name
@app.route("/sortcontactLN")
def sortcontactLN():
    sort = request.args.get("q")
    if sort == "ASC":
        query = "SELECT * FROM contacts ORDER BY LOWER(surname) ASC"
    else:
        query = "SELECT * FROM contacts ORDER BY LOWER(surname) DESC"
    contacts = db.execute(query)
    return render_template("search.html",contacts=contacts,title="contacts")


@app.route("/search")
def search():
    q = request.args.get("q")
    if q:
        q = request.args.get("q")+"%"
        contacts = db.execute("SELECT * FROM contacts WHERE name LIKE ? OR surname LIKE ? OR number LIKE ? OR department LIKE ? OR email LIKE ?",q,q,q,q,q)
    else:
        contacts = contacts = db.execute("SELECT * FROM contacts ORDER BY name ASC")
    return render_template("search.html",contacts=contacts,title="contacts")


@app.route("/add-contacts",methods=['POST'])
def addContacts():
        print("test")
        # get fields
        if request.method == 'POST':
            fname = request.form.get("fname")
            lname = request.form.get("surname")
            department = request.form.get("department")
            num = request.form.get("num")
            email = request.form.get("email")
            #add to data base
            db.execute("INSERT INTO contacts (name,surname,number,email,department) VALUES (?,?,?,?,?)",fname,lname,num,email,department)
            return redirect("/")
        return render_template("/staff-contacts")

@app.route("/upload-contacts",methods=['POST'])
def csvContacts():
    # upload file flask
    f = request.files.get('file')
    # Extracting uploaded file name
    data_filename = secure_filename(f.filename)
    f.save(os.path.join(app.config['UPLOAD_FOLDER'],data_filename))
    session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'],data_filename)
    filenames = find_csv_filenames(suffix=".csv")
    file = filenames[0]
    with open("./static/"+file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name,surname,number,email,department= row["name"],row["surname"],row["number"],row["email"],row["department"]
            db.execute("INSERT INTO contacts (name,surname,number,email,department) VALUES (?,?,?,?,?)",name,surname,number,email,department)
    os.remove("./static/"+file)
    return redirect("/staff-contacts")

def find_csv_filenames(suffix=".csv"):
    filenames = listdir("./static")
    return [ filename for filename in filenames if filename.endswith( suffix )]





#######################################folder code####################
#< change this to edit location of folder
# for windows
#baseFolderPath = r'C:\local-files'
#for mac
baseFolderPath = os.path.expanduser("~/Desktop/local-files")
#######################################
@app.route("/reports/",defaults={'reqPath':""})
@app.route('/reports/<path:reqPath>')
def reports(reqPath):
    #absPath = safe_join(baseFolderPath, reqPath)
    absPath = baseFolderPath+"/"+ reqPath

    if not os.path.exists(absPath):
        return abort(404)

    if os.path.isfile(absPath):
        return send_file(absPath)

    def fObjFromScan(x):
        fIcon = 'bi bi-folder-fill' if os.path.isdir(x.path) else files.getIconClassForFilename(x.name)
        fileStat = x.stat()
        fBytes = files.getReadableByteSize(fileStat.st_size)
        fTime = files.getTimeStampString(fileStat.st_mtime)
        return {
            'name' : x.name,
            'size': fBytes,
            'mTime': fTime,
            'fIcon' : fIcon,
            'fLink' : os.path.relpath(x.path, baseFolderPath).replace("\\","/")
            }
    fNames = [fObjFromScan(x) for x in os.scandir(absPath)]
    parentPath = os.path.relpath(Path(absPath).parents[0], baseFolderPath).replace("\\","/")
    links = helpers.get_links()
    return render_template('files.html',files=fNames, parentPath=parentPath,links=links,title="Documents")

#runs main
if __name__ == "__main__":
    app.run(debug=True)
