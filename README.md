<div align="center">

  # 🏥 Sanatorio UNDAV — Gestión Clínica & Guardia
  **Sistema Integral de Gestión Hospitalaria · Control de Acceso Basado en Roles (RBAC)**

  [![Demo en Vivo](https://img.shields.io/badge/🚀_Demo_en_Vivo-GitHub_Pages-0ea5e9?style=for-the-badge)](https://juan-manuel-pizzorno.github.io/SanatorioUndav/)
  [![Estado Sprint 1](https://img.shields.io/badge/Sprint_1-SU--4_Completado-10b981?style=for-the-badge)](https://github.com/Juan-Manuel-Pizzorno/SanatorioUndav)
  [![Tests QA](https://img.shields.io/badge/QA_Suite-11%2F11_Passing-22c55e?style=for-the-badge)](./testing/PLAN_DE_PRUEBAS_SU39.md)

  ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
  ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
  ![JavaScript ES6+](https://img.shields.io/badge/JavaScript_ES6+-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
  ![Node.js Test Runner](https://img.shields.io/badge/Node_Test-339933?style=flat-square&logo=nodedotjs&logoColor=white)

  [🌐 Abrir Aplicación Web](https://juan-manuel-pizzorno.github.io/SanatorioUndav/) · [📋 Plan de Pruebas QA](./testing/PLAN_DE_PRUEBAS_SU39.md) · [🔐 Módulo de Autenticación](./back/auth.js)

</div>

---

## 📋 Sobre el Proyecto

Plataforma web desarrollada para la cátedra de **Ingeniería del Software (UNDAV)** bajo metodología ágil **Scrum**. Permite la autenticación institucional del personal de salud y restringe dinámicamente las vistas operativas según el perfil asignado en la Especificación de Requerimientos (ERS).

### ✨ Características principales
* **Interfaz Split-Screen Clínica:** Diseño moderno y responsivo con indicador de estado operativo y visor de contraseña.
* **Control de Acceso por Roles (RBAC):** Habilitación estricta de módulos autorizados y bloqueo visual de pantallas ajenas al rol.
* **Autocompletado Rápido para QA:** Chips interactivos en pantalla para probar los 6 perfiles operativos en un clic.
* **Suite de Pruebas Automatizadas:** Cobertura de 11 casos de prueba (positivos, negativos y matriz de seguridad cruzada).

---

## 🔐 Credenciales de Prueba (Sprint 1 — `SU-4`)

> **Contraseña universal para todos los perfiles de prueba:** `1234`

| Rol Operativo | Profesional de Prueba | Correo Institucional | Módulos Habilitados |
| :--- | :--- | :--- | :--- |
| 🟦 **Admisión** | Laura Gómez | `admision@undav.edu.ar` | `Registro de Guardia`, `Búsqueda por DNI/Afiliado` |
| 🟩 **Triage** | Carlos Méndez | `triage@undav.edu.ar` | `Registro de Parámetros Fisiológicos`, `Clasificación Triage` |
| 🩺 **Médico** | Dra. Sofía Martínez *(MP-45821)* | `medico@undav.edu.ar` | `Atención de Guardia`, `Historia Clínica`, `Recetas Electrónicas` |
| 🟨 **Jefe de Guardia** | Dr. Roberto Silva | `jefe@undav.edu.ar` | `Tablero de Control en Tiempo Real`, `Autorización de Derivaciones` |
| 🟪 **Administrativo** | Mariana Torres | `admin.consultorios@undav.edu.ar` | `Validación de Órdenes Médicas`, `Gestión de Agenda` |
| ⚙️ **Área TI** | Juan Pizzorno | `ti@undav.edu.ar` | `Alta de Profesionales`, `Parametrización Obras Sociales`, `Reglas CIE-10` |

---

## 🗂️ Arquitectura del Repositorio y Trazabilidad Jira

```text
SanatorioUndav/
├── index.html                        # Punto de entrada y redirección para GitHub Pages
├── front/
│   └── index.html                    # [SU-36] Interfaz de inicio de sesión y dashboard RBAC
├── back/
│   ├── usuarios.json                 # [SU-37] Padrón estructurado de los 6 roles operativos
│   └── auth.js                       # [SU-38] Lógica de validación de credenciales y permisos
└── testing/
    ├── login.test.mjs                # [SU-39] Suite automatizada en Node.js (11 test cases)
    └── PLAN_DE_PRUEBAS_SU39.md       # [SU-39] Documentación de pruebas positivas y negativas
