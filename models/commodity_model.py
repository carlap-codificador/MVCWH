# models/commodity_model.py
from database import db

class Commodity(db.Model):
    __tablename__ = "commodities"
    
    # Estados
    STATUS_ON_HAND   = 0
    STATUS_RELEASED  = 1

    id           = db.Column(db.Integer, primary_key=True)
    description  = db.Column(db.String(120), nullable=False)
    package_type = db.Column(db.String(120), nullable=False)
    pieces       = db.Column(db.Integer, nullable=False)
    length       = db.Column(db.Float(11, 2), nullable=False)
    width        = db.Column(db.Float(11, 2), nullable=False)
    height       = db.Column(db.Float(11, 2), nullable=False)
    unit         = db.Column(db.String(20), nullable=False)         # unidad de las dimensiones

    # Peso: se guarda SIEMPRE en kg, pero recordamos la unidad que eligió el usuario
    weight       = db.Column(db.Float(11, 2), nullable=False)       # siempre en kg
    weight_unit  = db.Column(db.String(5), nullable=False, default="kg")  # 'kg' o 'lb'

    # Volumen: se guarda SIEMPRE en m³, pero recordamos la unidad de visualización
    volume       = db.Column(db.Float(11, 4), nullable=False)       # siempre en m³
    volume_unit  = db.Column(db.String(5), nullable=False, default="m3")  # 'm3','cm3','ft3','in3'

    status       = db.Column(db.Integer, nullable=False, default=STATUS_ON_HAND)

    # Relación con WHR
    whr_id = db.Column(db.Integer, db.ForeignKey('whrs.id'), nullable=True)
    whr    = db.relationship('WHR', back_populates='commodities')

    # ------------------------------------------------------------------
    # __init__
    # ------------------------------------------------------------------
    def __init__(
        self,
        description,
        package_type,
        pieces,
        length,
        width,
        height,
        unit,
        weight,
        weight_unit="kg",
        volume=0.0,
        volume_unit="m3",
        status=STATUS_ON_HAND,
        whr_id=None
    ):
        self.description  = description
        self.package_type = package_type
        self.pieces       = pieces
        self.length       = length
        self.width        = width
        self.height       = height
        self.unit         = unit

        # usamos los helpers para normalizar
        self.set_weight(weight, weight_unit)
        self.set_volume_from_dims(length, width, height, unit, volume_unit)

        self.status = status
        self.whr_id = whr_id

    # ------------------------------------------------------------------
    # Helpers de estado
    # ------------------------------------------------------------------
    def set_on_hand(self):
        self.status = self.STATUS_ON_HAND

    def set_released(self):
        self.status = self.STATUS_RELEASED

    def is_on_hand(self):
        return self.status == self.STATUS_ON_HAND

    def is_released(self):
        return self.status == self.STATUS_RELEASED

    # ------------------------------------------------------------------
    # Helpers de peso y volumen
    # ------------------------------------------------------------------
    def set_weight(self, value, unit):
        """Guarda el peso siempre en kg y recuerda la unidad original."""
        if unit == "lb":
            self.weight = value * 0.453592  # lb → kg
        else:
            self.weight = value
        self.weight_unit = unit

    def set_volume_from_dims(self, length, width, height, dim_unit, vol_unit):
        """
        Calcula volumen a partir de las dimensiones y unidad de longitud.
        Guarda SIEMPRE en m³ y guarda la unidad elegida para mostrar.
        """
        # Pasar dimensiones a metros
        if dim_unit == "cm":
            L = length / 100.0
            W = width  / 100.0
            H = height / 100.0
        elif dim_unit == "inch":
            L = length * 0.0254
            W = width  * 0.0254
            H = height * 0.0254
        elif dim_unit == "foot":
            L = length * 0.3048
            W = width  * 0.3048
            H = height * 0.3048
        else:  # 'm'
            L, W, H = length, width, height

        volume_m3 = L * W * H
        self.volume = volume_m3
        self.volume_unit = vol_unit

    def get_volume_display(self):
        """Devuelve el volumen convertido a la unidad de visualización."""
        v = float(self.volume)
        if self.volume_unit == "cm3":
            return v * 1_000_000.0
        if self.volume_unit == "ft3":
            return v * 35.3147
        if self.volume_unit == "in3":
            return v * 61_023.7441
        return v  # m3

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Commodity.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Commodity.query.get(id)
    
    def update(
        self,
        description=None,
        package_type=None,
        pieces=None,
        length=None,
        width=None,
        height=None,
        unit=None,
        weight=None,
        weight_unit=None,
        volume_unit=None,
        status=None,
        whr_id=None
    ):
        if description is not None:
            self.description = description
        if package_type is not None:
            self.package_type = package_type
        if pieces is not None:
            self.pieces = pieces
        if length is not None:
            self.length = length
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if unit is not None:
            self.unit = unit

        # Peso
        if (weight is not None) and (weight_unit is not None):
            self.set_weight(weight, weight_unit)

        # Volumen
        if (length is not None and width is not None and
            height is not None and unit is not None and
            volume_unit is not None):
            self.set_volume_from_dims(length, width, height, unit, volume_unit)

        if status is not None:
            self.status = status

        if whr_id is not None:
            self.whr_id = whr_id
        
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
