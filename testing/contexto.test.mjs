// [SU-43] Testing: Pruebas positivas y negativas de acceso por matrícula y selector de contexto médico
import { describe, it, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

const usuariosJSON = JSON.parse(fs.readFileSync('./back/usuarios.json', 'utf-8'));

globalThis.fetch = async () => ({
  ok: true,
  json: async () => usuariosJSON
});

const storage = new Map();
globalThis.sessionStorage = {
  getItem: (k) => (storage.has(k) ? storage.get(k) : null),
  setItem: (k, v) => storage.set(k, String(v)),
  removeItem: (k) => storage.delete(k),
  clear: () => storage.clear()
};

const {
  iniciarSesion,
  seleccionarContextoMedico,
  tieneAccesoModulo,
  obtenerSesionActiva
} = await import('../back/auth.js');

describe('Suite de Testing — Selector de Contexto Médico y Matrícula (SU-43)', () => {

  beforeEach(() => {
    sessionStorage.clear();
  });

  // =========================================================================
  // BLOQUE A: PRUEBAS POSITIVAS (FLUJOS VÁLIDOS DE MATRÍCULA Y CONTEXTO)
  // =========================================================================
  describe('A. Pruebas Positivas (Acceso y Adaptación por Ámbito)', () => {

    it('CP-12: Médico con doble ámbito ingresa con usuario único vinculado a su matrícula y solicita selección', async () => {
      const res = await iniciarSesion('medico@undav.edu.ar', '1234');
      assert.equal(res.ok, true);
      assert.equal(res.usuario.matricula, 'MP-45821');
      assert.equal(res.requiereSeleccionContexto, true);
      assert.equal(res.usuario.contexto_activo, null);
    });

    it('CP-13: Selección de contexto "Guardia" habilita herramientas de urgencia y bloquea agenda externa', async () => {
      await iniciarSesion('medico@undav.edu.ar', '1234');
      const res = seleccionarContextoMedico('Guardia');

      assert.equal(res.ok, true);
      assert.equal(res.usuario.contexto_activo, 'Guardia');
      assert.equal(tieneAccesoModulo(res.usuario, 'Atención de Guardia'), true);
      assert.equal(tieneAccesoModulo(res.usuario, 'Solicitud de Derivaciones'), true);
      assert.equal(tieneAccesoModulo(res.usuario, 'Agenda de Consultorios'), false);
      assert.equal(tieneAccesoModulo(res.usuario, 'Solicitud de Estudios'), false);
    });

    it('CP-14: Selección de contexto "Consultorios Externos" adapta la interfaz a agenda y estudios', async () => {
      await iniciarSesion('medico@undav.edu.ar', '1234');
      const res = seleccionarContextoMedico('Consultorios Externos');

      assert.equal(res.ok, true);
      assert.equal(res.usuario.contexto_activo, 'Consultorios Externos');
      assert.equal(tieneAccesoModulo(res.usuario, 'Agenda de Consultorios'), true);
      assert.equal(tieneAccesoModulo(res.usuario, 'Solicitud de Estudios'), true);
      assert.equal(tieneAccesoModulo(res.usuario, 'Atención de Guardia'), false);
      assert.equal(tieneAccesoModulo(res.usuario, 'Solicitud de Derivaciones'), false);
    });

    it('CP-15: Cambio dinámico de ámbito en sesión activa actualiza permisos al instante', async () => {
      await iniciarSesion('medico@undav.edu.ar', '1234');
      seleccionarContextoMedico('Guardia');
      assert.equal(tieneAccesoModulo(obtenerSesionActiva(), 'Atención de Guardia'), true);

      const cambio = seleccionarContextoMedico('Consultorios Externos');
      assert.equal(cambio.ok, true);
      assert.equal(tieneAccesoModulo(obtenerSesionActiva(), 'Atención de Guardia'), false);
      assert.equal(tieneAccesoModulo(obtenerSesionActiva(), 'Agenda de Consultorios'), true);
    });

    it('CP-16: Médico habilitado en un único ámbito ingresa directo sin selector intermedio', async () => {
      const res = await iniciarSesion('consultorios.medico@undav.edu.ar', '1234');
      assert.equal(res.ok, true);
      assert.equal(res.usuario.matricula, 'MP-51204');
      assert.equal(res.requiereSeleccionContexto, false);
      assert.equal(res.usuario.contexto_activo, 'Consultorios Externos');
      assert.equal(tieneAccesoModulo(res.usuario, 'Agenda de Consultorios'), true);
    });
  });

  // =========================================================================
  // BLOQUE B: PRUEBAS NEGATIVAS (RESTRICCIONES Y VALIDACIÓN DE MATRÍCULA)
  // =========================================================================
  describe('B. Pruebas Negativas (Bloqueos de Matrícula y Ámbitos No Autorizados)', () => {

    it('CP-17: Rechaza médico de ámbito único intentando cambiar a un contexto no habilitado', async () => {
      await iniciarSesion('consultorios.medico@undav.edu.ar', '1234');
      const res = seleccionarContextoMedico('Guardia');

      assert.equal(res.ok, false);
      assert.match(res.mensaje, /no está habilitado para la matrícula MP-51204/i);
    });

    it('CP-18: Rechaza selección de un ámbito operativo inexistente', async () => {
      await iniciarSesion('medico@undav.edu.ar', '1234');
      const res = seleccionarContextoMedico('Quirófano Central');

      assert.equal(res.ok, false);
      assert.match(res.mensaje, /no está habilitado/i);
    });

    it('CP-19: Rechaza cambio de contexto si el usuario autenticado no tiene rol Médico', async () => {
      await iniciarSesion('admision@undav.edu.ar', '1234');
      const res = seleccionarContextoMedico('Guardia');

      assert.equal(res.ok, false);
      assert.match(res.mensaje, /No hay un médico autenticado/i);
    });

    it('CP-20: Rechaza cambio de contexto sin sesión activa', () => {
      const res = seleccionarContextoMedico('Guardia');
      assert.equal(res.ok, false);
    });
  });
});