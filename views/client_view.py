from flask import render_template

def list(clients):
    return render_template('clients/index.html',clients=clients)

def create():
    return render_template('clients/create.html')

def edit(client):
    return render_template('clients/edit.html',client=client)