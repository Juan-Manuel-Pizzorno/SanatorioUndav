# [SU-44] Formulario de admisión de paciente en guardia
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "FuncionesDeValidacion")))

from backPacientes import esPacientePediatrico, guardar_ingreso_y_derivar
from Validaciones import pedir_cadena_numerica, pedir_entero, pedir_texto


def formulario_admision():
    """Muestra el formulario de admisión por consola, guarda el ingreso y deriva a Triage."""
    print("\n=== SANATORIO UNDAV - ADMISIÓN DE GUARDIA ===\n")

    paciente = {
        "dni_afiliado": pedir_cadena_numerica(
            "DNI / N° de Afiliado (solo números): ",
            7,
            12,
            "Error: Ingresá solo números (entre 7 y 12 dígitos): ",
        ),
        "nombre_apellido": pedir_texto(
            "Nombre y Apellido: ",
            "Error: Ingresá al menos 2 caracteres (solo letras y espacios): ",
            solo_letras=True,
        ),
        "edad": pedir_entero(
            "Edad: ",
            0,
            100,
            "Error: Ingresá una edad válida (0 a 100): ",
        ),
        "obra_social": pedir_texto("Obra Social: ", "Error: Ingresá al menos 2 caracteres: "),
        "plan": pedir_texto("Plan: ", "Error: Ingresá al menos 2 caracteres: "),
        "motivo_consulta": pedir_texto("Motivo de consulta: ", "Error: Ingresá al menos 2 caracteres: "),
    }

    tipo_atencion = "Pediátrica (hasta 16 años)" if esPacientePediatrico(paciente) else "Adultos"

    print("\n--- Resumen de datos ingresados ---")
    for clave, valor in paciente.items():
        print(f"  {clave}: {valor}")
    print(f"  tipo_atencion: {tipo_atencion}")
    print("-----------------------------------\n")

    if guardar_ingreso_y_derivar(paciente):
        print("Ingreso guardado y paciente derivado automáticamente a la cola de Triage.")
        return paciente

    print("Error: El paciente ya se encuentra admitido o los datos son inválidos.")
    return None


if __name__ == "__main__":
    datos_paciente = formulario_admision()
    if datos_paciente is not None:
        print("Formulario completado correctamente.")
