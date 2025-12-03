from flask import request, redirect, url_for, Blueprint, abort

from models.commodity_model import Commodity
from views import commodity_view
from decorators import login_required

commodity_bp = Blueprint('commodity', __name__, url_prefix="/commodities")


@commodity_bp.route("/")
@login_required
def index():
    commodities = Commodity.get_all()
    return commodity_view.list(commodities)


@commodity_bp.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    whr_id = request.args.get("whr_id") if request.method == "GET" else request.form.get("whr_id")

    if request.method == 'POST':
        description   = request.form['description']
        package_type  = request.form['package_type']
        pieces        = int(request.form['pieces'])
        length        = float(request.form['length'])
        width         = float(request.form['width'])
        height        = float(request.form['height'])
        unit          = request.form['unit']
        weight        = float(request.form['weight'])
        volume        = float(request.form['volume'])
        status        = int(request.form['status'])

        commodity = Commodity(
            description=description,
            package_type=package_type,
            pieces=pieces,
            length=length,
            width=width,
            height=height,
            unit=unit,
            weight=weight,
            volume=volume,
            status=status,
            whr_id=int(whr_id) if whr_id else None
        )
        commodity.save()

        if whr_id:
            return redirect(url_for('whr.edit', id=whr_id))

        return redirect(url_for('commodity.index'))

    return commodity_view.create(whr_id=whr_id)


@commodity_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    commodity = Commodity.get_by_id(id)
    if not commodity:
        abort(404)

    if request.method == 'POST':
        description   = request.form['description']
        package_type  = request.form['package_type']
        pieces        = int(request.form['pieces'])
        length        = float(request.form['length'])
        width         = float(request.form['width'])
        height        = float(request.form['height'])
        unit          = request.form['unit']

        weight_val    = float(request.form['weight'])
        weight_unit   = request.form['weight_unit']

        volume_unit   = request.form['volume_unit']
        status        = int(request.form['status'])

        commodity.update(
            description=description,
            package_type=package_type,
            pieces=pieces,
            length=length,
            width=width,
            height=height,
            unit=unit,
            weight=weight_val,
            weight_unit=weight_unit,
            volume_unit=volume_unit,
            status=status
        )

        return redirect(url_for('commodity.index'))

    return commodity_view.edit(commodity)


@commodity_bp.route("/delete/<int:id>")
def delete(id):
    commodity = Commodity.get_by_id(id)
    if not commodity:
        abort(404)

    commodity.delete()
    return redirect(url_for('commodity.index'))
