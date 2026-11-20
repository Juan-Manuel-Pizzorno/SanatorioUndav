# [SU-37 / SU-38] Padrón de usuarios del personal de salud y validación de acceso

USUARIOS_SISTEMA = [
    {
        "id": 1,
        "nombre": "Laura Gómez",
        "email": "laura.gomez@undav.edu.ar",
        "password": "1234",
        "rol": "Admisión",
        "pantallas_permitidas": ["Registro de Guardia", "Búsqueda por DNI/Afiliado"]
    },
    {
        "id": 2,
        "nombre": "Carlos Méndez",
        "email": "carlos.mendez@undav.edu.ar",
        "password": "1234",
        "rol": "Triage",
        "pantallas_permitidas": ["Registro de Parámetros Fisiológicos", "Clasificación Triage"]
    },
    {
        "id": 3,
        "nombre": "Dra. Sofía Martínez",
        "email": "sofia.martinez@undav.edu.ar",
        "password": "1234",
        "rol": "Médico",
        "matricula": "MP-45821",
        "doble_contexto": True,
        "contextos_habilitados": ["Guardia", "Consultorios Externos"],
        "permisos_por_contexto": {
            "Guardia": ["Atención de Guardia", "Historia Clínica", "Recetas Electrónicas", "Solicitud de Derivaciones"],
            "Consultorios Externos": ["Agenda de Consultorios", "Historia Clínica", "Recetas Electrónicas", "Solicitud de Estudios"]
        },
        "pantallas_permitidas": ["Atención de Guardia", "Historia Clínica", "Recetas Electrónicas"]
    },
    {
        "id": 4,
        "nombre": "Dr. Roberto Silva",
        "email": "roberto.silva@undav.edu.ar",
        "password": "1234",
        "rol": "Jefe de Guardia",
        "pantallas_permitidas": ["Tablero de Control en Tiempo Real", "Autorización de Derivaciones"]
    },
    {
        "id": 5,
        "nombre": "Mariana Torres",
        "email": "mariana.torres@undav.edu.ar",
        "password": "1234",
        "rol": "Administrativo",
        "pantallas_permitidas": ["Validación de Órdenes Médicas", "Gestión de Agenda"]
    },
    {
        "id": 6,
        "nombre": "Juan Pizzorno",
        "email": "juan.pizzorno@undav.edu.ar",
        "password": "1234",
        "rol": "TI",
        "pantallas_permitidas": ["Alta de Profesionales", "Parametrización Obras Sociales", "Reglas CIE-10"]
    },
    {
        "id": 7,
        "nombre": "Dr. Lucas Pereyra",
        "email": "lucas.pereyra@undav.edu.ar",
        "password": "1234",
        "rol": "Médico",
        "matricula": "MP-51204",
        "doble_contexto": False,
        "contexto_activo": "Consultorios Externos",
        "pantallas_permitidas": ["Agenda de Consultorios", "Historia Clínica", "Recetas Electrónicas", "Solicitud de Estudios"]
    }
]


def buscar_usuario_por_email(lista_usuarios, email):
    """Busca un usuario por correo institucional ignorando mayúsculas y espacios."""
    email_limpio = email.strip().lower()
    for usuario in lista_usuarios:
        if usuario["email"].lower() == email_limpio:
            return usuario
    return None


def iniciar_sesion(email, password, lista_usuarios=USUARIOS_SISTEMA):
    """Valida credenciales y devuelve los datos de sesión sin la contraseña, o None si falla."""
    if not email or not password or not email.strip():
        return None

    usuario = buscar_usuario_por_email(lista_usuarios, email)
    if usuario is None or usuario["password"] != password:
        return None

    sesion = {clave: valor for clave, valor in usuario.items() if clave != "password"}
    return sesion


def tiene_acceso_modulo(usuario, modulo):
    """Verifica si el usuario autenticado tiene permiso para acceder a un módulo."""
    if usuario is None:
        return False
    return modulo in usuario.get("pantallas_permitidas", [])