# Plan y Ejecución de Pruebas — Historia SU-5 (`SU-43`)
**Proyecto:** Sistema Integral de Gestión Hospitalaria — Sanatorio UNDAV  
**Entorno probado:** `https://juan-manuel-pizzorno.github.io/SanatorioUndav/` + Suite Node (`testing/contexto.test.mjs`)

## 1. Casos de Prueba Positivos (Matrícula Única y Cambio de Ámbito)

| ID | Caso de Prueba | Datos de Entrada | Resultado Esperado | Resultado Obtenido | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CP-12** | Login médico doble ámbito con matrícula | `medico@undav.edu.ar` / `1234` | Autentica usuario único (`MP-45821`) y despliega selector *Guardia* / *Consultorios Externos*. | Mostró pantalla intermedia con matrícula `MP-45821` y ambas opciones. | **PASS** |
| **CP-13** | Selección de contexto *Guardia Médica* | Clic en tarjeta **Guardia Médica** | Habilita *Atención de Guardia* y *Solicitud de Derivaciones*; bloquea *Agenda de Consultorios*. | Barra superior indica `Ámbito: Guardia` y habilita los 4 módulos de guardia. | **PASS** |
| **CP-14** | Selección de contexto *Consultorios Externos* | Clic en tarjeta **Consultorios Externos** | Habilita *Agenda de Consultorios* y *Solicitud de Estudios*; bloquea *Atención de Guardia*. | Barra superior indica `Ámbito: Consultorios Externos` y adapta los módulos. | **PASS** |
| **CP-15** | Cambio dinámico de ámbito en sesión | Botón **Cambiar ámbito** -> alternar área | Permite alternar entre Guardia y Consultorios sin cerrar sesión, recalculando permisos. | Reemplazó dinámicamente los módulos habilitados y bloqueados. | **PASS** |
| **CP-16** | Login médico de ámbito único | `consultorios.medico@undav.edu.ar` / `1234` | Ingresa directo a *Consultorios Externos* (`MP-51204`) sin pedir selección ni mostrar botón de cambio. | Entró directo al panel de Consultorios Externos. | **PASS** |

## 2. Casos de Prueba Negativos (Validación de Matrícula y Ámbitos Restringidos)

| ID | Caso de Prueba | Datos de Entrada | Resultado Esperado | Resultado Obtenido | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CP-17** | Médico ámbito único intenta forzar otro ámbito | `MP-51204` -> `seleccionarContextoMedico('Guardia')` | Deniega el cambio informando que el ámbito no está habilitado para su matrícula. | Retornó `ok: false` con mensaje de restricción por matrícula. | **PASS** |
| **CP-18** | Selección de ámbito inexistente | `MP-45821` -> `'Quirófano Central'` | Rechaza el contexto inválido y conserva el estado previo sin errores. | Retornó `ok: false` bloqueando el cambio. | **PASS** |
| **CP-19** | Usuario no médico intenta cambiar contexto | Rol `Admisión` -> `seleccionarContextoMedico('Guardia')` | Rechaza la operación por no corresponder a un perfil médico con matrícula. | Retornó `ok: false`: *"No hay un médico autenticado con matrícula válida."* | **PASS** |
| **CP-20** | Cambio de contexto sin sesión activa | `sessionStorage` vacío | Bloquea cualquier intento de asignación de contexto sin autenticación previa. | Retornó `ok: false`. | **PASS** |