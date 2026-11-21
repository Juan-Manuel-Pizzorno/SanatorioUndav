# 🏥 Sanatorio UNDAV — Sistema de Gestión de Guardia Médica

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-18%20Tests%20Passing-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Estado](https://img.shields.io/badge/Sprint%201-Completado-2EA44F?style=for-the-badge)
![Universidad](https://img.shields.io/badge/UNDAV-Ingenier%C3%ADa%20del%20Software-8A2BE2?style=for-the-badge)

Aplicación interactiva por consola desarrollada en **Python puro** para gestionar el flujo operativo inicial de la guardia del **Sanatorio UNDAV**:
* 🔐 **Autenticación y control de permisos por rol (RBAC)**
* 🩺 **Selector dinámico de ámbito médico por matrícula**
* 🚑 **Admisión de pacientes, detección pediátrica y derivación automática a Triage**

---

## 📁 Estructura del Proyecto

Cada Historia de Usuario (`SU-XX`) vive en su propia carpeta modular con tres responsabilidades bien separadas: **lógica pura (`back*.py`)**, **interfaz de consola (`front.py`)** y **pruebas automatizadas (`Tests_SU-*.py`)**.

```text
📦 SanatorioUndav/
├── 📂 SU-4/                         # 🔐 Historia SU-4: Inicio de sesión del personal de salud
│   ├── 📄 backUsuarios.py           # Padrón nominal, validación de login y permisos por rol
│   ├── 📄 front.py                  # Pantalla interactiva de inicio de sesión por consola
│   └── 🧪 Tests_SU-4.py             # 6 pruebas unitarias de autenticación y RBAC
│
├── 📂 SU-5/                         # 🩺 Historia SU-5: Selector de contexto de trabajo médico
│   ├── 📄 backContexto.py           # Vinculación por matrícula y cambio dinámico de ámbito
│   ├── 📄 front.py                  # Menú médico con selector y cambio en caliente
│   └── 🧪 Tests_SU-5.py             # 6 pruebas unitarias de matrícula y ámbitos operativos
│
├── 📂 SU-16/                        # 🚑 Historia SU-16: Admisión de paciente en guardia
│   ├── 📄 backPacientes.py          # Búsqueda/alta de pacientes, pediatría y cola de Triage
│   ├── 📄 FuncionesSU_45.py         # Módulo de compatibilidad hacia backPacientes (SU-45)
│   ├── 📄 front.py                  # Formulario interactivo de admisión por consola
│   └── 🧪 Tests_SU-16.py            # 6 pruebas unitarias de admisión, pediatría y derivación
│
├── ⚙️ pytest.ini                    # Configuración global para ejecutar todos los tests juntos
├── 🙈 .gitignore                    # Ignora archivos temporales (__pycache__, .pytest_cache)
└── 📘 README.md                     # Guía visual del proyecto
```

---

## 🚀 Cómo Instalar y Arrancar (Paso a Paso)

### 1️⃣ Clonar o actualizar el repositorio
Abrí una terminal en la carpeta del proyecto y bajá los últimos cambios de `main`:
```powershell
git pull origin main
```

### 2️⃣ Instalar `pytest` (única dependencia externa)
```powershell
py -m pip install pytest
```

---

## 🖥️ Guía Visual de Uso por Consola

Cada módulo se puede ejecutar de manera independiente desde la raíz del proyecto (`SanatorioUndav/`):

### 🔐 Paso 1: Inicio de Sesión del Personal (`SU-4`)
Valida el correo institucional y la contraseña, y muestra **únicamente** las herramientas habilitadas para el perfil que ingresó.

```powershell
py SU-4/front.py
```

#### 👥 Usuarios de prueba listos para usar:

| Perfil Operativo | Nombre | Correo Institucional | Contraseña | Matrícula / Ámbito |
| :--- | :--- | :--- | :---: | :--- |
| 🗂️ **Admisión** | Laura Gómez | `laura.gomez@undav.edu.ar` | `1234` | Guardia (Mesa de entrada) |
| 🩺 **Triage** | Carlos Méndez | `carlos.mendez@undav.edu.ar` | `1234` | Clasificación fisiológica |
| 👨‍⚕️ **Médico (Doble ámbito)** | Dra. Sofía Martínez | `sofia.martinez@undav.edu.ar` | `1234` | `MP-45821` *(Guardia + Consultorios)* |
| 👨‍⚕️ **Médico (Ámbito único)** | Dr. Lucas Pereyra | `lucas.pereyra@undav.edu.ar` | `1234` | `MP-51204` *(Solo Consultorios)* |
| 🚨 **Jefe de Guardia** | Dr. Roberto Silva | `roberto.silva@undav.edu.ar` | `1234` | Supervisión en tiempo real |
| 📋 **Administrativo** | Mariana Torres | `mariana.torres@undav.edu.ar` | `1234` | Órdenes y agenda |
| 💻 **TI / Sistemas** | Juan Pizzorno | `juan.pizzorno@undav.edu.ar` | `1234` | Administración del sistema |

---

### 🩺 Paso 2: Selector de Contexto Médico (`SU-5`)
Si un médico tiene doble habilitación (`MP-45821`), el sistema le pide elegir su ámbito al entrar y le permite **cambiar de área sin cerrar sesión**, recalculando sus módulos en vivo. Si tiene ámbito único (`MP-51204`), entra directo.

```powershell
py SU-5/front.py
```

> **💡 Ejemplo de prueba rápida:**
> 1. Ingresá con `sofia.martinez@undav.edu.ar` / `1234`.
> 2. Elegí **`1`** (*Guardia*) ➔ habilita *Atención de Guardia* y *Solicitud de Derivaciones*.
> 3. En el menú, apretá **`1`** (*Cambiar de ámbito operativo*) ➔ cambia al instante a *Consultorios Externos* y habilita *Agenda de Consultorios* y *Solicitud de Estudios*.

---

### 🚑 Paso 3: Admisión de Paciente en Guardia (`SU-16`)
Busca si el paciente ya estaba ingresado por DNI/Afiliado, valida sus datos, detecta automáticamente si es **Pediátrico ($\le 16$ años)** y lo envía a la cola de espera de **Triage**.

```powershell
py SU-16/front.py
```

> **💡 Ejemplo de prueba rápida (Paciente Pediátrico):**
> * **DNI / Afiliado:** `48123456`
> * **Nombre y Apellido:** `Mateo Rojas`
> * **Edad:** `10` *(al ser $\le 16$, el sistema lo marca automáticamente como `PEDIÁTRICO`)*
> * **Obra Social / Plan:** `OSDE` / `210`
> * **Motivo de consulta:** `Fiebre alta y dolor de garganta`
> * **Resultado:** Queda admitido y derivado automáticamente a la cola de Triage.

---

## 🧪 Pruebas Automatizadas (`pytest`)

El archivo `pytest.ini` de la raíz detecta automáticamente todas las baterías de prueba del equipo. Con un solo comando se ejecutan los **18 tests**:

```powershell
py -m pytest -v
```

### 📊 Detalle de los 18 Casos de Prueba Automatizados

#### 🔐 `SU-4/Tests_SU-4.py` — Autenticación y Permisos (6 tests)
* ✅ `test_login_exitoso`: Valida ingreso correcto y oculta la contraseña en la sesión.
* ✅ `test_login_normaliza_mayusculas_y_espacios`: Acepta correos con espacios o mayúsculas (`SOFIA.MARTINEZ@...`).
* ✅ `test_negar_login_password_incorrecta`: Bloquea acceso si la clave no coincide.
* ✅ `test_negar_login_usuario_inexistente`: Rechaza correos fuera del padrón institucional.
* ✅ `test_negar_login_campos_vacios`: Impide iniciar sesión con campos en blanco.
* ✅ `test_restriccion_modulos_por_rol`: Verifica que *Triage* no pueda acceder a pantallas de *Guardia* o *TI*.

#### 🩺 `SU-5/Tests_SU-5.py` — Matrícula y Ámbitos Médicos (6 tests)
* ✅ `test_medico_doble_ambito_requiere_selector`: Detecta que `MP-45821` debe elegir turno al ingresar.
* ✅ `test_seleccionar_contexto_guardia`: Habilita módulos de Guardia y bloquea Consultorios.
* ✅ `test_seleccionar_contexto_consultorios`: Habilita módulos de Consultorios y bloquea Guardia.
* ✅ `test_medico_ambito_unico_no_requiere_selector`: Verifica ingreso directo de `MP-51204`.
* ✅ `test_negar_contexto_no_habilitado`: Impide que un médico de ámbito único fuerce otro sector.
* ✅ `test_negar_cambio_contexto_usuario_no_medico`: Bloquea el selector para perfiles no médicos.

#### 🚑 `SU-16/Tests_SU-16.py` — Admisión, Pediatría y Triage (6 tests)
* ✅ `test_admision`: Registra correctamente a un paciente nuevo en la lista de admitidos.
* ✅ `test_negarDobleAdmision`: Evita duplicar a un paciente que ya está admitido en guardia.
* ✅ `test_esPediatrico`: Clasifica como pediátrico hasta 16 años inclusive y como adulto desde los 17.
* ✅ `test_derivadoATriage`: Envía al paciente admitido a la cola de espera de Triage.
* ✅ `test_negarDerivacionTriageUnNoAdmitido`: Bloquea derivar a Triage a alguien sin admisión previa.
* ✅ `test_negarDobleDerivacionTriage`: Impide encolar dos veces al mismo paciente en Triage.

### 🖥️ Salida esperada en terminal:
```text
========================= test session starts =========================
collected 18 items

SU-16/Tests_SU-16.py::test_admision PASSED                       [  5%]
SU-16/Tests_SU-16.py::test_negarDobleAdmision PASSED             [ 11%]
SU-16/Tests_SU-16.py::test_esPediatrico PASSED                   [ 16%]
SU-16/Tests_SU-16.py::test_derivadoATriage PASSED                [ 22%]
SU-16/Tests_SU-16.py::test_negarDerivacionTriageUnNoAdmitido PASSED [ 27%]
SU-16/Tests_SU-16.py::test_negarDobleDerivacionTriage PASSED     [ 33%]
SU-4/Tests_SU-4.py::test_login_exitoso PASSED                    [ 38%]
SU-4/Tests_SU-4.py::test_login_normaliza_mayusculas_y_espacios PASSED [ 44%]
SU-4/Tests_SU-4.py::test_negar_login_password_incorrecta PASSED  [ 50%]
SU-4/Tests_SU-4.py::test_negar_login_usuario_inexistente PASSED  [ 55%]
SU-4/Tests_SU-4.py::test_negar_login_campos_vacios PASSED        [ 61%]
SU-4/Tests_SU-4.py::test_restriccion_modulos_por_rol PASSED      [ 66%]
SU-5/Tests_SU-5.py::test_medico_doble_ambito_requiere_selector PASSED [ 72%]
SU-5/Tests_SU-5.py::test_seleccionar_contexto_guardia PASSED     [ 77%]
SU-5/Tests_SU-5.py::test_seleccionar_contexto_consultorios PASSED [ 83%]
SU-5/Tests_SU-5.py::test_medico_ambito_unico_no_requiere_selector PASSED [ 88%]
SU-5/Tests_SU-5.py::test_negar_contexto_no_habilitado PASSED     [ 94%]
SU-5/Tests_SU-5.py::test_negar_cambio_contexto_usuario_no_medico PASSED [100%]

========================= 18 passed in 0.12s ==========================
```