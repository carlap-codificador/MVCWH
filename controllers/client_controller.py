from flask import request, redirect, url_for, Blueprint

from models.client_model import Client
from views import client_view
from decorators import login_required

client_bp=Blueprint('client',__name__,url_prefix="/clients")

@client_bp.route("/")
@login_required
def index():
    #recupera los registros de la tabla clients en forma de objeto
    clients=Client.get_all()
    return client_view.list(clients)

@client_bp.route("/create", methods=['GET','POST'])
def create():
    if request.method =='POST':
        name=request.form['name']
        email=request.form['email']
        address=request.form['address']
        phone=request.form['phone']

        client=Client(name,email,address,phone)
        client.save()
        return redirect(url_for('client.index'))
    
    return client_view.create()

@client_bp.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id):
    client=Client.get_by_id(id)
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        address=request.form['address']
        phone=request.form['phone']
        #actualizar
        client.update(name=name,email=email,address=address, phone=phone)
        return redirect(url_for('client.index'))
    
    return client_view.edit(client)
@client_bp.route("/delete/<int:id>")
def delete(id):
    client=Client.get_by_id(id)
    client.delete()
    return redirect(url_for('client.index'))

