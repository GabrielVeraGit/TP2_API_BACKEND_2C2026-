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
    

