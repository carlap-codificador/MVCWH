from flask import request, redirect, url_for, Blueprint, abort
from datetime import datetime

from models.whr_model import WHR
from models.client_model import Client
from decorators import login_required
from views import whr_view

whr_bp = Blueprint('whr', __name__, url_prefix="/whr")


# ---------------------------------------------------------
# LISTA DE WHR
# ---------------------------------------------------------
@whr_bp.route("/")
@login_required
def index():
    whrs = WHR.get_all()
    return whr_view.list(whrs)


# ---------------------------------------------------------
# CREAR WHR (cabecera)
# ---------------------------------------------------------
@whr_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        whr_number = request.form.get("whr_number")
        date_str   = request.form.get("date")
        mbl        = request.form.get("mbl")
        hbl        = request.form.get("hbl")

        shipper_id   = int(request.form.get("shipper_id"))
        consignee_id = int(request.form.get("consignee_id"))

        mode        = request.form.get("mode_of_transportation")
        origin      = request.form.get("origin")
        destination = request.form.get("destination")

        date = datetime.strptime(date_str, "%Y-%m-%d").date()

        whr = WHR(
            whr_number=whr_number,
            date=date,
            mbl=mbl,
            hbl=hbl,
            shipper_id=shipper_id,
            consignee_id=consignee_id,
            mode_of_transportation=mode,
            origin=origin,
            destination=destination
        )
        whr.save()

        # Después de crear, vamos a editar y agregar commodities
        return redirect(url_for("whr.edit", id=whr.id))

    clients = Client.get_all()
    return whr_view.create(clients)


# ---------------------------------------------------------
# EDITAR / RESUMEN WHR (agregar commodities y ver totales)
# ---------------------------------------------------------
@whr_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    whr = WHR.get_by_id(id)
    if not whr:
        abort(404)

    if request.method == "POST":
        # Si quieres permitir cambiar cabecera, descomenta/ajusta:
        # whr_number = request.form.get("whr_number")
        # ...
        # whr.update(...)

        return redirect(url_for("whr.index"))

    clients = Client.get_all()
    return whr_view.edit(whr, clients)


# ---------------------------------------------------------
# VER DETALLE SOLO LECTURA
# ---------------------------------------------------------
@whr_bp.route("/view/<int:id>")
@login_required
def view(id):
    whr = WHR.get_by_id(id)
    if not whr:
        abort(404)
    return whr_view.view(whr)


# ---------------------------------------------------------
# ELIMINAR WHR
# ---------------------------------------------------------
@whr_bp.route("/delete/<int:id>")
@login_required
def delete(id):
    whr = WHR.get_by_id(id)
    if not whr:
        abort(404)
    whr.delete()
    return redirect(url_for("whr.index"))
