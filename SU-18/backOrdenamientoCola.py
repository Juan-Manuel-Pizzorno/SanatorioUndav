# Ordenamiento e ingreso de pacientes en la cola de espera de guardia
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "SU-16")))

from FuncionesSU_45 import buscarPaciente
from backColaGuardia import NOMBRES_NIVELES_TRIAGE, clasificar_nivel_triage

# Cola general de espera en memoria
cola_espera_guardia = []


def ordenar_cola_guardia(cola_pacientes):
    """
    Ordena la cola de espera priorizando siempre el nivel de gravedad
    (Nivel 1 como más urgente) y desempatando por mayor tiempo acumulado de espera.
    """
    return sorted(
        cola_pacientes,
        key=lambda paciente: (
            paciente["nivel_triage"],
            -paciente.get("tiempo_espera", 0),
        ),
    )


def ingresar_a_cola_guardia(
    paciente,
    tiempo_espera=0,
    colaGuardia=cola_espera_guardia,
):
    """
    Clasifica al paciente según sus signos vitales, lo incorpora a la cola
    general de espera de guardia y mantiene la cola ordenada.
    Devuelve el paciente actualizado o None si los datos son inválidos.
    """
    if not isinstance(paciente, dict) or "dni_afiliado" not in paciente:
        return None

    if isinstance(tiempo_espera, bool) or not isinstance(tiempo_espera, (int, float)) or tiempo_espera < 0:
        return None

    nivel = paciente.get("nivel_triage")
    if "signos_vitales" in paciente:
        nivel = clasificar_nivel_triage(paciente["signos_vitales"])

    if nivel not in NOMBRES_NIVELES_TRIAGE:
        return None

    paciente["nivel_triage"] = nivel
    paciente["tiempo_espera"] = tiempo_espera

    existente = buscarPaciente(colaGuardia, paciente["dni_afiliado"])
    if existente is None:
        colaGuardia.append(paciente)
    else:
        existente.update(paciente)

    colaGuardia[:] = ordenar_cola_guardia(colaGuardia)
    return paciente
