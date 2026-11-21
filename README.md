# Sanatorio UNDAV — Sistema de Gestión de Guardia Médica

Aplicación de consola desarrollada en **Python 3.12** para la asignatura **Ingeniería del Software (UNDAV)**, orientada a gestionar el flujo operativo inicial de la guardia hospitalaria: autenticación del personal por rol (RBAC), selección dinámica de contexto médico por matrícula y admisión de pacientes con identificación pediátrica y derivación automática a Triage.

---

## Estructura del Proyecto

El repositorio está organizado de forma modular por Historia de Usuario (`SU-XX/`), separando la lógica de negocio (`back*.py`), la interfaz interactiva por consola (`front.py`) y la batería de pruebas unitarias (`Tests_SU-*.py`):

```text
SanatorioUndav/
├── SU-4/                        # Historia SU-4: Inicio de sesión del personal de salud
│   ├── backUsuarios.py          # Padrón nominal, validación de credenciales y permisos RBAC
│   ├── front.py                 # Interfaz de consola para inicio de sesión
│   └── Tests_SU-4.py            # Pruebas unitarias de login y restricción de módulos (6 tests)
├── SU-5/                        # Historia SU-5: Selector de contexto de trabajo médico
│   ├── backContexto.py          # Vinculación por matrícula y cambio de ámbito operativo
│   ├── front.py                 # Selector de contexto y cambio dinámico en sesión
│   └── Tests_SU-5.py            # Pruebas unitarias de matrícula y ámbitos médicos (6 tests)
├── SU-16/                       # Historia SU-16: Admisión de paciente en guardia
│   ├── backPacientes.py         # Búsqueda/alta de pacientes, detección pediátrica y cola Triage
│   ├── FuncionesSU_45.py        # Módulo de compatibilidad de funciones de admisión (SU-45)
│   ├── front.py                 # Formulario interactivo de admisión por consola
│   └── Tests_SU-16.py           # Pruebas unitarias de admisión, pediatría y derivación (6 tests)
├── pytest.ini                   # Configuración global de descubrimiento de tests (Tests_SU-*.py)
├── .gitignore                   # Exclusión de archivos temporales (__pycache__, .pytest_cache)
└── README.md                    # Documentación técnica del proyecto
```

---

## Historias de Usuario Implementadas (Sprint 1 — Flujo Base de Guardia)

### `SU-4` — Inicio de sesión del personal de salud
* **Autenticación y roles (`SU-36`, `SU-37`, `SU-38`):** Valida el ingreso mediante correo institucional y contraseña, normalizando mayúsculas y espacios, y habilitando exclusivamente las pantallas asignadas a cada perfil operativo (*Admisión*, *Triage*, *Médico*, *Jefe de Guardia*, *Administrativo* y *TI*).
* **Credenciales de prueba disponibles:**
  * **Admisión:** `laura.gomez@undav.edu.ar` / `1234`
  * **Triage:** `carlos.mendez@undav.edu.ar` / `1234`
  * **Médico (doble ámbito):** `sofia.martinez@undav.edu.ar` / `1234` (`MP-45821`)
  * **Médico (ámbito único):** `lucas.pereyra@undav.edu.ar` / `1234` (`MP-51204`)
  * **Jefe de Guardia:** `roberto.silva@undav.edu.ar` / `1234`
  * **Administrativo:** `mariana.torres@undav.edu.ar` / `1234`
  * **TI:** `juan.pizzorno@undav.edu.ar` / `1234`

### `SU-5` — Selector de contexto de trabajo médico
* **Matrícula única y contexto operativo (`SU-40`, `SU-41`, `SU-42`):** Permite a profesionales habilitados en más de un área (*Guardia* y *Consultorios Externos*) elegir su ámbito al iniciar sesión o alternar dinámicamente entre ambos sin cerrar sesión, recalculando las herramientas habilitadas. Los médicos con un único ámbito asignado ingresan directamente sin selector.

### `SU-16` — Admisión de paciente en guardia
* **Registro, pediatría y derivación (`SU-45`):** Permite buscar pacientes por DNI/N° de Afiliado para evitar duplicados, registrar sus datos personales, obra social, plan y motivo de consulta, identificar automáticamente la atención pediátrica (<= 16 años) y derivar al paciente admitido a la cola de espera del módulo de Triage.

---

## Requisitos e Instalación

* **Python 3.12** o superior.
* **pytest** para la ejecución de pruebas automatizadas:

```powershell
py -m pip install pytest
```

---

## Ejecución por Consola

Desde la raíz del proyecto (`SanatorioUndav/`), cada módulo interactivo puede ejecutarse de forma independiente:

```powershell
# Ejecutar inicio de sesión del personal (SU-4)
py SU-4/front.py

# Ejecutar acceso y selector de contexto médico (SU-5)
py SU-5/front.py

# Ejecutar formulario de admisión de guardia (SU-16)
py SU-16/front.py
```

---

## Ejecución de Pruebas Automatizadas (`pytest`)

El repositorio incluye un archivo `pytest.ini` en la raíz configurado para detectar y ejecutar automáticamente todas las suites (`Tests_SU-4.py`, `Tests_SU-5.py` y `Tests_SU-16.py`):

```powershell
py -m pytest -v
```

### Cobertura de Pruebas (18 tests)
* **`SU-4/Tests_SU-4.py` (6 tests):** Login exitoso por rol, normalización de correo, rechazo de contraseñas inválidas/usuarios inexistentes/campos vacíos y verificación de permisos por perfil.
* **`SU-5/Tests_SU-5.py` (6 tests):** Detección de médico de doble ámbito, selección de *Guardia* y *Consultorios Externos*, ingreso directo para matrícula de ámbito único y bloqueo de cambios no autorizados.
* **`SU-16/Tests_SU-16.py` (6 tests):** Admisión de paciente, prevención de doble admisión, detección de paciente pediátrico (<= 16 años), derivación a Triage y bloqueo de derivación duplicada o de pacientes no admitidos.