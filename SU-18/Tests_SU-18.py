import os
import sys

RUTA_RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if RUTA_RAIZ not in sys.path:
    sys.path.append(RUTA_RAIZ)

from backColaGuardia import clasificar_nivel_triage
from backOrdenamientoCola import ingresar_a_cola_guardia, ordenar_cola_guardia
from frontColaGuardia import mostrar_cola_espera


def _signos_normales():
    return {
        "ta_sistolica": 120,
        "ta_diastolica": 80,
        "frecuencia_cardiaca": 75,
        "frecuencia_respiratoria": 16,
        "temperatura": 36.6,
        "saturacion_o2": 98,
    }


def _paciente_ejemplo(dni, nombre, edad=35, motivo="Consulta en guardia", signos=None):
    paciente = {
        "dni_afiliado": dni,
        "nombre_apellido": nombre,
        "edad": edad,
        "obra_social": "OSDE",
        "plan": "210",
        "motivo_consulta": motivo,
    }
    if signos is not None:
        paciente["signos_vitales"] = signos
    return paciente


def test_clasificacion_nivel_1_riesgo_vital():
    signos = _signos_normales()
    signos["saturacion_o2"] = 82
    nivel = clasificar_nivel_triage(signos)
    assert nivel == 1
    print(f"\n[OK] Clasificación Nivel 1 verificada (SatO2: {signos['saturacion_o2']}% -> Nivel {nivel})")


def test_clasificacion_nivel_2_emergencia():
    signos = _signos_normales()
    signos["saturacion_o2"] = 88
    nivel = clasificar_nivel_triage(signos)
    assert nivel == 2
    print(f"\n[OK] Clasificación Nivel 2 verificada (SatO2: {signos['saturacion_o2']}% -> Nivel {nivel})")


def test_clasificacion_nivel_3_urgencia():
    signos = _signos_normales()
    signos["temperatura"] = 38.5
    nivel = clasificar_nivel_triage(signos)
    assert nivel == 3
    print(f"\n[OK] Clasificación Nivel 3 verificada (Temp: {signos['temperatura']}°C -> Nivel {nivel})")


def test_clasificacion_nivel_4_menos_urgente():
    signos = _signos_normales()
    signos["temperatura"] = 37.6
    nivel = clasificar_nivel_triage(signos)
    assert nivel == 4
    print(f"\n[OK] Clasificación Nivel 4 verificada (Temp: {signos['temperatura']}°C -> Nivel {nivel})")


def test_clasificacion_nivel_5_no_urgente():
    nivel = clasificar_nivel_triage(_signos_normales())
    assert nivel == 5
    print(f"\n[OK] Clasificación Nivel 5 verificada (Signos normales -> Nivel {nivel})")


def test_clasificacion_signos_invalidos():
    signos_malos = _signos_normales()
    signos_malos["ta_sistolica"] = 80
    signos_malos["ta_diastolica"] = 100
    assert clasificar_nivel_triage(signos_malos) is None
    assert clasificar_nivel_triage(None) is None
    print("\n[OK] Rechazo de signos vitales inválidos verificado.")


def test_ordenamiento_por_gravedad():
    cola_desordenada = [
        {
            "dni_afiliado": "38412905",
            "nombre_apellido": "Lucía Fernández",
            "edad": 28,
            "motivo_consulta": "Fiebre moderada",
            "nivel_triage": 4,
            "tiempo_espera": 50,
        },
        {
            "dni_afiliado": "21745845",
            "nombre_apellido": "Jorge Ramírez",
            "edad": 54,
            "motivo_consulta": "Insuficiencia respiratoria aguda",
            "nivel_triage": 1,
            "tiempo_espera": 5,
        },
        {
            "dni_afiliado": "42903118",
            "nombre_apellido": "Mateo Giménez",
            "edad": 12,
            "motivo_consulta": "Control por golpe leve",
            "nivel_triage": 5,
            "tiempo_espera": 90,
        },
        {
            "dni_afiliado": "27654321",
            "nombre_apellido": "Valeria Castro",
            "edad": 41,
            "motivo_consulta": "Dolor precordial intenso",
            "nivel_triage": 2,
            "tiempo_espera": 10,
        },
        {
            "dni_afiliado": "33198472",
            "nombre_apellido": "Hernán Silva",
            "edad": 33,
            "motivo_consulta": "Cólico renal",
            "nivel_triage": 3,
            "tiempo_espera": 30,
        },
    ]

    print("\n>>> TEST ORDENAMIENTO POR GRAVEDAD - ANTES:")
    mostrar_cola_espera(cola_desordenada)

    ordenada = ordenar_cola_guardia(cola_desordenada)

    print(">>> TEST ORDENAMIENTO POR GRAVEDAD - DESPUÉS:")
    mostrar_cola_espera(ordenada)

    niveles = [p["nivel_triage"] for p in ordenada]
    assert niveles == [1, 2, 3, 4, 5]
    print("[OK] La cola se ordenó correctamente del Nivel 1 al Nivel 5.")


def test_desempate_por_mayor_tiempo_espera():
    cola_empatada = [
        {
            "dni_afiliado": "29481036",
            "nombre_apellido": "Diego Morales",
            "edad": 39,
            "motivo_consulta": "Fiebre alta",
            "nivel_triage": 3,
            "tiempo_espera": 15,
        },
        {
            "dni_afiliado": "24819503",
            "nombre_apellido": "Marta Benítez",
            "edad": 61,
            "motivo_consulta": "Crisis hipertensiva moderada",
            "nivel_triage": 3,
            "tiempo_espera": 45,
        },
        {
            "dni_afiliado": "35720419",
            "nombre_apellido": "Camila Torres",
            "edad": 25,
            "motivo_consulta": "Dolor abdominal agudo",
            "nivel_triage": 3,
            "tiempo_espera": 30,
        },
    ]

    print("\n>>> TEST DESEMPATE POR TIEMPO DE ESPERA - ANTES:")
    mostrar_cola_espera(cola_empatada)

    ordenada = ordenar_cola_guardia(cola_empatada)

    print(">>> TEST DESEMPATE POR TIEMPO DE ESPERA - DESPUÉS:")
    mostrar_cola_espera(ordenada)

    dnis_ordenados = [p["dni_afiliado"] for p in ordenada]
    assert dnis_ordenados == ["24819503", "35720419", "29481036"]
    print("[OK] A igual nivel de triage, priorizó al paciente con mayor tiempo de espera (45 > 30 > 15 min).")


def test_ingresar_a_cola_clasifica_y_ordena_automaticamente():
    cola = []

    signos_nivel_3 = _signos_normales()
    signos_nivel_3["temperatura"] = 38.4
    p1 = _paciente_ejemplo("31604892", "Carlos Ruiz", 44, "Fiebre y decaimiento", signos_nivel_3)

    signos_nivel_3_mas_espera = _signos_normales()
    signos_nivel_3_mas_espera["frecuencia_cardiaca"] = 115
    p2 = _paciente_ejemplo("26937154", "Laura Díaz", 31, "Taquicardia", signos_nivel_3_mas_espera)

    ingresar_a_cola_guardia(p1, tiempo_espera=10, colaGuardia=cola)
    ingresar_a_cola_guardia(p2, tiempo_espera=25, colaGuardia=cola)

    print("\n>>> TEST INGRESO AUTOMÁTICO - ANTES (con 2 pacientes Nivel 3):")
    mostrar_cola_espera(cola)

    # Ingresa un paciente crítico Nivel 1 con solo 2 minutos de espera
    signos_nivel_1 = _signos_normales()
    signos_nivel_1["saturacion_o2"] = 80
    p3 = _paciente_ejemplo("40518263", "Pedro Gómez", 19, "Disnea severa", signos_nivel_1)
    ingresar_a_cola_guardia(p3, tiempo_espera=2, colaGuardia=cola)

    print(">>> TEST INGRESO AUTOMÁTICO - DESPUÉS (ingresa paciente Nivel 1 y pasa primero):")
    mostrar_cola_espera(cola)

    assert [p["dni_afiliado"] for p in cola] == ["40518263", "26937154", "31604892"]
    print("[OK] El ingreso automático clasificó por signos vitales y reordenó la cola correctamente.")


def test_ingresar_paciente_sin_signos_validos_devuelve_none():
    cola = []
    paciente_sin_triage = _paciente_ejemplo("37294610", "Sofía López", 27, "Dolor de garganta")
    assert ingresar_a_cola_guardia(paciente_sin_triage, tiempo_espera=10, colaGuardia=cola) is None
    assert len(cola) == 0
    print("\n[OK] Bloqueo de ingreso sin signos vitales válidos verificado.")


if __name__ == "__main__":
    test_clasificacion_nivel_1_riesgo_vital()
    test_clasificacion_nivel_2_emergencia()
    test_clasificacion_nivel_3_urgencia()
    test_clasificacion_nivel_4_menos_urgente()
    test_clasificacion_nivel_5_no_urgente()
    test_clasificacion_signos_invalidos()
    test_ordenamiento_por_gravedad()
    test_desempate_por_mayor_tiempo_espera()
    test_ingresar_a_cola_clasifica_y_ordena_automaticamente()
    test_ingresar_paciente_sin_signos_validos_devuelve_none()
    print("\n============================================================")
    print("TODOS LOS TESTS DE SU-18 PASARON CORRECTAMENTE.")
    print("============================================================")
