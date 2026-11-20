import assert from 'node:assert';
import fs from 'node:fs';

const usuarios = JSON.parse(fs.readFileSync('./back/usuarios.json', 'utf-8'));

// Prueba 1: Existen los 6 roles operativos del ERS
const rolesEsperados = ['Admisión', 'Triage', 'Médico', 'Jefe de Guardia', 'Administrativo', 'TI'];
const rolesCargados = usuarios.map(u => u.rol);
assert.deepStrictEqual(rolesCargados, rolesEsperados, 'Faltan roles operativos en usuarios.json');

// Prueba 2: Credenciales válidas encuentran usuario
const medico = usuarios.find(u => u.email === 'medico@undav.edu.ar' && u.password === '1234');
assert.ok(medico, 'No se pudo autenticar al médico de prueba');

// Prueba 3: Restricción de permisos (Triage no debe tener acceso a Alta de Profesionales)
const triage = usuarios.find(u => u.rol === 'Triage');
assert.strictEqual(triage.pantallas_permitidas.includes('Alta de Profesionales'), false, 'Falla de seguridad RBAC');

console.log('✅ Todas las pruebas funcionales de SU-39 pasaron correctamente.');