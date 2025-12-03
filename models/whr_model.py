from database import db

class WHR(db.Model):
    __tablename__ = "whrs"

    id          = db.Column(db.Integer, primary_key=True)
    whr_number  = db.Column(db.String(50), nullable=False, unique=True)
    date        = db.Column(db.Date, nullable=False)
    mbl         = db.Column(db.String(50))
    hbl         = db.Column(db.String(50))

    # 🔹 relación con clientes
    shipper_id   = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    consignee_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

    shipper   = db.relationship('Client', foreign_keys=[shipper_id])
    consignee = db.relationship('Client', foreign_keys=[consignee_id])

    mode_of_transportation = db.Column(db.String(50), nullable=False)
    origin      = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)

    # relación con commodities
    commodities = db.relationship(
        "Commodity",
        back_populates="whr",
        cascade="all, delete-orphan"
    )

    def __init__(self, whr_number, date, mbl, hbl,
                 shipper_id, consignee_id,
                 mode_of_transportation, origin, destination):
        self.whr_number  = whr_number
        self.date        = date
        self.mbl         = mbl
        self.hbl         = hbl
        self.shipper_id  = shipper_id
        self.consignee_id = consignee_id
        self.mode_of_transportation = mode_of_transportation
        self.origin      = origin
        self.destination = destination

    # --- agregados desde commodities ---
    @property
    def total_pieces(self):
        """Piezas aún en almacén (solo commodities ON_HAND)."""
        from models.commodity_model import Commodity
        return sum(
            c.pieces
            for c in self.commodities
            if c.status == Commodity.STATUS_ON_HAND
        )

    @property
    def total_weight(self):
        """Peso aún en almacén (kg, solo ON_HAND)."""
        from models.commodity_model import Commodity
        return sum(
            float(c.weight)
            for c in self.commodities
            if c.status == Commodity.STATUS_ON_HAND
        )

    @property
    def total_volume(self):
        """Volumen aún en almacén (m³, solo ON_HAND)."""
        from models.commodity_model import Commodity
        return sum(
            float(c.volume)
            for c in self.commodities
            if c.status == Commodity.STATUS_ON_HAND
        )

    @property
    def status(self):
        """
        Estado derivado de los commodities:
        - On Hand   → todos ON_HAND
        - Released  → todos RELEASED
        - Partial   → mezcla de estados
        - No Cargo  → sin commodities
        """
        from models.commodity_model import Commodity

        if not self.commodities:
            return "No Cargo"

        all_on_hand = all(c.status == Commodity.STATUS_ON_HAND for c in self.commodities)
        all_released = all(c.status == Commodity.STATUS_RELEASED for c in self.commodities)

        if all_on_hand:
            return "On Hand"
        if all_released:
            return "Released"
        return "Partial"

    # --- CRUD ---
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return WHR.query.all()

    @staticmethod
    def get_by_id(id):
        return WHR.query.get(id)

    def update(self, **kwargs):
        for field, value in kwargs.items():
            if hasattr(self, field) and value is not None:
                setattr(self, field, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
