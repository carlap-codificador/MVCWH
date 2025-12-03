from flask import render_template

def list(commodities):
    return render_template('commodities/index.html',commodities=commodities)

def create(whr_id=None):
    return render_template('commodities/create.html', whr_id=whr_id)

def edit(commodity):
    return render_template('commodities/edit.html',commodity=commodity)