# Vista de consola de la cola de espera general de guardia
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "SU-16")))

from FuncionesSU_45 import esPacientePediatrico
from backColaGuardia import NOMBRES_NIVELES_TRIAGE, clasificar_nivel_triage


def mostrar_cola_espera(cola_pacientes):
    """Muestra en consola la cola general de guardia con su orden, nivel y tiempo de espera."""
    print("\n=== SANATORIO UNDAV - COLA DE ESPERA GENERAL DE GUARDIA ===\n")

    if not cola_pacientes:
        print("No hay pacientes en espera en este momento.\n")
        return

    for orden, paciente in enumerate(cola_pacientes, start=1):
        nivel = paciente.get("nivel_triage")
        if nivel is None and "signos_vitales" in paciente:
            nivel = clasificar_nivel_triage(paciente["signos_vitales"])

        descripcion_nivel = NOMBRES_NIVELES_TRIAGE.get(nivel, "Sin clasificar")
        nombre = paciente.get("nombre_apellido", "Sin nombre")
        dni = paciente.get("dni_afiliado", "S/D")
        espera = paciente.get("tiempo_espera", 0)
        motivo = paciente.get("motivo_consulta", "-")

        if "edad" in paciente:
            atencion = "Pediátrica" if esPacientePediatrico(paciente) else "Adultos"
        else:
            atencion = "No especificada"

        print(f"#{orden} | {descripcion_nivel} | Espera: {espera} min")
        print(f"    Paciente: {nombre} (DNI: {dni}) - Atención: {atencion}")
        print(f"    Motivo: {motivo}")
        print("-" * 60)

    print()
