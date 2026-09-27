from datetime import datetime
def validar_cancha(data):
    nombre = data.get("nombre")
    if nombre is None  or not nombre.strip():
        return None, "Nombre no puede estar vacio"

    deporte = data.get("id_deporte")
    if deporte is None:
            return None, "el ID de deporte no puede estar vacio"
    
    precio_hora = data.get("precio_hora")
    if precio_hora is None:
                return None, "el precio por hora no puede estar vacio"

    return True, None

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
    

