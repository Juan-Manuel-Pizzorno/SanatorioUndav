# Editar el nombre donde estén las funciones que se usan... buscarPaciente, esPacientePediatrico e ingresarPaciente 
# me parece que pueden ir en un módulo común porque ¿no son bastante usadas? Si es así habría que separar el
# import en los archivos que haga falta
from ARCHIVOCONLASFUNCIONES import (buscarPaciente, esPacientePediatrico,
EDAD_MAXIMA_PEDIATRIA, ingresarPaciente, derivarPacienteATriage)

def test_admision():
    pacienteGenerico = {"dni_afiliado": "12345678"}
    listaPacientesAdmitidos = []
    ingresarPaciente(pacienteGenerico, listaPacientesAdmitidos)
    assert (buscarPaciente(listaPacientesAdmitidos, pacienteGenerico["dni_afiliado"])
             is not None)

def test_negarDobleAdmision():
    pacienteGenerico = {"dni_afiliado": "12345678"}
    listaPacientesAdmitidos = [pacienteGenerico]
    ingresarPaciente(pacienteGenerico, listaPacientesAdmitidos)
    assert (buscarPaciente(listaPacientesAdmitidos, pacienteGenerico["dni_afiliado"])
             is not None)
    assert (len(listaPacientesAdmitidos) == 1)

def test_esPediatrico (edadMaxima = EDAD_MAXIMA_PEDIATRIA):
    pacienteMenor = {"edad": edadMaxima - 1}
    pacienteMismo = {"edad": edadMaxima }
    pacienteMayor = {"edad": edadMaxima + 1}
    assert esPacientePediatrico(pacienteMenor, edadMaxima)
    assert esPacientePediatrico(pacienteMismo, edadMaxima)
    assert not esPacientePediatrico(pacienteMayor, edadMaxima)

def test_derivadoATriage():
    pacienteGenerico = {"dni_afiliado": "12345678"}
    listaPacientesAdmitidos = []
    listaPacientesEnTriage = []
    ingresarPaciente(pacienteGenerico, listaPacientesAdmitidos)
    derivarPacienteATriage(pacienteGenerico,
                            listaPacientesAdmitidos, listaPacientesEnTriage)
    assert (buscarPaciente(listaPacientesAdmitidos, pacienteGenerico["dni_afiliado"])
            is not None)
    assert (buscarPaciente(listaPacientesEnTriage, pacienteGenerico["dni_afiliado"])
            is not None)

def test_negarDerivacionTriageUnNoAdmitido():
    pacienteGenerico = {"dni_afiliado": "12345678"}
    listaPacientesAdmitidos = []
    listaPacientesEnTriage = []
    derivarPacienteATriage(pacienteGenerico, listaPacientesAdmitidos,
                            listaPacientesEnTriage)
    assert (buscarPaciente(listaPacientesEnTriage, pacienteGenerico["dni_afiliado"])
             is None)

def test_negarDobleDerivacionTriage():
    pacienteGenerico = {"dni_afiliado": "12345678"}
    listaPacientesAdmitidos = [pacienteGenerico]
    listaPacientesEnTriage = [pacienteGenerico]
    derivarPacienteATriage(pacienteGenerico, listaPacientesAdmitidos,
                            listaPacientesEnTriage)
    assert len(listaPacientesEnTriage) == 1
