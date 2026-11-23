# [SU-52] Backend de clasificación automática de Triage según parámetros fisiológicos
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "SU-17")))

from backTriage import validar_signos_vitales

NOMBRES_NIVELES_TRIAGE = {
    1: "Nivel 1 - Rojo (Resucitación)",
    2: "Nivel 2 - Naranja (Emergencia)",
    3: "Nivel 3 - Amarillo (Urgencia)",
    4: "Nivel 4 - Verde (Menos urgente)",
    5: "Nivel 5 - Azul (No urgente)",
}


def clasificar_nivel_triage(signos):
    """
    [SU-52] Asigna automáticamente una categoría de triage (1 a 5)
    basándose en los parámetros fisiológicos registrados en SU-17.
    Devuelve un entero del 1 (más urgente) al 5 (menos urgente), o None si los signos son inválidos.
    """
    if not validar_signos_vitales(signos):
        return None

    tas = signos["ta_sistolica"]
    tad = signos["ta_diastolica"]
    fc = signos["frecuencia_cardiaca"]
    fr = signos["frecuencia_respiratoria"]
    temp = signos["temperatura"]
    sat = signos["saturacion_o2"]

    # Nivel 1: Riesgo vital inmediato
    if (
        sat < 85
        or tas < 70
        or tas > 220
        or fc < 40
        or fc > 150
        or fr < 8
        or fr > 35
        or temp < 34.0
        or temp >= 41.0
    ):
        return 1

    # Nivel 2: Emergencia
    if (
        sat < 90
        or tas < 90
        or tas >= 180
        or tad >= 110
        or fc < 50
        or fc > 130
        or fr < 10
        or fr > 28
        or temp < 35.0
        or temp >= 39.5
    ):
        return 2

    # Nivel 3: Urgencia
    if (
        sat < 94
        or tas >= 150
        or tad >= 95
        or fc > 110
        or fr > 22
        or temp >= 38.0
    ):
        return 3

    # Nivel 4: Menos urgente
    if (
        sat < 96
        or tas >= 140
        or tad >= 90
        or fc > 100
        or fr > 20
        or temp >= 37.5
    ):
        return 4

    # Nivel 5: No urgente (parámetros fisiológicos normales)
    return 5