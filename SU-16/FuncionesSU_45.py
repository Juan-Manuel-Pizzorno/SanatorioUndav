EDAD_MAXIMA_PEDIATRIA = 16
#Recibe un número de DNI o de Afiliado y una lista.
#Devuelve un paciente o None si no lo encuentra
def buscarPaciente (listaDePacientes, nro_DNI_Afiliado):
    i = 0
    cantDePacientes = len(listaDePacientes)
    while (i<cantDePacientes
        and listaDePacientes[i]["dni_afiliado"] != nro_DNI_Afiliado):
        i+=1
    return (listaDePacientes[i] if i < cantDePacientes else None)

# Recibe un paciente
# Devuelve un booleano. True si es menor o igual a la edad máxima y False si es mayor
def esPacientePediatrico (paciente, edadMaxima = EDAD_MAXIMA_PEDIATRIA):
    return paciente["edad"] <= edadMaxima

def ingresarPaciente (paciente, pacientesAdmitidos):
    seEncontroAlPaciente = buscarPaciente(pacientesAdmitidos, paciente["dni_afiliado"])
    if seEncontroAlPaciente is None:
        pacientesAdmitidos.append(paciente)
    

def derivarPacienteATriage (paciente, pacientesAdmitidos, pacientesEnTriage):
    pacienteAdmitido = buscarPaciente(pacientesAdmitidos, paciente["dni_afiliado"])
    estaEnTriage = buscarPaciente(pacientesEnTriage, paciente["dni_afiliado"])
    if (estaEnTriage is None and pacienteAdmitido):
        pacientesEnTriage.append(paciente)
