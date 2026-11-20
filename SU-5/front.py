# [SU-41] Selector de contexto operativo por consola para médicos (Guardia / Consultorios Externos)
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "SU-4")))

from backUsuarios import iniciar_sesion
from backContexto import requiere_seleccion_contexto, seleccionar_contexto_medico


def elegir_contexto_consola(usuario):
    """Muestra las opciones de ámbito operativo si el médico tiene doble contexto."""
    if not requiere_seleccion_contexto(usuario):
        ambito = usuario.get("contexto_activo", "Sin ámbito asignado")
        print(f"\nIngreso directo en ámbito: {ambito} (Matrícula: {usuario.get('matricula')})")
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


def flujo_medico_consola():
    print("\n=== SANATORIO UNDAV - ACCESO MÉDICO ===\n")
    email = input("Correo institucional del médico: ").strip()
    password = input("Contraseña: ").strip()

    usuario = iniciar_sesion(email, password)
    if usuario is None or usuario["rol"] != "Médico":
        print("Error: Credenciales inválidas o el usuario no corresponde a un médico.")
        return None

    usuario = elegir_contexto_consola(usuario)
    print(f"\nÁmbito activo: {usuario['contexto_activo']}")
    print("Herramientas habilitadas para este turno:")
    for modulo in usuario["pantallas_permitidas"]:
        print(f"  - {modulo}")
    print("------------------------------------------\n")
    return usuario


if __name__ == "__main__":
    flujo_medico_consola()