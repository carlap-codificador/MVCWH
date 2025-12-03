
from flask import Blueprint, request, redirect, url_for, abort
from datetime import datetime

from decorators import login_required
from models.cr_model import CargoRelease, CargoReleaseItem
from models.client_model import Client
from models.whr_model  import WHR
from models.commodity_model import Commodity
from views import cr_view

cr_bp = Blueprint("cr", __name__, url_prefix="/cr")


# -------------------------------------------------
# LISTA DE CR
# -------------------------------------------------
@cr_bp.route("/")
@login_required
def index():
    crs = CargoRelease.get_all()
    return cr_view.list(crs)


# -------------------------------------------------
# CREAR CR
# -------------------------------------------------
@cr_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        cr_number    = request.form.get("cr_number")
        date_str     = request.form.get("date")
        consignee_id = request.form.get("consignee_id")

        whr_ids = request.form.getlist("whr_ids")

        if not cr_number or not date_str or not consignee_id or not whr_ids:
            return redirect(url_for("cr.create"))

        consignee_id = int(consignee_id)
        cr_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Crear CR
        cr = CargoRelease(
            cr_number=cr_number,
            date=cr_date,
            consignee_id=consignee_id
        )
        cr.save()   # ya existe en BD

        # Crear items
        for whr_id_str in whr_ids:
            whr = WHR.get_by_id(int(whr_id_str))
            if not whr:
                continue

            pieces = whr.total_pieces
            volume = whr.total_volume
            weight = whr.total_weight

            days_in_wh = (cr_date - whr.date).days

            item = CargoReleaseItem(
                cr_id=cr.id,
                whr_id=whr.id,
                pieces=pieces,
                volume=volume,
                weight=weight,
                days_in_wh=days_in_wh
            )
            item.save()   # 👈 commit se hace dentro del modelo

            # Actualizar estados de commodities
            for c in whr.commodities:
                c.set_released()
                c.save()   # 👈 commit individual, como tu modelo maneja

        return redirect(url_for("cr.view", id=cr.id))

    # GET
    clients = Client.get_all()
    whrs    = WHR.get_all()
    return cr_view.create(clients, whrs)


# -------------------------------------------------
# VER DETALLE DE CR
# -------------------------------------------------
@cr_bp.route("/view/<int:id>")
@login_required
def view(id):
    cr = CargoRelease.get_by_id(id)
    if not cr:
        abort(404)
    return cr_view.view(cr)


# -------------------------------------------------
# ELIMINAR CR
# -------------------------------------------------
@cr_bp.route("/delete/<int:id>")
@login_required
def delete(id):
    cr = CargoRelease.get_by_id(id)
    if not cr:
        abort(404)
    cr.delete()
    return redirect(url_for("cr.index"))
