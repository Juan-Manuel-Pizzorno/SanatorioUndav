# [SU-41] Selector de contexto operativo por consola para médicos (Guardia / Consultorios Externos)
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "SU-4")))

from backUsuarios import iniciar_sesion
from backContexto import requiere_seleccion_contexto, seleccionar_contexto_medico


def mostrar_panel_medico(usuario):
    """Muestra en consola el ámbito activo y las herramientas habilitadas para el turno."""
    print(f"\n--- PANEL MÉDICO ({usuario['nombre']} | Matrícula: {usuario['matricula']}) ---")
    print(f"Ámbito activo: {usuario['contexto_activo']}")
    print("Herramientas habilitadas para este turno:")
    for modulo in usuario["pantallas_permitidas"]:
        print(f"  - {modulo}")
    print("----------------------------------------------------------")


def elegir_contexto_consola(usuario):
    """Muestra las opciones de ámbito operativo si el médico tiene doble contexto."""
    if not requiere_seleccion_contexto(usuario):
        return usuario

    print(f"\n=== SELECTOR DE CONTEXTO MÉDICO ({usuario['nombre']} - {usuario['matricula']}) ===")
    print("1. Guardia")
    print("2. Consultorios Externos")

    while True:
        opcion = input("Seleccioná tu ámbito operativo (1 o 2): ").strip()
        if opcion == "1":
            return seleccionar_contexto_medico(usuario, "Guardia")
        if opcion == "2":
            return seleccionar_contexto_medico(usuario, "Consultorios Externos")
        print("Error: Ingresá 1 para Guardia o 2 para Consultorios Externos.")


def menu_sesion_medico(usuario):
    """Permite operar y cambiar de ámbito en caliente si la matrícula tiene doble contexto."""
    doble_ambito = requiere_seleccion_contexto(usuario)

    while True:
        mostrar_panel_medico(usuario)
        if doble_ambito:
            print("Opciones: [1] Cambiar de ámbito operativo  |  [2] Cerrar sesión")
            accion = input("Elegí una opción: ").strip()
            if accion == "1":
                nuevo_ctx = "Consultorios Externos" if usuario["contexto_activo"] == "Guardia" else "Guardia"
                usuario = seleccionar_contexto_medico(usuario, nuevo_ctx)
                print(f"\n>>> Ámbito cambiado dinámicamente a: {usuario['contexto_activo']} <<<")
            elif accion == "2":
                print("\nSesión cerrada correctamente.\n")
                break
            else:
                print("Error: Opción inválida.")
        else:
            input("\n(Ámbito único por matrícula) Presioná Enter para cerrar sesión...")
            print("\nSesión cerrada correctamente.\n")
            break


def flujo_medico_consola():
    print("\n=== SANATORIO UNDAV - ACCESO MÉDICO ===\n")
    email = input("Correo institucional del médico: ").strip()
    password = input("Contraseña: ").strip()

    usuario = iniciar_sesion(email, password)
    if usuario is None or usuario["rol"] != "Médico":
        print("Error: Credenciales inválidas o el usuario no corresponde a un médico.")
        return None

    usuario = elegir_contexto_consola(usuario)
    menu_sesion_medico(usuario)
    return usuario


if __name__ == "__main__":
    flujo_medico_consola()