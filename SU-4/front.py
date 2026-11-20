# [SU-36] Interfaz de consola para inicio de sesión del personal de salud
from backUsuarios import iniciar_sesion


def pedir_credenciales():
    """Solicita correo institucional y contraseña por consola."""
    while True:
        email = input("Correo institucional: ").strip()
        if "@" not in email or len(email) < 5:
            print("Error: Ingresá un correo institucional válido.")
            continue

        password = input("Contraseña: ").strip()
        if not password:
            print("Error: La contraseña no puede estar vacía.")
            continue

        return email, password


def pantalla_login():
    """Flujo de inicio de sesión por consola."""
    print("\n=== SANATORIO UNDAV - INICIO DE SESIÓN ===\n")
    while True:
        email, password = pedir_credenciales()
        usuario = iniciar_sesion(email, password)

        if usuario is None:
            print("\nError: Credenciales inválidas. Intentá nuevamente.\n")
            continue

        print(f"\nBienvenido/a, {usuario['nombre']} (Perfil: {usuario['rol']})")
        print("Módulos habilitados:")
        for modulo in usuario["pantallas_permitidas"]:
            print(f"  - {modulo}")
        print("------------------------------------------\n")
        return usuario


if __name__ == "__main__":
    pantalla_login()