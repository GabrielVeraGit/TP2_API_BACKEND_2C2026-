from config import db


class Cancha(db.Model):
    __tablename__ = "canchas"

    id = db.Column(db.Integer, primary_key=True)
    id_deporte = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    techada = db.Column(db.Boolean, nullable=False)
    activa = db.Column(db.Boolean, nullable=False)
    precio_hora = db.Column(db.Numeric(10, 2), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "id_deporte": self.id_deporte,
            "nombre": self.nombre,
            "techada": self.techada,
            "activa": self.activa,
            "precio_hora": self.precio_hora
        }