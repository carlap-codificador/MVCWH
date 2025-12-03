# models/cr_model.py
from database import db


class CargoRelease(db.Model):
    __tablename__ = "cargo_releases"

    id        = db.Column(db.Integer, primary_key=True)
    cr_number = db.Column(db.String(50), nullable=False, unique=True)
    date      = db.Column(db.Date, nullable=False)

    # Consignee viene de clients
    consignee_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    consignee    = db.relationship('Client')

    # Items (por WHR)
    items = db.relationship(
        "CargoReleaseItem",
        back_populates="cargo_release",
        cascade="all, delete-orphan"
    )

    # --------- Totales derivados de los items ---------
    @property
    def total_pieces(self):
        return sum(i.pieces for i in self.items)

    @property
    def total_volume(self):
        return sum(float(i.volume) for i in self.items)

    @property
    def total_weight(self):
        return sum(float(i.weight) for i in self.items)

    # --------- Métodos CRUD ---------
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return CargoRelease.query.all()

    @staticmethod
    def get_by_id(id):
        return CargoRelease.query.get(id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class CargoReleaseItem(db.Model):
    __tablename__ = "cargo_release_items"

    id       = db.Column(db.Integer, primary_key=True)

    cr_id    = db.Column(db.Integer, db.ForeignKey('cargo_releases.id'), nullable=False)
    whr_id   = db.Column(db.Integer, db.ForeignKey('whrs.id'), nullable=False)

    pieces   = db.Column(db.Integer, nullable=False)
    volume   = db.Column(db.Float(11, 4), nullable=False)   # m³
    weight   = db.Column(db.Float(11, 2), nullable=False)   # kg
    days_in_wh = db.Column(db.Integer, nullable=False)

    # Relaciones
    cargo_release = db.relationship("CargoRelease", back_populates="items")
    whr           = db.relationship("WHR")

    # CRUD básico (por si lo necesitas)
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return CargoReleaseItem.query.get(id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
