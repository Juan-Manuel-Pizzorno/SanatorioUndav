# [SU-50] Backend de registro y vinculación de parámetros fisiológicos (Triage) con la admisión
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "SU-16")))

from backPacientes import buscarPaciente, pacientes_admitidos, pacientes_en_triage
from FuncionesDeValidacion.Validaciones import numero_dentro_rangoCerrado

RANGOS_SIGNOS_VITALES = {
    "ta_sistolica": (40, 300),
    "ta_diastolica": (20, 200),
    "frecuencia_cardiaca": (20, 250),
    "frecuencia_respiratoria": (5, 80),
    "temperatura": (30.0, 45.0),
    "saturacion_o2": (40, 100),
}

registros_triage = []


def validar_signos_vitales(signos):
    """Verifica que estén todos los parámetros obligatorios y dentro de sus rangos válidos."""
    if not isinstance(signos, dict):
        return False

    for campo, (minimo, maximo) in RANGOS_SIGNOS_VITALES.items():
        if campo not in signos:
            return False
        valor = signos[campo]
        if not isinstance(valor, (int, float)) or isinstance(valor, bool):
            return False
        if not numero_dentro_rangoCerrado(valor, minimo, maximo):
            return False

    if signos["ta_diastolica"] >= signos["ta_sistolica"]:
        return False

    return True


def registrar_signos_vitales(
    dni_afiliado,
    signos,
    pacientesAdmitidos=pacientes_admitidos,
    pacientesEnTriage=pacientes_en_triage,
    listaRegistrosTriage=registros_triage,
):
    """
    [SU-50] Valida los parámetros fisiológicos y los vincula directamente
    al registro de admisión del paciente que está siendo evaluado.
    """
    paciente = buscarPaciente(pacientesAdmitidos, dni_afiliado)
    if paciente is None:
        return None

    if not validar_signos_vitales(signos):
        return None

    signos_vinculados = {
        "dni_afiliado": dni_afiliado,
        **{campo: signos[campo] for campo in RANGOS_SIGNOS_VITALES},
    }

    # Vincula los signos directamente al diccionario de admisión del paciente
    paciente["signos_vitales"] = signos_vinculados
    paciente["triage_completado"] = True

    # Evita duplicados si se actualiza la medición del mismo paciente
    existente = buscarPaciente(listaRegistrosTriage, dni_afiliado)
    if existente is None:
        listaRegistrosTriage.append(signos_vinculados)
    else:
        existente.update(signos_vinculados)

    # Si estaba en la cola de espera de Triage, lo marca como evaluado / lo retira de espera
    en_espera = buscarPaciente(pacientesEnTriage, dni_afiliado)
    if en_espera is not None:
        pacientesEnTriage.remove(en_espera)

    return signos_vinculados


def obtener_signos_paciente(dni_afiliado, pacientesAdmitidos=pacientes_admitidos):
    """Devuelve los signos vitales vinculados al registro de admisión del paciente."""
    paciente = buscarPaciente(pacientesAdmitidos, dni_afiliado)
    if paciente is None:
        return None
    return paciente.get("signos_vitales")
