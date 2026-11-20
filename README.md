<div align="center">

  # 🏥 Sanatorio UNDAV — Sistema Integral de Gestión Hospitalaria
  **Plataforma Web Centralizada para Guardia, Consultorios Externos, Gestión de Pacientes y Cuerpo Médico**

  [![Demo en Vivo](https://img.shields.io/badge/🚀_Demo_en_Vivo-GitHub_Pages-0ea5e9?style=for-the-badge)](https://juan-manuel-pizzorno.github.io/SanatorioUndav/)
  [![Metodología](https://img.shields.io/badge/Metodología-Scrum_%7C_Jira-0284c7?style=for-the-badge)](https://github.com/Juan-Manuel-Pizzorno/SanatorioUndav)
  [![Estado Sprint 1](https://img.shields.io/badge/Sprint_1-SU--4_%26_SU--5_Completados-10b981?style=for-the-badge)](https://github.com/Juan-Manuel-Pizzorno/SanatorioUndav)
  [![QA Suite](https://img.shields.io/badge/QA_Suite-20%2F20_Passing-22c55e?style=for-the-badge)](./testing/PLAN_DE_PRUEBAS_SU43.md)

  ![Arquitectura Web](https://img.shields.io/badge/Arquitectura-Web_%2B_Contingencia_Offline-0f172a?style=flat-square)
  ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
  ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
  ![JavaScript ES6+](https://img.shields.io/badge/JavaScript_ES6+-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
  ![Node.js](https://img.shields.io/badge/Node.js_Test-339933?style=flat-square&logo=nodedotjs&logoColor=white)

  [🌐 Abrir Aplicación en Vivo](https://juan-manuel-pizzorno.github.io/SanatorioUndav/) · [📋 Plan de Pruebas Login](./testing/PLAN_DE_PRUEBAS_SU39.md) · [📋 Plan de Pruebas Contexto](./testing/PLAN_DE_PRUEBAS_SU43.md) · [🔐 Módulo Auth & RBAC](./back/auth.js)

</div>

---

## 🎯 Propósito y Alcance del Sistema

El **Sistema Integral de Gestión Hospitalaria del Sanatorio UNDAV** es una solución web desarrollada para reemplazar el registro manual e informal en planillas de Excel por una plataforma centralizada, trazable y automatizada. El sistema elimina errores de tipeo, sistematiza la priorización clínica en guardia mediante Triage estándar, valida coberturas médicas y habilita la autogestión de los pacientes.

### 🏗️ Las 4 Áreas Interconectadas
1. **🚑 Guardia Médica:** Admisión administrativa, clasificación Triage de 5 niveles con ordenamiento por gravedad y tiempo acumulado, alertas de reevaluación, atención inmediata en Shock Room (Código Rojo), tablero de control en tiempo real, autorización de derivaciones con firma digital y llamados en monitores públicos.
2. **🩺 Consultorios Externos:** Autogestión de turnos, motor de recomendación inteligente basado en profesionales frecuentes y diagnósticos **CIE-10**, recordatorios automáticos (WhatsApp / e-mail), gestión de sobreturnos en agendas separadas y reasignación automática a suplentes ante ausencias médicas.
3. **🧑‍🤝‍🧑 Portal Web del Paciente:** Autenticación local o social (Gmail / Facebook), reserva y cancelación de turnos, carga de órdenes médicas para estudios y consulta centralizada de historial clínico, recetas electrónicas y resultados en PDF.
4. **⚙️ Administración y Plataforma:** Identidad única para médicos vinculada a su matrícula profesional con selector de contexto (*Guardia* / *Consultorios Externos*), parametrización de obras sociales y reglas CIE-10 por TI, y **esquema de contingencia offline** con autoguardado local y sincronización automática.

> **Exclusiones expresas del alcance:** La validación formal de matrículas y títulos profesionales (responsabilidad de RRHH), la creación de salas físicas separadas para pediatría y la gestión/firma física de declaraciones juradas por retiro voluntario quedan fuera del sistema.

---

## 👥 Perfiles de Usuario y Control de Acceso (RBAC)

El sistema adapta dinámicamente sus vistas y permisos según el rol operativo del usuario:

| Perfil / Rol | Responsabilidades Principales en el Sistema |
| :--- | :--- |
| **Paciente** *(Portal Web)* | Reserva/cancela turnos (`Inicio`, `Mis turnos`, `Recetas electrónicas`, `Gestiones médicas`, `Cartilla médica`), sube órdenes y descarga estudios en PDF. |
| **Admisión de Guardia** | Registra ingresos por DNI/Afiliado, valida cobertura/plan, asienta motivo de consulta y deriva a Triage. |
| **Enfermería / Triage** | Registra parámetros fisiológicos (**TA, FC, FR, Temp, SatO₂**), asigna nivel de Triage y ejecuta reevaluaciones. |
| **Médico de Guardia** | Atiende según prioridad de Triage y espera acumulada, evoluciona historia clínica, solicita estudios, receta y gestiona altas o derivaciones. |
| **Médico de Consultorios** | Atiende agenda programada, consulta resumen clínico, registra evoluciones y emite recetas electrónicas *(usuario único vinculado a matrícula con selector de contexto si actúa en ambas áreas)*. |
| **Jefe de Guardia** | Monitorea ocupación en tiempo real (consultorios, Shock Room, camas de observación), controla alertas de espera y autoriza derivaciones externas con **firma digital**. |
| **Administrativo de Consultorios** | Valida administrativamente las órdenes médicas adjuntadas por los pacientes para habilitar turnos de estudios. |
| **Personal / Área de TI** | Da de alta profesionales, gestiona cuentas y roles, parametriza obras sociales/planes y configura reglas de recomendación **CIE-10**. |

---

## 🚨 Clasificación Triage y Reglas Críticas de Negocio

El módulo de Guardia implementa estrictamente el estándar internacional de **Triage de 5 categorías** con alertas automáticas por exceso de espera:

| Nivel | Categoría | Color | Tiempo Máximo de Espera | Flujo Operativo |
| :---: | :--- | :---: | :---: | :--- |
| **Nivel 1** | **Reanimación / Riesgo de Vida** | 🔴 Rojo | **Inmediato (0 min)** | Derivación directa a **Shock Room** omitiendo admisión/triage inicial (registro administrativo posterior). |
| **Nivel 2** | **Emergencia** | 🟠 Naranja | **15 minutos** | Alerta automática de reevaluación por enfermería al superar el límite. |
| **Nivel 3** | **Urgencia** | 🟡 Amarillo | **60 minutos** | Ordenamiento por gravedad y mayor tiempo de espera acumulado. |
| **Nivel 4** | **Urgencia Menor** | 🟢 Verde | **120 minutos** | Atención general (incluye guardia pediátrica hasta 16 años en consultorios compartidos). |
| **Nivel 5** | **Sin Urgencia** | 🔵 Azul | **240 minutos** | Atención programada de baja complejidad en guardia. |

### 📌 Otras Reglas Operativas Clave
* **Privacidad en Salas de Espera:** Los monitores públicos proyectan únicamente **Nombre del paciente y Consultorio/Box** (nunca el DNI).
* **Tolerancia en Consultorios:** Límite estricto de **10 minutos** de tolerancia para turnos programados.
* **Cancelación Autónoma:** Permitida hasta **1 hora antes** del turno (bloqueada con aviso de error si falta menos tiempo).
* **Recordatorios Automáticos:** Notificaciones **1 o 2 días antes** vía **WhatsApp o correo electrónico** con confirmación/cancelación directa.

---

## 📑 Mapa de Requisitos Funcionales (ERS)

<details>
<summary><b>Ver listado completo de los 21 Requisitos Funcionales (RF-01 a RF-21)</b></summary>

* **`RF-01` Autenticación y Registro de Pacientes:** Alta presencial en recepción o autónoma en portal (local o Gmail/Facebook).
* **`RF-02` Login y Selector de Contexto Profesional:** Autenticación por rol y selector *Guardia / Consultorios* para médicos de doble ámbito.
* **`RF-03` Reserva Autónoma de Turnos:** Selección por profesional o especialidad sin orden médica previa.
* **`RF-04` Recomendación Inteligente:** Sugerencia prioritaria por médicos frecuentes y antecedentes clínicos.
* **`RF-05` Turnos para Estudios Médicos:** Carga obligatoria de orden médica autorizada.
* **`RF-06` Validación Administrativa:** Control de obra social, afiliado y órdenes subidas.
* **`RF-07` Cancelación Autónoma:** Bloqueo ante intentos con menos de 60 minutos de antelación.
* **`RF-08` Recordatorios y Confirmación:** Envío automático vía WhatsApp / e-mail.
* **`RF-09` Gestión de Sobreturnos y Ausencias:** Agenda diferenciada de sobreturnos y reasignación automática a suplentes.
* **`RF-10` Admisión de Guardia:** Ingreso por DNI/Afiliado y derivación a Triage.
* **`RF-11` Parámetros Fisiológicos:** Registro de TA, FC, FR, Temperatura y SatO₂.
* **`RF-12` Clasificación Automática de Triage:** Categorización en 5 niveles y ordenamiento de cola.
* **`RF-13` Código Rojo (Shock Room):** Ingreso inmediato sin demora administrativa.
* **`RF-14` Alertas de Reevaluación:** Notificación visual por exceso de tiempos límite por nivel.
* **`RF-15` Retiros Voluntarios y Ausencias:** Registro de declaración jurada y estado *Ausente* tras llamados reiterados.
* **`RF-16` Evolución Médica e Historia Clínica:** Registro clínico, solicitud de estudios, derivaciones y altas.
* **`RF-17` Recetas Electrónicas:** Emisión y envío automático por correo electrónico al paciente.
* **`RF-18` Tablero de Control y Derivaciones:** Ocupación en tiempo real y autorización con firma digital por Jefe de Guardia.
* **`RF-19` Monitores Públicos:** Visualización en sala de espera sin exposición de DNI.
* **`RF-20` Consulta de Historia Clínica y Estudios:** Acceso del paciente a historial, recetas y descarga de PDF.
* **`RF-21` Parametrización de TI:** Alta de profesionales, usuarios/roles, obras sociales y reglas CIE-10.

</details>

---

## 🔐 Credenciales Nominales de Prueba (`Sprint 1`: `SU-4` y `SU-5`)

Para probar el control de acceso basado en roles y el selector de contexto médico directamente en la aplicación desplegada:

> **Contraseña universal de prueba:** `1234` *(o utilizar los botones de autocompletado rápido en pantalla)*

| Rol Operativo | Profesional de Prueba | Correo Institucional | Matrícula / Ámbito |
| :--- | :--- | :--- | :--- |
| 🟦 **Admisión** | Laura Gómez | `laura.gomez@undav.edu.ar` | Recepción Guardia |
| 🟩 **Triage** | Carlos Méndez | `carlos.mendez@undav.edu.ar` | Box de Triage |
| 🩺 **Médico (Doble Ámbito)** | Dra. Sofía Martínez | `sofia.martinez@undav.edu.ar` | `MP-45821` · *Guardia / Consultorios Externos* |
| 🩺 **Médico (Ámbito Único)** | Dr. Lucas Pereyra | `lucas.pereyra@undav.edu.ar` | `MP-51204` · *Solo Consultorios Externos* |
| 🟨 **Jefe de Guardia** | Dr. Roberto Silva | `roberto.silva@undav.edu.ar` | Supervisión y Derivaciones |
| 🟪 **Administrativo** | Mariana Torres | `mariana.torres@undav.edu.ar` | Consultorios Externos |
| ⚙️ **Área TI** | Juan Pizzorno | `juan.pizzorno@undav.edu.ar` | Administración del Sistema |

---

## 🗂️ Estructura del Repositorio & Ejecución

```text
SanatorioUndav/
├── .github/workflows/
│   └── qa.yml                        # Pipeline CI en GitHub Actions (ejecuta CP-00 a CP-19)
├── index.html                        # Punto de entrada y redirección para GitHub Pages
├── package.json                      # Configuración modular ES6 y script npm test
├── front/
│   └── index.html                    # [SU-36 / SU-41] Login Split-Screen, Selector de Contexto y Panel RBAC
├── back/
│   ├── usuarios.json                 # [SU-37 / SU-40] Padrón nominal con matrículas y permisos por contexto
│   └── auth.js                       # [SU-38 / SU-40 / SU-42] Autenticación, vínculo por matrícula y cambio de ámbito
└── testing/
    ├── 01-login.test.mjs             # [SU-39] Suite automatizada de Login y RBAC (CP-00 a CP-10)
    ├── 02-contexto.test.mjs          # [SU-43] Suite automatizada de Matrícula y Contexto Médico (CP-11 a CP-19)
    ├── PLAN_DE_PRUEBAS_SU39.md       # [SU-39] Matriz QA documentada — Historia SU-4
    └── PLAN_DE_PRUEBAS_SU43.md       # [SU-43] Matriz QA documentada — Historia SU-5