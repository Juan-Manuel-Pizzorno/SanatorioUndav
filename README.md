# 🏥 Sanatorio UNDAV — Sistema de Gestión de Guardia Médica

Aplicación interactiva por consola desarrollada en **Python puro** para gestionar el flujo operativo de la guardia del Sanatorio UNDAV:
- 🔐 **Autenticación y control de permisos por rol (RBAC)**
- 🩺 **Selector dinámico de ámbito médico por matrícula**
- 🚑 **Admisión de pacientes, detección pediátrica y derivación automática a Triage**
- 💓 **Registro y validación de parámetros fisiológicos en Triage vinculados a la admisión**
- 🚦 **Clasificación y gestión de cola de atención de guardia** *(en desarrollo)*

---

## 📁 Estructura del Proyecto

Cada Historia de Usuario (`SU-XX`) vive en su propia carpeta modular con tres responsabilidades bien separadas: lógica pura (`back*.py`), interfaz de consola (`front.py`) y pruebas automatizadas (`Tests_SU-*.py`).

```text
📦 SanatorioUndav/
├── 📂 FuncionesDeValidacion/        # 🛡️ Módulo transversal de validación de entradas
│   └── 📄 Validaciones.py           # Rangos cerrados, texto, DNI numérico, enteros y decimales
│
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
│   └── 🧪 Tests_SU16.py             # 6 pruebas unitarias de admisión, pediatría y derivación
│
├── 📂 SU-17/                        # 💓 Historia SU-17: Registro de parámetros fisiológicos en Triage
│   ├── 📄 backTriage.py             # Validación y vinculación de signos vitales a admisión (SU-50)
│   ├── 📄 front.py                  # Formulario interactivo de signos vitales en Triage (SU-48/49)
│   └── 🧪 Tests_SU-17.py            # 11 pruebas unitarias de signos vitales y vinculación (SU-51)
│
├── 📂 SU-18/                        # 🚦 Historia SU-18: Cola de atención de guardia (En desarrollo)
│   ├── 📄 backColaGuardia.py        # Clasificación automática de urgencia según Triage (SU-52)
│   └── 📄 front.py                  # Interfaz de visualización de cola de guardia
│
├── ⚙️ pytest.ini                    # Configuración global para ejecutar todos los tests juntos
├── 🙈 .gitignore                    # Ignora archivos temporales (__pycache__, .pytest_cache)
└── 📘 README.md                     # Guía visual del proyecto
```

---

## 🚀 Cómo Instalar y Arrancar (Paso a Paso)

### 1️⃣ Clonar o actualizar el repositorio
Abrí una terminal en la carpeta del proyecto y bajá los últimos cambios de `main`:
```bash
git pull origin main
```

### 2️⃣ Instalar `pytest` (única dependencia externa)
```bash
py -m pip install pytest
```

---

## 🖥️ Guía Visual de Uso por Consola

Cada módulo se puede ejecutar de manera independiente desde la raíz del proyecto (`SanatorioUndav/`):

### 🔐 Paso 1: Inicio de Sesión del Personal (`SU-4`)
Valida el correo institucional y la contraseña, y muestra únicamente las herramientas habilitadas para el perfil que ingresó.
```bash
py SU-4/front.py
```

**👥 Usuarios de prueba listos para usar:**

| Perfil Operativo | Nombre | Correo Institucional | Contraseña | Matrícula / Ámbito |
| :--- | :--- | :--- | :--- | :--- |
| 🗂️ Admisión | Laura Gómez | `laura.gomez@undav.edu.ar` | `1234` | Guardia (Mesa de entrada) |
| 🩺 Triage | Carlos Méndez | `carlos.mendez@undav.edu.ar` | `1234` | Clasificación fisiológica |
| 👨‍⚕️ Médico (Doble ámbito) | Dra. Sofía Martínez | `sofia.martinez@undav.edu.ar` | `1234` | `MP-45821` (Guardia + Consultorios) |
| 👨‍⚕️ Médico (Ámbito único) | Dr. Lucas Pereyra | `lucas.pereyra@undav.edu.ar` | `1234` | `MP-51204` (Solo Consultorios) |
| 🚨 Jefe de Guardia | Dr. Roberto Silva | `roberto.silva@undav.edu.ar` | `1234` | Supervisión en tiempo real |
| 📋 Administrativo | Mariana Torres | `mariana.torres@undav.edu.ar` | `1234` | Órdenes y agenda |
| 💻 TI / Sistemas | Juan Pizzorno | `juan.pizzorno@undav.edu.ar` | `1234` | Administración del sistema |

---

### 🩺 Paso 2: Selector de Contexto Médico (`SU-5`)
Si un médico tiene doble habilitación (`MP-45821`), el sistema le pide elegir su ámbito al entrar y le permite cambiar de área sin cerrar sesión, recalculando sus módulos en vivo. Si tiene ámbito único (`MP-51204`), entra directo.
```bash
py SU-5/front.py
```

**💡 Ejemplo de prueba rápida:**
1. Ingresá con `sofia.martinez@undav.edu.ar` / `1234`.
2. Elegí `1` (*Guardia*) ➔ habilita **Atención de Guardia** y **Solicitud de Derivaciones**.
3. En el menú, apretá `1` (*Cambiar de ámbito operativo*) ➔ cambia al instante a **Consultorios Externos** y habilita **Agenda de Consultorios** y **Solicitud de Estudios**.

---

### 🚑 Paso 3: Admisión de Paciente en Guardia (`SU-16`)
Busca si el paciente ya estaba ingresado por DNI/Afiliado, valida sus datos, detecta automáticamente si es **Pediátrico ($\le 16$ años)** y lo envía a la cola de espera de Triage.
```bash
py SU-16/front.py
```

**💡 Ejemplo de prueba rápida (Paciente Pediátrico):**
- **DNI / Afiliado:** `48123456`
- **Nombre y Apellido:** `Mateo Rojas`
- **Edad:** `10` *(al ser $\le 16$, el sistema lo marca automáticamente como **PEDIÁTRICO**)*
- **Obra Social / Plan:** `OSDE` / `210`
- **Motivo de consulta:** `Fiebre alta y dolor de garganta`
- **Resultado:** Queda admitido y derivado automáticamente a la cola de Triage.

---

### 💓 Paso 4: Registro de Parámetros Fisiológicos en Triage (`SU-17` / `SU-50`)
Permite al enfermero ingresar los 6 signos vitales obligatorios, valida rangos numéricos cerrados mediante `FuncionesDeValidacion/Validaciones.py`, comprueba coherencia clínica ($\text{TA Diastólica} < \text{TA Sistólica}$) y vincula la medición directamente al registro de admisión del paciente.
```bash
py SU-17/front.py
```

**💡 Ejemplo de prueba rápida (Signos Vitales):**
- **DNI / Afiliado:** `35111222` *(si no está en memoria, el flujo crea un registro de prueba)*
- **TA Sistólica (máxima):** `120` *(rango válido: `40` – `300`)*
- **TA Diastólica (mínima):** `80` *(rango válido: `20` – `200`, menor a sistólica)*
- **Frecuencia Cardíaca:** `78` *(rango válido: `20` – `250`)*
- **Frecuencia Respiratoria:** `16` *(rango válido: `5` – `80`)*
- **Temperatura (°C):** `36.7` *(rango válido: `30.0` – `45.0`)*
- **Saturación O2 (%):** `98` *(rango válido: `40` – `100`)*
- **Resultado:** Vincula los signos vitales al registro de admisión del paciente y lo retira de la cola de espera de Triage.

---

## 🧪 Pruebas Automatizadas (`pytest`)

El archivo `pytest.ini` de la raíz detecta automáticamente todas las baterías de prueba del equipo. Con un solo comando se ejecutan los **29 tests**:
```bash
py -m pytest -v
```

*(También podés ejecutar una suite puntual, por ejemplo: `py -m pytest SU-17/Tests_SU-17.py -v`)*

---

## 📊 Detalle de los 29 Casos de Prueba Automatizados

### 🔐 `SU-4/Tests_SU-4.py` — Autenticación y Permisos (6 tests)
- ✅ `test_login_exitoso`: Valida ingreso correcto y oculta la contraseña en la sesión.
- ✅ `test_login_normaliza_mayusculas_y_espacios`: Acepta correos con espacios o mayúsculas (`SOFIA.MARTINEZ@...`).
- ✅ `test_negar_login_password_incorrecta`: Bloquea acceso si la clave no coincide.
- ✅ `test_negar_login_usuario_inexistente`: Rechaza correos fuera del padrón institucional.
- ✅ `test_negar_login_campos_vacios`: Impide iniciar sesión con campos en blanco.
- ✅ `test_restriccion_modulos_por_rol`: Verifica que Triage no pueda acceder a pantallas de Guardia o TI.

### 🩺 `SU-5/Tests_SU-5.py` — Matrícula y Ámbitos Médicos (6 tests)
- ✅ `test_medico_doble_ambito_requiere_selector`: Detecta que `MP-45821` debe elegir turno al ingresar.
- ✅ `test_seleccionar_contexto_guardia`: Habilita módulos de Guardia y bloquea Consultorios.
- ✅ `test_seleccionar_contexto_consultorios`: Habilita módulos de Consultorios y bloquea Guardia.
- ✅ `test_medico_ambito_unico_no_requiere_selector`: Verifica ingreso directo de `MP-51204`.
- ✅ `test_negar_contexto_no_habilitado`: Impide que un médico de ámbito único fuerce otro sector.
- ✅ `test_negar_cambio_contexto_usuario_no_medico`: Bloquea el selector para perfiles no médicos.

### 🚑 `SU-16/Tests_SU16.py` — Admisión, Pediatría y Triage (6 tests)
- ✅ `test_admision`: Registra correctamente a un paciente nuevo en la lista de admitidos.
- ✅ `test_negarDobleAdmision`: Evita duplicar a un paciente que ya está admitido en guardia.
- ✅ `test_esPediatrico`: Clasifica como pediátrico hasta 16 años inclusive y como adulto desde los 17.
- ✅ `test_derivadoATriage`: Envía al paciente admitido a la cola de espera de Triage.
- ✅ `test_negarDerivacionTriageUnNoAdmitido`: Bloquea derivar a Triage a alguien sin admisión previa.
- ✅ `test_negarDobleDerivacionTriage`: Impide encolar dos veces al mismo paciente en Triage.

### 💓 `SU-17/Tests_SU-17.py` — Signos Vitales y Vinculación con Admisión (`SU-51`, 11 tests)
- ✅ `test_rango_cerrado_validaciones`: Verifica límites inclusivos y exclusivos en `numero_dentro_rangoCerrado`.
- ✅ `test_validar_signos_vitales_correctos`: Valida una medición clínica completa dentro de rangos normales.
- ✅ `test_validar_valores_limite_minimos_y_maximos`: Comprueba aceptación exacta en los extremos mínimos y máximos permitidos.
- ✅ `test_negar_cada_parametro_fuera_de_rango`: Rechaza individualmente valores por debajo del mínimo o por encima del máximo en los 6 signos vitales.
- ✅ `test_negar_signos_incompletos_o_no_diccionario`: Bloquea diccionarios con parámetros faltantes o tipos de estructura inválidos.
- ✅ `test_negar_tipos_de_dato_invalidos`: Impide ingresar cadenas de texto (`"78"`) o booleanos (`True`) en lugar de valores numéricos.
- ✅ `test_negar_ta_diastolica_mayor_o_igual_sistolica`: Garantiza coherencia clínica ($\text{TA Diastólica} < \text{TA Sistólica}$).
- ✅ `test_registrar_y_vincular_signos_a_admision`: Vincula los parámetros al registro de admisión del paciente (`SU-50`) y lo retira de espera.
- ✅ `test_actualizar_signos_mismo_paciente_sin_duplicar`: Actualiza mediciones posteriores del mismo paciente sin duplicar registros en historial.
- ✅ `test_negar_registro_triage_paciente_no_admitido`: Impide registrar Triage para un DNI que no fue admitido previamente.
- ✅ `test_obtener_signos_paciente_sin_triage_o_inexistente`: Devuelve `None` si el paciente aún no fue evaluado o no existe.

---

### 🖥️ Salida esperada en terminal:
```text
========================= test session starts =========================
collected 29 items

SU-16/Tests_SU16.py::test_admision PASSED                         [  3%]
SU-16/Tests_SU16.py::test_negarDobleAdmision PASSED               [  6%]
SU-16/Tests_SU16.py::test_esPediatrico PASSED                     [ 10%]
SU-16/Tests_SU16.py::test_derivadoATriage PASSED                  [ 13%]
SU-16/Tests_SU16.py::test_negarDerivacionTriageUnNoAdmitido PASSED [ 17%]
SU-16/Tests_SU16.py::test_negarDobleDerivacionTriage PASSED       [ 20%]
SU-17/Tests_SU-17.py::test_rango_cerrado_validaciones PASSED      [ 24%]
SU-17/Tests_SU-17.py::test_validar_signos_vitales_correctos PASSED [ 27%]
SU-17/Tests_SU-17.py::test_validar_valores_limite_minimos_y_maximos PASSED [ 31%]
SU-17/Tests_SU-17.py::test_negar_cada_parametro_fuera_de_rango PASSED [ 34%]
SU-17/Tests_SU-17.py::test_negar_signos_incompletos_o_no_diccionario PASSED [ 37%]
SU-17/Tests_SU-17.py::test_negar_tipos_de_dato_invalidos PASSED   [ 41%]
SU-17/Tests_SU-17.py::test_negar_ta_diastolica_mayor_o_igual_sistolica PASSED [ 44%]
SU-17/Tests_SU-17.py::test_registrar_y_vincular_signos_a_admision PASSED [ 48%]
SU-17/Tests_SU-17.py::test_actualizar_signos_mismo_paciente_sin_duplicar PASSED [ 51%]
SU-17/Tests_SU-17.py::test_negar_registro_triage_paciente_no_admitido PASSED [ 55%]
SU-17/Tests_SU-17.py::test_obtener_signos_paciente_sin_triage_o_inexistente PASSED [ 58%]
SU-4/Tests_SU-4.py::test_login_exitoso PASSED                      [ 62%]
SU-4/Tests_SU-4.py::test_login_normaliza_mayusculas_y_espacios PASSED [ 65%]
SU-4/Tests_SU-4.py::test_negar_login_password_incorrecta PASSED    [ 68%]
SU-4/Tests_SU-4.py::test_negar_login_usuario_inexistente PASSED    [ 72%]
SU-4/Tests_SU-4.py::test_negar_login_campos_vacios PASSED          [ 75%]
SU-4/Tests_SU-4.py::test_restriccion_modulos_por_rol PASSED        [ 79%]
SU-5/Tests_SU-5.py::test_medico_doble_ambito_requiere_selector PASSED [ 82%]
SU-5/Tests_SU-5.py::test_seleccionar_contexto_guardia PASSED       [ 86%]
SU-5/Tests_SU-5.py::test_seleccionar_contexto_consultorios PASSED  [ 89%]
SU-5/Tests_SU-5.py::test_medico_ambito_unico_no_requiere_selector PASSED [ 93%]
SU-5/Tests_SU-5.py::test_negar_contexto_no_habilitado PASSED       [ 96%]
SU-5/Tests_SU-5.py::test_negar_cambio_contexto_usuario_no_medico PASSED [100%]

========================= 29 passed in 0.10s ==========================
```