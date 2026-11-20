# Formulario de admisión de paciente en guardia

def pedir_texto(mensaje, solo_letras=False):
    """Pide un texto por consola, valida longitud mínima y opcionalmente que sean solo letras."""
    while True:
        valor = input(mensaje).strip()
        if len(valor) < 2:
            print("Error: Ingresá al menos 2 caracteres.")
            continue
        if solo_letras and not all(c.isalpha() or c.isspace() for c in valor):
            print("Error: Este campo solo puede contener letras y espacios.")
            continue
        return valor


def pedir_dni_afiliado():
    """Pide DNI o N° de Afiliado y valida que sean solo números (7 a 12 dígitos)."""
    while True:
        valor = input("DNI / N° de Afiliado (solo números): ").strip()
        if valor.isdigit() and 7 <= len(valor) <= 12:
            return valor
        print("Error: Ingresá solo números (entre 7 y 12 dígitos, sin puntos ni guiones).")


def pedir_edad():
    """Pide la edad y valida que sea un número entero entre 0 y 100."""
    while True:
        entrada = input("Edad: ").strip()
        if entrada.isdigit() and 0 <= int(entrada) <= 100:
            return int(entrada)
        print("Error: Ingresá una edad válida (número entre 0 y 100).")


def formulario_admision():
    """Muestra el formulario de admisión por consola y devuelve los datos del paciente."""
    print("\n=== SANATORIO UNDAV - ADMISIÓN DE GUARDIA ===\n")

    paciente = {
        "dni_afiliado": pedir_dni_afiliado(),
        "nombre_apellido": pedir_texto("Nombre y Apellido: ", solo_letras=True),
        "edad": pedir_edad(),
        "obra_social": pedir_texto("Obra Social: "),
        "plan": pedir_texto("Plan: "),
        "motivo_consulta": pedir_texto("Motivo de consulta: "),
    }

    print("\n--- Resumen de datos ingresados ---")
    for clave, valor in paciente.items():
        print(f"  {clave}: {valor}")
    print("-----------------------------------\n")

    return paciente


if __name__ == "__main__":
    datos_paciente = formulario_admision()
    print("Formulario completado correctamente.")
