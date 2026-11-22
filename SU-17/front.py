from Validaciones_SU17 import pedir_entero, pedir_decimal
def formulario_signos_vitales(paciente):
    print("\n--- Triage:", paciente["nombre"], paciente["apellido"], "(DNI:", paciente["dni_afiliado"] + ") ---")

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
        "\n--- Resumen de signos vitales registrados ---\n" +
        "TA:", str(signos["ta_sistolica"]) + "/" + str(signos["ta_diastolica"]),
        "| FC:", signos["frecuencia_cardiaca"],
        "| FR:", signos["frecuencia_respiratoria"],
        "| Temp:", str(signos["temperatura"]) + "°",
        "| SatO2:", str(signos["saturacion_o2"]) + "%\n"
    )
    return signos 
