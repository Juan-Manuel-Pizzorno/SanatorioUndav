// back/auth.js - Lógica de autenticación y control de acceso por roles (SU-38)

export const TODOS_LOS_MODULOS = [
  "Registro de Guardia",
  "Búsqueda por DNI/Afiliado",
  "Registro de Parámetros Fisiológicos",
  "Clasificación Triage",
  "Atención de Guardia",
  "Historia Clínica",
  "Recetas Electrónicas",
  "Tablero de Control en Tiempo Real",
  "Autorización de Derivaciones",
  "Validación de Órdenes Médicas",
  "Gestión de Agenda",
  "Alta de Profesionales",
  "Parametrización Obras Sociales",
  "Reglas CIE-10"
];

const BACKUP_USUARIOS = [
  { nombre: "Laura Gómez", email: "admision@undav.edu.ar", password: "1234", rol: "Admisión", pantallas_permitidas: ["Registro de Guardia", "Búsqueda por DNI/Afiliado"] },
  { nombre: "Carlos Méndez", email: "triage@undav.edu.ar", password: "1234", rol: "Triage", pantallas_permitidas: ["Registro de Parámetros Fisiológicos", "Clasificación Triage"] },
  { nombre: "Dra. Sofía Martínez", email: "medico@undav.edu.ar", password: "1234", rol: "Médico", matricula: "MP-45821", pantallas_permitidas: ["Atención de Guardia", "Historia Clínica", "Recetas Electrónicas"] },
  { nombre: "Dr. Roberto Silva", email: "jefe@undav.edu.ar", password: "1234", rol: "Jefe de Guardia", pantallas_permitidas: ["Tablero de Control en Tiempo Real", "Autorización de Derivaciones"] },
  { nombre: "Mariana Torres", email: "admin.consultorios@undav.edu.ar", password: "1234", rol: "Administrativo", pantallas_permitidas: ["Validación de Órdenes Médicas", "Gestión de Agenda"] },
  { nombre: "Juan Pizzorno", email: "ti@undav.edu.ar", password: "1234", rol: "TI", pantallas_permitidas: ["Alta de Profesionales", "Parametrización Obras Sociales", "Reglas CIE-10"] }
];

async function cargarUsuarios() {
  try {
    const resp = await fetch('../back/usuarios.json');
    if (!resp.ok) throw new Error('Error al leer usuarios.json');
    return await resp.json();
  } catch (error) {
    return BACKUP_USUARIOS;
  }
}

// 1. Valida credenciales y guarda la sesión activa
export async function iniciarSesion(email, password) {
  const emailLimpio = email.trim().toLowerCase();
  if (!emailLimpio || !password) {
    return { ok: false, mensaje: 'Completá correo y contraseña.' };
  }

  const usuarios = await cargarUsuarios();
  const usuario = usuarios.find(
    (u) => u.email.toLowerCase() === emailLimpio && u.password === password
  );

  if (!usuario) {
    return { ok: false, mensaje: 'Credenciales inválidas. Verificá tu correo institucional y contraseña.' };
  }

  // Guardamos el usuario autenticado (sin la contraseña) en la sesión del navegador
  const { password: _, ...datosSesion } = usuario;
  sessionStorage.setItem('sesion_undav', JSON.stringify(datosSesion));

  return { ok: true, usuario: datosSesion };
}

// 2. Verifica si un rol tiene acceso autorizado a un módulo específico
export function tieneAccesoModulo(usuario, nombreModulo) {
  if (!usuario || !Array.isArray(usuario.pantallas_permitidas)) return false;
  return usuario.pantallas_permitidas.includes(nombreModulo);
}

// 3. Recupera la sesión activa si recargan la página
export function obtenerSesionActiva() {
  const raw = sessionStorage.getItem('sesion_undav');
  return raw ? JSON.parse(raw) : null;
}

// 4. Cierra la sesión y limpia permisos
export function cerrarSesion() {
  sessionStorage.removeItem('sesion_undav');
}