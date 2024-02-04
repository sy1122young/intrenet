
from flask import redirect, render_template, session
from functools import wraps
import csv


# def apology(message, code=400):
#     return 


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
# get links
def get_links():
    #read csv links file
    with open("./files/links.csv") as csvfile:
            reader = csv.DictReader(csvfile)
            links = list(reader)
            #print(links[0]["priority"])
            sorted_links = sorted(links, key=lambda x: x['priority'])
    return sorted_links

