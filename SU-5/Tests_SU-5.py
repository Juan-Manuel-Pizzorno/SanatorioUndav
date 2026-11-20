# [SU-43] Pruebas unitarias de acceso por matrícula y cambio de contexto médico
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "SU-4")))

from backUsuarios import iniciar_sesion, tiene_acceso_modulo
from backContexto import requiere_seleccion_contexto, seleccionar_contexto_medico


def test_medico_doble_ambito_requiere_selector():
    medico = iniciar_sesion("sofia.martinez@undav.edu.ar", "1234")
    assert medico["matricula"] == "MP-45821"
    assert requiere_seleccion_contexto(medico)


def test_seleccionar_contexto_guardia():
    medico = iniciar_sesion("sofia.martinez@undav.edu.ar", "1234")
    en_guardia = seleccionar_contexto_medico(medico, "Guardia")

    assert en_guardia is not None
    assert en_guardia["contexto_activo"] == "Guardia"
    assert tiene_acceso_modulo(en_guardia, "Atención de Guardia")
    assert not tiene_acceso_modulo(en_guardia, "Agenda de Consultorios")


def test_seleccionar_contexto_consultorios():
    medico = iniciar_sesion("sofia.martinez@undav.edu.ar", "1234")
    en_consultorios = seleccionar_contexto_medico(medico, "Consultorios Externos")

    assert en_consultorios is not None
    assert en_consultorios["contexto_activo"] == "Consultorios Externos"
    assert tiene_acceso_modulo(en_consultorios, "Agenda de Consultorios")
    assert not tiene_acceso_modulo(en_consultorios, "Atención de Guardia")


def test_medico_ambito_unico_no_requiere_selector():
    medico = iniciar_sesion("lucas.pereyra@undav.edu.ar", "1234")
    assert medico["matricula"] == "MP-51204"
    assert not requiere_seleccion_contexto(medico)
    assert medico["contexto_activo"] == "Consultorios Externos"


def test_negar_contexto_no_habilitado():
    medico = iniciar_sesion("lucas.pereyra@undav.edu.ar", "1234")
    resultado = seleccionar_contexto_medico(medico, "Guardia")
    assert resultado is None


def test_negar_cambio_contexto_usuario_no_medico():
    admision = iniciar_sesion("laura.gomez@undav.edu.ar", "1234")
    resultado = seleccionar_contexto_medico(admision, "Guardia")
    assert resultado is None