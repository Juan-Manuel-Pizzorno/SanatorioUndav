# [SU-40 / SU-42] Vinculación de médico único por matrícula y selección de contexto operativo

CONTEXTOS_VALIDOS = ["Guardia", "Consultorios Externos"]


def requiere_seleccion_contexto(usuario):
    """Indica si el médico atiende en ambos ámbitos y debe elegir turno al ingresar."""
    if usuario is None or usuario.get("rol") != "Médico":
        return False
    return bool(usuario.get("doble_contexto", False))


def seleccionar_contexto_medico(usuario, contexto):
    """Valida la matrícula del médico y adapta las pantallas permitidas según el contexto elegido."""
    if usuario is None or usuario.get("rol") != "Médico" or not usuario.get("matricula"):
        return None

    habilitados = usuario.get("contextos_habilitados", [])
    if contexto not in habilitados:
        return None

    sesion_actualizada = dict(usuario)
    sesion_actualizada["contexto_activo"] = contexto

    permisos_ctx = usuario.get("permisos_por_contexto", {})
    if contexto in permisos_ctx:
        sesion_actualizada["pantallas_permitidas"] = list(permisos_ctx[contexto])

    return sesion_actualizada