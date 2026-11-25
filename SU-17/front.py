import sys
import os

RAIZ_PROYECTO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if RAIZ_PROYECTO not in sys.path:
    sys.path.insert(0, RAIZ_PROYECTO)
from FuncionesDeValidacion.Validaciones import pedir_entero, pedir_decimal
from backTriage import registrar_signos_vitales


def formulario_signos_vitales(paciente):
    nombre_completo = paciente.get(
        "nombre_apellido",
        f"{paciente.get('nombre', '')} {paciente.get('apellido', '')}".strip(),
    )
    print(f"\n--- Triage: {nombre_completo} (DNI: {paciente['dni_afiliado']}) ---")

    signos = {
        "dni_afiliado": paciente["dni_afiliado"],
        "ta_sistolica": pedir_entero("TA Sistólica (máxima): ", 40, 300, "Valor inválido (40-300): "),
        "ta_diastolica": pedir_entero("TA Diastólica (mínima): ", 20, 200, "Valor inválido (20-200): "),
        "frecuencia_cardiaca": pedir_entero("Frecuencia Cardíaca: ", 20, 250, "Valor inválido (20-250): "),
        "frecuencia_respiratoria": pedir_entero("Frecuencia Respiratoria: ", 5, 80, "Valor inválido (5-80): "),
        "temperatura": pedir_decimal("Temperatura (°C): ", 30.0, 45.0, "Valor inválido (30.0-45.0): "),
        "saturacion_o2": pedir_entero("Saturación O2 (%): ", 40, 100, "Valor inválido (40-100): "),
    }

    print(
        "\n--- Resumen de signos vitales registrados ---\n"
        + "TA:", str(signos["ta_sistolica"]) + "/" + str(signos["ta_diastolica"]),
        "| FC:", signos["frecuencia_cardiaca"],
        "| FR:", signos["frecuencia_respiratoria"],
        "| Temp:", str(signos["temperatura"]) + "°",
        "| SatO2:", str(signos["saturacion_o2"]) + "%\n",
    )
    return signos


if __name__ == "__main__":
    import sys
    import os

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "SU-16")))
    from backPacientes import buscarPaciente, ingresarPaciente, derivarPacienteATriage, pacientes_admitidos, pacientes_en_triage

    print("\n=== SANATORIO UNDAV - MÓDULO DE TRIAGE ===")
    dni = input("Ingresá DNI / N° de Afiliado del paciente a evaluar: ").strip()
    paciente = buscarPaciente(pacientes_admitidos, dni)

    if paciente is None:
        print("Aviso: Paciente no encontrado en memoria; cargando registro de admisión de prueba...")
        paciente = {
            "dni_afiliado": dni,
            "nombre_apellido": input("Nombre y Apellido del paciente: ").strip(),
            "edad": int(input("Edad: ").strip()),
            "obra_social": "OSDE",
            "plan": "210",
            "motivo_consulta": "Control en guardia",
        }
        ingresarPaciente(paciente, pacientes_admitidos)
        derivarPacienteATriage(paciente, pacientes_admitidos, pacientes_en_triage)

    signos = formulario_signos_vitales(paciente)
    resultado = registrar_signos_vitales(dni, signos, pacientes_admitidos, pacientes_en_triage)
    if resultado:
        print("Signos vitales vinculados correctamente al registro de admisión del paciente.")
    else:
        print("Error: No se pudieron vincular los signos vitales (verificá que TA diastólica < sistólica).")
