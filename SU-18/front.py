# Vista de consola de la cola de espera general de guardia
import os
import sys

RUTA_RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for carpeta in ("SU-16", "SU-17"):
    ruta = os.path.join(RUTA_RAIZ, carpeta)
    if ruta not in sys.path:
        sys.path.append(ruta)

from FuncionesSU_45 import buscarPaciente, esPacientePediatrico
from backColaGuardia import NOMBRES_NIVELES_TRIAGE, clasificar_nivel_triage
from backOrdenamientoCola import cola_espera_guardia, ingresar_a_cola_guardia
from backPacientes import pacientes_admitidos


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


def flujo_cola_guardia():
    """Muestra la cola desordenada, ejecuta la clasificación/ordenamiento de SU-18 y muestra el resultado."""
    if not cola_espera_guardia:
        cola_previa = [
            {
                "dni_afiliado": "42903118",
                "nombre_apellido": "Mateo Giménez",
                "edad": 12,
                "motivo_consulta": "Control por golpe leve",
                "tiempo_espera": 60,
                "signos_vitales": {
                    "ta_sistolica": 110,
                    "ta_diastolica": 70,
                    "frecuencia_cardiaca": 80,
                    "frecuencia_respiratoria": 16,
                    "temperatura": 36.6,
                    "saturacion_o2": 99,
                },
            },
            {
                "dni_afiliado": "29481036",
                "nombre_apellido": "Diego Morales",
                "edad": 39,
                "motivo_consulta": "Fiebre alta",
                "tiempo_espera": 15,
                "signos_vitales": {
                    "ta_sistolica": 120,
                    "ta_diastolica": 80,
                    "frecuencia_cardiaca": 85,
                    "frecuencia_respiratoria": 18,
                    "temperatura": 38.5,
                    "saturacion_o2": 97,
                },
            },
            {
                "dni_afiliado": "24819503",
                "nombre_apellido": "Marta Benítez",
                "edad": 61,
                "motivo_consulta": "Taquicardia moderada",
                "tiempo_espera": 45,
                "signos_vitales": {
                    "ta_sistolica": 130,
                    "ta_diastolica": 85,
                    "frecuencia_cardiaca": 115,
                    "frecuencia_respiratoria": 19,
                    "temperatura": 36.8,
                    "saturacion_o2": 96,
                },
            },
        ]
    else:
        cola_previa = list(cola_espera_guardia)

    # Si admitiste y evaluaste en triage un paciente en las opciones 3 y 4, se suma al final antes de ordenar
    for p in pacientes_admitidos:
        if p.get("triage_completado") and buscarPaciente(cola_previa, p["dni_afiliado"]) is None:
            p.setdefault("tiempo_espera", 5)
            cola_previa.append(p)

    print("\n>>> 1. COLA DE ESPERA ACTUAL (ANTES DE ORDENAR) <<<")
    mostrar_cola_espera(cola_previa)

    input("Presioná Enter para clasificar y ordenar la cola automáticamente (SU-18)...")

    for p in cola_previa:
        ingresar_a_cola_guardia(p, tiempo_espera=p.get("tiempo_espera", 0), colaGuardia=cola_espera_guardia)

    print("\n>>> 2. COLA DE ESPERA ACTUALIZADA (CLASIFICADA Y ORDENADA POR SU-18) <<<")
    mostrar_cola_espera(cola_espera_guardia)


if __name__ == "__main__":
    flujo_cola_guardia()
