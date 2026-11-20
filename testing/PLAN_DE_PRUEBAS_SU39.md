# Plan y Ejecución de Pruebas — Historia SU-4 (`SU-39`)
**Proyecto:** Sistema Integral de Gestión Hospitalaria — Sanatorio UNDAV  
**Entorno probado:** `https://juan-manuel-pizzorno.github.io/SanatorioUndav/` + Suite Node (`testing/login.test.mjs`)

## 1. Casos de Prueba Positivos (Acceso y Permisos Habilitados)

| ID | Caso de Prueba | Datos de Entrada | Resultado Esperado | Resultado Obtenido | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CP-01** | Padrón completo de roles ERS | Archivo `back/usuarios.json` | Contener los 6 roles operativos: Admisión, Triage, Médico, Jefe de Guardia, Administrativo y TI. | Los 6 perfiles están cargados con sus permisos diferenciados. | **PASS** |
| **CP-02** | Login exitoso por perfil (6 roles) | Correo de cada rol + clave `1234` | Autentica al usuario, oculta la contraseña en sesión y despliega su panel operativo. | Todos los perfiles ingresaron correctamente. | **PASS** |
| **CP-03** | Normalización de correo institucional | `  MEDICO@UNDAV.EDU.AR ` / `1234` | Ignora mayúsculas y espacios, autentica a *Dra. Sofía Martínez* y muestra `MP-45821`. | Ingresó y mostró nombre, rol y matrícula profesional. | **PASS** |
| **CP-04** | Persistencia y cierre de sesión | Login válido + botón *Cerrar sesión* | Mantiene sesión en `sessionStorage` al recargar y la limpia por completo al salir. | Al cerrar sesión vuelve al login limpio y sin permisos residuales. | **PASS** |
| **CP-05** | Habilitación de módulos propios | Perfil `Triage` (`triage@undav.edu.ar`) | Habilita *Registro de Parámetros Fisiológicos* y *Clasificación Triage*. | Ambos módulos figuran con estado `✓ Acceso habilitado`. | **PASS** |

## 2. Casos de Prueba Negativos (Errores de Autenticación y Bloqueo RBAC)

| ID | Caso de Prueba | Datos de Entrada | Resultado Esperado | Resultado Obtenido | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CP-06** | Contraseña incorrecta | `medico@undav.edu.ar` / `9999` | Deniega acceso, no crea sesión y muestra alerta visual de error. | Banner rojo: *"Credenciales inválidas. Verificá tu correo institucional y contraseña."* | **PASS** |
| **CP-07** | Correo institucional inexistente | `intruso@undav.edu.ar` / `1234` | Deniega acceso y muestra mensaje de error sin revelar si el correo existe. | Banner rojo de credenciales inválidas; acceso bloqueado. | **PASS** |
| **CP-08** | Campos vacíos o solo espacios | Correo: `""` o `"   "` / Clave: `""` | Impide el envío / rechaza validación solicitando completar ambos campos. | Validación HTML5 + validación backend bloquean el ingreso. | **PASS** |
| **CP-09** | Intento de inyección en credenciales | `' OR '1'='1` en correo y clave | Rechaza la entrada como texto plano inválido sin comprometer la sesión. | Acceso denegado; `sessionStorage` permanece vacío. | **PASS** |
| **CP-10** | Restricción cruzada entre roles (RBAC) | Todos los perfiles vs. 14 módulos | Cada rol tiene bloqueados con `✕ Restringido por rol` los módulos ajenos a su función. | Ningún rol pudo acceder a pantallas de otro perfil (ej. Triage no accede a TI ni Recetas). | **PASS** |
| **CP-11** | Acceso sin sesión activa | `usuario = null` | Cualquier consulta de permiso sobre los 14 módulos devuelve `false`. | Todos los módulos permanecen denegados sin autenticación previa. | **PASS** |