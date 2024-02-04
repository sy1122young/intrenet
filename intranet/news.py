from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import json
import os
UPLOAD_FOLDER = '/static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# reads news file
def readFile():
    file = open("files/news.json")
    try:
        data = json.load(file)
        new = data["data"]
        #print(new[0]["title"])
    except:
        print("file not found")
    return new

#def addNews():
    #with open("files/news.json","w") as out:
        #json.dump(data, out)





