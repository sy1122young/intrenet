from flask import Flask, render_template, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import json
import os
from os import listdir
import csv
from fileinput import filename
import uuid

# def find_csv_filenames(suffix=".csv"):
#     filenames = listdir("./static")
#     return [ filename for filename in filenames if filename.endswith( suffix )]

# def ReadNewFile():
#     filenames = find_csv_filenames(suffix=".csv")
#     file = filenames[0]
#     with open("./static/"+file) as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             print(row["surname"])
#             AddToFile(surname=row["surname"],name=row["name"],number=row["number"],email=row["email"])
#     os.remove("./static/"+file)

# def AddToFile(surname, name, number,email):
#     with open("files/contacts.csv", "a") as file:
#         writer = csv.DictWriter(file, fieldnames=["surname","name","number","email"])
#         writer.writerow({"surname": surname,"name": name,"number": number,"email": email})



