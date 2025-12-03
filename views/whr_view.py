# views/whr_view.py
from flask import render_template

def list(whrs):
    return render_template('whr/index.html', whrs=whrs)

def create(clients):
    return render_template('whr/create.html', clients=clients)

def edit(whr, clients):
    return render_template('whr/edit.html', whr=whr, clients=clients)

def view(whr):
    return render_template('whr/view.html', whr=whr)
