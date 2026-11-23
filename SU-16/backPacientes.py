# [SU-16] Backend de admisión de pacientes y derivación automática a Triage [SU-46]
from FuncionesSU_45 import (
    EDAD_MAXIMA_PEDIATRIA,
    buscarPaciente,
    esPacientePediatrico,
    ingresarPaciente,
    derivarPacienteATriage,
)

# Listas compartidas en memoria (importadas por SU-17/backTriage.py)
pacientes_admitidos = []
pacientes_en_triage = []


def guardar_ingreso_y_derivar(
    paciente,
    pacientesAdmitidos=pacientes_admitidos,
    pacientesEnTriage=pacientes_en_triage,
):
    """
    [SU-46] Valida datos mínimos, guarda el ingreso en admisión y deriva
    automáticamente el paciente a la cola de espera de Triage.
    Devuelve True si se realizó correctamente, o False si ya estaba ingresado o faltan datos.
    """
    campos_obligatorios = (
        "dni_afiliado",
        "nombre_apellido",
        "edad",
        "obra_social",
        "plan",
        "motivo_consulta",
    )
    if not isinstance(paciente, dict):
        return False
    for campo in campos_obligatorios:
        if campo not in paciente or paciente[campo] in (None, ""):
            return False

    if buscarPaciente(pacientesAdmitidos, paciente["dni_afiliado"]) is not None:
        return False

    ingresarPaciente(paciente, pacientesAdmitidos)
    derivarPacienteATriage(paciente, pacientesAdmitidos, pacientesEnTriage)

    return (
        buscarPaciente(pacientesAdmitidos, paciente["dni_afiliado"]) is not None
        and buscarPaciente(pacientesEnTriage, paciente["dni_afiliado"]) is not None
    )