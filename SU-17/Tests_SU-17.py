import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "SU-16")))

from backPacientes import ingresarPaciente, derivarPacienteATriage
from Validaciones import numero_dentro_rangoCerrado
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
    assert numero_dentro_rangoCerrado(45.0, 30.0, 45.0) is True
    assert numero_dentro_rangoCerrado(46.0, 30.0, 45.0) is False


def test_validar_signos_vitales_correctos():
    assert validar_signos_vitales(_signos_validos()) is True


def test_validar_valores_limite_minimos_y_maximos():
    limites_minimos = {
        "ta_sistolica": 40,
        "ta_diastolica": 20,
        "frecuencia_cardiaca": 20,
        "frecuencia_respiratoria": 5,
        "temperatura": 30.0,
        "saturacion_o2": 40,
    }
    limites_maximos = {
        "ta_sistolica": 300,
        "ta_diastolica": 200,
        "frecuencia_cardiaca": 250,
        "frecuencia_respiratoria": 80,
        "temperatura": 45.0,
        "saturacion_o2": 100,
    }
    assert validar_signos_vitales(limites_minimos) is True
    assert validar_signos_vitales(limites_maximos) is True


def test_negar_cada_parametro_fuera_de_rango():
    casos_invalidos = [
        ("ta_sistolica", 35),
        ("ta_sistolica", 310),
        ("ta_diastolica", 15),
        ("ta_diastolica", 210),
        ("frecuencia_cardiaca", 10),
        ("frecuencia_cardiaca", 260),
        ("frecuencia_respiratoria", 2),
        ("frecuencia_respiratoria", 90),
        ("temperatura", 29.9),
        ("temperatura", 45.1),
        ("saturacion_o2", 39),
        ("saturacion_o2", 101),
    ]
    for campo, valor_malo in casos_invalidos:
        signos = _signos_validos()
        signos[campo] = valor_malo
        assert validar_signos_vitales(signos) is False


def test_negar_signos_incompletos_o_no_diccionario():
    assert validar_signos_vitales(None) is False
    assert validar_signos_vitales([]) is False

    incompletos = _signos_validos()
    del incompletos["saturacion_o2"]
    assert validar_signos_vitales(incompletos) is False


def test_negar_tipos_de_dato_invalidos():
    signos_texto = _signos_validos()
    signos_texto["frecuencia_cardiaca"] = "78"
    assert validar_signos_vitales(signos_texto) is False

    signos_bool = _signos_validos()
    signos_bool["temperatura"] = True
    assert validar_signos_vitales(signos_bool) is False


def test_negar_ta_diastolica_mayor_o_igual_sistolica():
    signos_mayor = _signos_validos()
    signos_mayor["ta_sistolica"] = 90
    signos_mayor["ta_diastolica"] = 100
    assert validar_signos_vitales(signos_mayor) is False

    signos_igual = _signos_validos()
    signos_igual["ta_sistolica"] = 100
    signos_igual["ta_diastolica"] = 100
    assert validar_signos_vitales(signos_igual) is False


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


def test_actualizar_signos_mismo_paciente_sin_duplicar():
    admitidos = []
    en_triage = []
    registros = []
    paciente = _paciente_ejemplo()

    ingresarPaciente(paciente, admitidos)
    registrar_signos_vitales(paciente["dni_afiliado"], _signos_validos(), admitidos, en_triage, registros)

    nuevos_signos = _signos_validos()
    nuevos_signos["temperatura"] = 38.4
    registrar_signos_vitales(paciente["dni_afiliado"], nuevos_signos, admitidos, en_triage, registros)

    assert len(registros) == 1
    assert obtener_signos_paciente(paciente["dni_afiliado"], admitidos)["temperatura"] == 38.4


def test_negar_registro_triage_paciente_no_admitido():
    admitidos = []
    en_triage = []
    registros = []

    resultado = registrar_signos_vitales("99999999", _signos_validos(), admitidos, en_triage, registros)
    assert resultado is None
    assert len(registros) == 0


def test_obtener_signos_paciente_sin_triage_o_inexistente():
    admitidos = []
    paciente = _paciente_ejemplo()
    ingresarPaciente(paciente, admitidos)

    assert obtener_signos_paciente(paciente["dni_afiliado"], admitidos) is None
    assert obtener_signos_paciente("00000000", admitidos) is None