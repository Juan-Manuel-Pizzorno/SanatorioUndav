// [SU-38 / SU-40 / SU-42] Back: Validación de credenciales, RBAC, matrícula médica y adaptación de permisos por contexto

export const TODOS_LOS_MODULOS = [
  "Registro de Guardia",
  "Búsqueda por DNI/Afiliado",
  "Registro de Parámetros Fisiológicos",
  "Clasificación Triage",
  "Atención de Guardia",
  "Agenda de Consultorios",
  "Historia Clínica",
  "Recetas Electrónicas",
  "Solicitud de Estudios",
  "Solicitud de Derivaciones",
  "Tablero de Control en Tiempo Real",
  "Autorización de Derivaciones",
  "Validación de Órdenes Médicas",
  "Gestión de Agenda",
  "Alta de Profesionales",
  "Parametrización Obras Sociales",
  "Reglas CIE-10"
];

const BACKUP_USUARIOS = [
  { id: 1, nombre: "Laura Gómez", email: "laura.gomez@undav.edu.ar", password: "1234", rol: "Admisión", pantallas_permitidas: ["Registro de Guardia", "Búsqueda por DNI/Afiliado"] },
  { id: 2, nombre: "Carlos Méndez", email: "carlos.mendez@undav.edu.ar", password: "1234", rol: "Triage", pantallas_permitidas: ["Registro de Parámetros Fisiológicos", "Clasificación Triage"] },
  {
    id: 3,
    nombre: "Dra. Sofía Martínez",
    email: "sofia.martinez@undav.edu.ar",
    password: "1234",
    rol: "Médico",
    matricula: "MP-45821",
    doble_contexto: true,
    contextos_habilitados: ["Guardia", "Consultorios Externos"],
    permisos_por_contexto: {
      "Guardia": ["Atención de Guardia", "Historia Clínica", "Recetas Electrónicas", "Solicitud de Derivaciones"],
      "Consultorios Externos": ["Agenda de Consultorios", "Historia Clínica", "Recetas Electrónicas", "Solicitud de Estudios"]
    },
    pantallas_permitidas: ["Atención de Guardia", "Historia Clínica", "Recetas Electrónicas"]
  },
  { id: 4, nombre: "Dr. Roberto Silva", email: "roberto.silva@undav.edu.ar", password: "1234", rol: "Jefe de Guardia", pantallas_permitidas: ["Tablero de Control en Tiempo Real", "Autorización de Derivaciones"] },
  { id: 5, nombre: "Mariana Torres", email: "mariana.torres@undav.edu.ar", password: "1234", rol: "Administrativo", pantallas_permitidas: ["Validación de Órdenes Médicas", "Gestión de Agenda"] },
  { id: 6, nombre: "Juan Pizzorno", email: "juan.pizzorno@undav.edu.ar", password: "1234", rol: "TI", pantallas_permitidas: ["Alta de Profesionales", "Parametrización Obras Sociales", "Reglas CIE-10"] },
  { id: 7, nombre: "Dr. Lucas Pereyra", email: "lucas.pereyra@undav.edu.ar", password: "1234", rol: "Médico", matricula: "MP-51204", doble_contexto: false, contexto_activo: "Consultorios Externos", pantallas_permitidas: ["Agenda de Consultorios", "Historia Clínica", "Recetas Electrónicas", "Solicitud de Estudios"] }
];

async function cargarUsuarios() {
  try {
    const urlJson = new URL('./usuarios.json', import.meta.url);
    const resp = await fetch(urlJson);
    if (!resp.ok) throw new Error('Error al leer usuarios.json');
    return await resp.json();
  } catch (error) {
    return BACKUP_USUARIOS;
  }
}

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

  if (usuario.rol === 'Médico' && !usuario.matricula) {
    return { ok: false, mensaje: 'Error de configuración: el perfil médico no posee una matrícula vinculada.' };
  }

  const { password: _, ...datosSesion } = usuario;

  if (datosSesion.rol === 'Médico' && datosSesion.doble_contexto) {
    datosSesion.contexto_activo = null;
  }

  sessionStorage.setItem('sesion_undav', JSON.stringify(datosSesion));

  return {
    ok: true,
    usuario: datosSesion,
    requiereSeleccionContexto: Boolean(datosSesion.rol === 'Médico' && datosSesion.doble_contexto)
  };
}

export function seleccionarContextoMedico(contexto) {
  const sesion = obtenerSesionActiva();
  if (!sesion || sesion.rol !== 'Médico' || !sesion.matricula) {
    return { ok: false, mensaje: 'No hay un médico autenticado con matrícula válida.' };
  }

  const permitidos = sesion.contextos_habilitados || [];
  if (!permitidos.includes(contexto)) {
    return { ok: false, mensaje: `El ámbito "${contexto}" no está habilitado para la matrícula ${sesion.matricula}.` };
  }

  sesion.contexto_activo = contexto;
  if (sesion.permisos_por_contexto && sesion.permisos_por_contexto[contexto]) {
    sesion.pantallas_permitidas = sesion.permisos_por_contexto[contexto];
  }

  sessionStorage.setItem('sesion_undav', JSON.stringify(sesion));
  return { ok: true, usuario: sesion };
}

export function tieneAccesoModulo(usuario, nombreModulo) {
  if (!usuario || !Array.isArray(usuario.pantallas_permitidas)) return false;
  return usuario.pantallas_permitidas.includes(nombreModulo);
}

export function obtenerSesionActiva() {
  const raw = sessionStorage.getItem('sesion_undav');
  return raw ? JSON.parse(raw) : null;
}

export function cerrarSesion() {
  sessionStorage.removeItem('sesion_undav');
}