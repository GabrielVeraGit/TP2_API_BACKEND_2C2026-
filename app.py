from config import Config, db
from flask import Flask, jsonify, request


app  = Flask(__name__)
app.config.from_object(Config)

# Inicializamos la base de datos con Flask
db.init_app(app)

# Definimos la estructura de la tabla
class Producto(db.Model):
  __tablename__ = "productos"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)

  # Función para convertir el objeto a diccionario (JSON)
  def to_dict(self):
    return {"id": self.id, "name": self.name}


# Crea las tablas automáticamente en la BD si no existen al iniciar
with app.app_context():
  db.create_all()


# --- RUTAS DE LA API ---


# GET /productos -> Obtener todos los productos
@app.route("/productos", methods=["GET"])
def obtener_productos():
  try:
    productos = Producto.query.all()
    return jsonify([p.to_dict() for p in productos]), 200
  except Exception as e:
    return jsonify({"error": str(e)}), 500


# POST /productos -> Crear un nuevo producto
@app.route("/productos", methods=["POST"])
def crear_producto():
  try:
    datos = request.get_json()
    nuevo_producto = Producto(name=datos.get("name"))

    db.session.add(nuevo_producto)
    db.session.commit()

    return jsonify(nuevo_producto.to_dict()), 201
  except Exception as e:
    return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=6969, debug=False)

