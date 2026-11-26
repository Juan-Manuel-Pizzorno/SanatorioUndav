import importlib.util
import os
import sys

RUTA_RAIZ = os.path.dirname(os.path.abspath(__file__))

# Agregamos las carpetas al path para que funcionen los imports internos de cada módulo
for carpeta in ("FuncionesDeValidacion", "SU-4", "SU-5", "SU-16", "SU-17", "SU-18"):
    ruta = os.path.join(RUTA_RAIZ, carpeta)
    if os.path.isdir(ruta) and ruta not in sys.path:
        sys.path.append(ruta)


def _cargar_front(carpeta, alias_modulo):
    """Carga un front.py específico sin colisiones de nombre entre carpetas."""
    ruta_archivo = os.path.join(RUTA_RAIZ, carpeta, "front.py")
    spec = importlib.util.spec_from_file_location(alias_modulo, ruta_archivo)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


front_su4 = _cargar_front("SU-4", "front_su4")
front_su5 = _cargar_front("SU-5", "front_su5")
front_su16 = _cargar_front("SU-16", "front_su16")
front_su17 = _cargar_front("SU-17", "front_su17")
front_su18 = _cargar_front("SU-18", "front_su18")


def menu_principal():
    while True:
        print("\n====================================================")
        print("      SANATORIO UNDAV - SISTEMA DE GUARDIA")
        print("====================================================")
        print("1. Inicio de sesión del personal de salud (SU-4)")
        print("2. Acceso médico y selector de contexto (SU-5)")
        print("3. Admisión de paciente en guardia (SU-16)")
        print("4. Clasificación de Triage (SU-17)")
        print("5. Cola de espera y priorización (SU-18)")
        print("0. Salir")

        opcion = input("\nSeleccioná una opción: ").strip()

        if opcion == "1":
            front_su4.pantalla_login()
            input("Presioná Enter para cerrar sesión y volver al menú...")
        elif opcion == "2":
            front_su5.flujo_medico_consola()
            input("Presioná Enter para volver al menú...")
        elif opcion == "3":
            front_su16.formulario_admision()
            input("Presioná Enter para volver al menú...")
        elif opcion == "4":
            front_su17.flujo_triage()
            input("Presioná Enter para volver al menú...")
        elif opcion == "5":
            front_su18.flujo_cola_guardia()
            input("Presioná Enter para volver al menú...")
        elif opcion == "0":
            print("\nCerrando sistema del Sanatorio UNDAV...")
            break
        else:
            print("\nError: Opción inválida. Intentá nuevamente.")


if __name__ == "__main__":
    menu_principal()
