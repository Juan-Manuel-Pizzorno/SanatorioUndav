//Ejecutando en la terminal "node --test testing/*.test.mjs" el sistema realiza el testing para todos los casos

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
  TODOS_LOS_MODULOS,
  iniciarSesion,
  tieneAccesoModulo,
  obtenerSesionActiva,
  cerrarSesion
} = await import('../back/auth.js');

describe('Suite de Testing Funcional y Seguridad RBAC — Sanatorio UNDAV (SU-39)', () => {

  beforeEach(() => {
    sessionStorage.clear();
  });

  describe('A. Pruebas Positivas (Flujos Válidos)', () => {

    it('CP-01: Estructura de datos contiene los 6 roles operativos definidos en el ERS', () => {
      const rolesEsperados = ['Admisión', 'Triage', 'Médico', 'Jefe de Guardia', 'Administrativo', 'TI'];
      const rolesUnicosEnJSON = [...new Set(usuariosJSON.map((u) => u.rol))];
      assert.deepEqual(rolesUnicosEnJSON, rolesEsperados);
    });

    it('CP-02: Inicio de sesión exitoso para todos los perfiles operativos con clave válida', async () => {
      for (const u of usuariosJSON) {
        const res = await iniciarSesion(u.email, '1234');
        assert.equal(res.ok, true, `Falló el login válido para ${u.rol}`);
        assert.equal(res.usuario.rol, u.rol);
        assert.equal(res.usuario.password, undefined, 'La contraseña nunca debe exponerse en la sesión');
      }
    });

    it('CP-03: Normalización de correo (mayúsculas y espacios laterales) permite ingresar', async () => {
      const res = await iniciarSesion('   SOFIA.MARTINEZ@UNDAV.EDU.AR  ', '1234');
      assert.equal(res.ok, true);
      assert.equal(res.usuario.nombre, 'Dra. Sofía Martínez');
      assert.equal(res.usuario.matricula, 'MP-45821');
    });

    it('CP-04: Persistencia y cierre de sesión limpian correctamente el estado', async () => {
      await iniciarSesion('laura.gomez@undav.edu.ar', '1234');
      assert.notEqual(obtenerSesionActiva(), null, 'La sesión debe quedar guardada tras login');

      cerrarSesion();
      assert.equal(obtenerSesionActiva(), null, 'La sesión debe quedar nula tras logout');
    });

    it('CP-05: Cada rol tiene acceso positivo a sus pantallas asignadas', async () => {
      const { usuario: triage } = await iniciarSesion('carlos.mendez@undav.edu.ar', '1234');
      assert.equal(tieneAccesoModulo(triage, 'Registro de Parámetros Fisiológicos'), true);
      assert.equal(tieneAccesoModulo(triage, 'Clasificación Triage'), true);

      const { usuario: jefe } = await iniciarSesion('roberto.silva@undav.edu.ar', '1234');
      assert.equal(tieneAccesoModulo(jefe, 'Tablero de Control en Tiempo Real'), true);
      assert.equal(tieneAccesoModulo(jefe, 'Autorización de Derivaciones'), true);
    });
  });

  describe('B. Pruebas Negativas (Credenciales Inválidas y Bloqueo RBAC)', () => {

    it('CP-06: Rechaza contraseña incorrecta para un usuario válido', async () => {
      const res = await iniciarSesion('sofia.martinez@undav.edu.ar', 'clave_incorrecta');
      assert.equal(res.ok, false);
      assert.match(res.mensaje, /Credenciales inválidas/i);
      assert.equal(obtenerSesionActiva(), null);
    });

    it('CP-07: Rechaza correo institucional inexistente en el padrón', async () => {
      const res = await iniciarSesion('intruso@undav.edu.ar', '1234');
      assert.equal(res.ok, false);
      assert.match(res.mensaje, /Credenciales inválidas/i);
    });

    it('CP-08: Rechaza intentos de login con campos vacíos o solo espacios', async () => {
      const resVacio = await iniciarSesion('', '');
      assert.equal(resVacio.ok, false);
      assert.match(resVacio.mensaje, /Completá correo y contraseña/i);

      const resEspacios = await iniciarSesion('   ', '1234');
      assert.equal(resEspacios.ok, false);
    });

    it('CP-09: Rechaza inyección básica o formato inválido en credenciales', async () => {
      const resSQLi = await iniciarSesion("' OR '1'='1", "' OR '1'='1");
      assert.equal(resSQLi.ok, false);
      assert.equal(obtenerSesionActiva(), null);
    });

    it('CP-10: Matriz RBAC — Bloquea estrictamente el acceso a pantallas de otros roles', async () => {
      for (const u of usuariosJSON) {
        const { usuario } = await iniciarSesion(u.email, '1234');
        const modulosProhibidos = TODOS_LOS_MODULOS.filter(
          (m) => !u.pantallas_permitidas.includes(m)
        );

        assert.ok(modulosProhibidos.length > 0, `El rol ${u.rol} debería tener módulos restringidos`);

        for (const moduloAjeno of modulosProhibidos) {
          assert.equal(
            tieneAccesoModulo(usuario, moduloAjeno),
            false,
            `FALLO DE SEGURIDAD: El rol ${u.rol} accedió al módulo ajeno "${moduloAjeno}"`
          );
        }
      }
    });

    it('CP-11: Usuario no autenticado (null) no tiene acceso a ningún módulo', () => {
      for (const modulo of TODOS_LOS_MODULOS) {
        assert.equal(tieneAccesoModulo(null, modulo), false);
      }
    });
  });
});