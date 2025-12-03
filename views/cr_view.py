# views/cr_view.py
from flask import render_template

def list(crs):
    return render_template("cr/index.html", crs=crs)

def create(clients, whrs):
    return render_template("cr/create.html", clients=clients, whrs=whrs)

def view(cr):
    return render_template("cr/view.html", cr=cr)
