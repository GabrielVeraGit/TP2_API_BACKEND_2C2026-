from datetime import datetime
from source.constants import PRECIO_MIN

def validar_cancha(data):

    if data is None:
        return None, "El cuerpo de la solicitud no puede estar vacío"

    nombre = data.get("nombre")

    if nombre is None or not isinstance(nombre, str) or not nombre.strip():
        return None, "El campo 'nombre' es obligatorio y no puede estar vacío"

    id_deporte = data.get("id_deporte")

    if id_deporte is None:
        return None, "El campo 'id_deporte' es obligatorio"

    if type(id_deporte) is not int:
        return None, "El campo 'id_deporte' debe ser un entero"

    precio_hora = data.get("precio_hora")

    if precio_hora is None:
        return None, "El campo 'precio_hora' es obligatorio"

    if not validar_precio(precio_hora):
        return None, "El campo 'precio_hora' debe ser un entero mayor o igual a 1"

    techada = data.get("techada")

    if techada is not None and type(techada) is not bool:
        return None, "El campo 'techada' debe ser booleano"

    activa = data.get("activa")

    if activa is not None and type(activa) is not bool:
        return None, "El campo 'activa' debe ser booleano"

    return True, None

def validar_update_cancha(data):

    if not data:
        return None, "El cuerpo de la solicitud no puede estar vacío"

    if "nombre" in data:
        nombre = data["nombre"]

        if not isinstance(nombre, str) or not nombre.strip():
            return None, "El campo 'nombre' no puede estar vacío"

    if "precio_hora" in data:
        precio_hora = data["precio_hora"]

        if not validar_precio(precio_hora):
            return None, "El campo 'precio_hora' debe ser un entero mayor o igual a 1"

    if "techada" in data:
        if type(data["techada"]) is not bool:
            return None, "El campo 'techada' debe ser booleano"

    if "activa" in data:
        if type(data["activa"]) is not bool:
            return None, "El campo 'activa' debe ser booleano"

    return True, None

def validar_precio(precio):
    return type(precio) is int and precio >= PRECIO_MIN

def validar_canchas_disponibles(data):

    fecha = data.get("fecha")
    hora_inicio = data.get("hora_inicio")
    hora_fin = data.get("hora_fin")

    if fecha is None or not fecha.strip():
        return None, "La fecha no puede estar vacia"

    if hora_inicio is None or not hora_inicio.strip():
        return None, "La hora de inicio no puede estar vacia"

    if hora_fin is None or not hora_fin.strip():
        return None, "La hora de fin no puede estar vacia"

    try:
        inicio = datetime.strptime(
            f"{fecha} {hora_inicio}",
            "%Y-%m-%d %H:%M:%S"
        )

        fin = datetime.strptime(
            f"{fecha} {hora_fin}",
            "%Y-%m-%d %H:%M:%S"
        )

    except ValueError:
        return None, "Formato de fecha u hora invalido"

    if inicio >= fin:
        return None, "La hora de inicio debe ser menor que la hora de fin"

    duracion = (fin - inicio).total_seconds() / 3600

    if duracion < 1 or duracion > 3:
        return None, "La reserva debe durar entre 1 y 3 horas"

    if inicio.minute != 0 or inicio.second != 0:
        return None, "La hora de inicio debe ser una hora exacta"

    if fin.minute != 0 or fin.second != 0:
        return None, "La hora de fin debe ser una hora exacta"

    if inicio.hour < 8 or fin.hour > 23:
        return None, "El horario debe estar entre las 08:00 y las 23:00"

    return True, None
    

