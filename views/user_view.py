from flask import render_template

def list(users):
    return render_template('users/index.html',users=users)

def create():
    return render_template('users/create.html')

def edit(user):
    return render_template('users/edit.html',user=user)