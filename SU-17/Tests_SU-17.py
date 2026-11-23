import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "SU-16")))

from backPacientes import ingresarPaciente, derivarPacienteATriage
from Validaciones_SU17 import numero_dentro_rangoCerrado
from backTriage import (
    validar_signos_vitales,
    registrar_signos_vitales,
    obtener_signos_paciente,
)


def _paciente_ejemplo():
    return {
        "dni_afiliado": "35111222",
        "nombre_apellido": "Ana Belén Sosa",
        "edad": 29,
        "obra_social": "Swiss Medical",
        "plan": "SMG20",
        "motivo_consulta": "Dolor torácico leve",
    }


def _signos_validos():
    return {
        "ta_sistolica": 120,
        "ta_diastolica": 80,
        "frecuencia_cardiaca": 78,
        "frecuencia_respiratoria": 16,
        "temperatura": 36.7,
        "saturacion_o2": 98,
    }


def test_rango_cerrado_validaciones():
    assert numero_dentro_rangoCerrado(36.5, 30.0, 45.0) is True
    assert numero_dentro_rangoCerrado(30.0, 30.0, 45.0) is True
    assert numero_dentro_rangoCerrado(46.0, 30.0, 45.0) is False


def test_validar_signos_vitales_correctos():
    assert validar_signos_vitales(_signos_validos()) is True


def test_negar_signos_fuera_de_rango_o_incompletos():
    signos_malos = _signos_validos()
    signos_malos["temperatura"] = 47.5
    assert validar_signos_vitales(signos_malos) is False

    incompletos = _signos_validos()
    del incompletos["saturacion_o2"]
    assert validar_signos_vitales(incompletos) is False


def test_negar_ta_diastolica_mayor_o_igual_sistolica():
    signos_ta_invalida = _signos_validos()
    signos_ta_invalida["ta_sistolica"] = 90
    signos_ta_invalida["ta_diastolica"] = 100
    assert validar_signos_vitales(signos_ta_invalida) is False


def test_registrar_y_vincular_signos_a_admision():
    admitidos = []
    en_triage = []
    registros = []
    paciente = _paciente_ejemplo()

    ingresarPaciente(paciente, admitidos)
    derivarPacienteATriage(paciente, admitidos, en_triage)

    guardado = registrar_signos_vitales(
        paciente["dni_afiliado"],
        _signos_validos(),
        admitidos,
        en_triage,
        registros,
    )

    assert guardado is not None
    assert paciente["triage_completado"] is True
    assert obtener_signos_paciente(paciente["dni_afiliado"], admitidos)["saturacion_o2"] == 98
    assert len(en_triage) == 0


def test_negar_registro_triage_paciente_no_admitido():
    admitidos = []
    en_triage = []
    registros = []

    resultado = registrar_signos_vitales("99999999", _signos_validos(), admitidos, en_triage, registros)
    assert resultado is None
    assert len(registros) == 0