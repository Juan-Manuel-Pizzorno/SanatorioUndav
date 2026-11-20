# Plan y Ejecución de Pruebas — Historia SU-4 (`SU-39`)
**Proyecto:** Sistema Integral de Gestión Hospitalaria — Sanatorio UNDAV  
**Entorno probado:** `https://juan-manuel-pizzorno.github.io/SanatorioUndav/` + Suite Node (`testing/01-login.test.mjs`)

## 1. Casos de Prueba Positivos (Acceso y Permisos Habilitados)

| ID | Caso de Prueba | Datos de Entrada | Resultado Esperado | Resultado Obtenido | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CP-00** | Padrón completo de roles ERS | Archivo `back/usuarios.json` | Contener los 6 roles operativos: Admisión, Triage, Médico, Jefe de Guardia, Administrativo y TI. | Los 6 perfiles están cargados con sus permisos diferenciados. | **PASS** |
| **CP-01** | Login exitoso por perfil (todos los usuarios) | Correo nominal de cada usuario + clave `1234` | Autentica al usuario, oculta la contraseña en sesión y despliega su panel operativo. | Todos los perfiles ingresaron correctamente. | **PASS** |
| **CP-02** | Normalización de correo institucional | `  SOFIA.MARTINEZ@UNDAV.EDU.AR ` / `1234` | Ignora mayúsculas y espacios, autentica a *Dra. Sofía Martínez* y muestra `MP-45821`. | Ingresó y mostró nombre, rol y matrícula profesional. | **PASS** |
| **CP-03** | Persistencia y cierre de sesión | Login válido (`laura.gomez@undav.edu.ar`) + *Cerrar sesión* | Mantiene sesión en `sessionStorage` al recargar y la limpia por completo al salir. | Al cerrar sesión vuelve al login limpio y sin permisos residuales. | **PASS** |
| **CP-04** | Habilitación de módulos propios | Perfil `Triage` (`carlos.mendez@undav.edu.ar`) | Habilita *Registro de Parámetros Fisiológicos* y *Clasificación Triage*. | Ambos módulos figuran con estado `✓ Acceso habilitado`. | **PASS** |

## 2. Casos de Prueba Negativos (Errores de Autenticación y Bloqueo RBAC)

| ID | Caso de Prueba | Datos de Entrada | Resultado Esperado | Resultado Obtenido | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CP-05** | Contraseña incorrecta | `sofia.martinez@undav.edu.ar` / `clave_incorrecta` | Deniega acceso, no crea sesión y muestra alerta visual de error. | Banner rojo: *"Credenciales inválidas. Verificá tu correo institucional y contraseña."* | **PASS** |
| **CP-06** | Correo institucional inexistente | `intruso@undav.edu.ar` / `1234` | Deniega acceso y muestra mensaje de error sin revelar si el correo existe. | Banner rojo de credenciales inválidas; acceso bloqueado. | **PASS** |
| **CP-07** | Campos vacíos o solo espacios | Correo: `""` o `"   "` / Clave: `""` | Impide el envío / rechaza validación solicitando completar ambos campos. | Validación HTML5 + validación backend bloquean el ingreso. | **PASS** |
| **CP-08** | Intento de inyección en credenciales | `' OR '1'='1` en correo y clave | Rechaza la entrada como texto plano inválido sin comprometer la sesión. | Acceso denegado; `sessionStorage` permanece vacío. | **PASS** |
| **CP-09** | Restricción cruzada entre roles (RBAC) | Todos los perfiles vs. 17 módulos | Cada rol tiene bloqueados con `✕ Restringido por rol` los módulos ajenos a su función. | Ningún rol pudo acceder a pantallas de otro perfil. | **PASS** |
| **CP-10** | Acceso sin sesión activa | `usuario = null` | Cualquier consulta de permiso sobre los 17 módulos devuelve `false`. | Todos los módulos permanecen denegados sin autenticación previa. | **PASS** |