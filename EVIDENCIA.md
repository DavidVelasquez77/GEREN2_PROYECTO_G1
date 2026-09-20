# Control de evidencias — QuetzalMart

Este archivo registra qué debe demostrarse durante la implementación y la evaluación.

| Bloque | Evidencia | Estado |
|---|---|---|
| 1 | Estructura del proyecto y plantillas de carga | Completado |
| 2 | Proyecto GCP, VM y acceso remoto | Completado |
| 3 | Odoo Community y PostgreSQL en la nube | Completado |
| 4 | Configuración de módulos, almacenes y datos base | Pendiente |
| 5 | Compras, ventas, cotizaciones y facturación | Pendiente |
| 6 | Sitio web, catálogo, carrito, impuestos y pago | Pendiente |
| 7 | Google Analytics 4, segmentos, audiencias y exploraciones | Pendiente |
| 8 | Flujo RPA en UiPath usando la interfaz de importación | Pendiente |
| 9 | Consultas SQL para la evaluación | Pendiente |
| 10 | Capturas y trazabilidad de resultados | Pendiente |
| 11 | Manuales 1, 2 y 3 | Pendiente |
| 12 | Ensayo de evaluación y revisión final | Pendiente |

## Bloque 2 — Infraestructura creada

- Proyecto: `quetzalmart-geren2-2026` — **QuetzalMart GEREN2 2026**.
- API habilitada: Compute Engine.
- VM: `quetzalmart-odoo`.
- Región/zona: `us-central1-a`.
- Sistema operativo: Ubuntu 24.04 LTS.
- Tipo de máquina: `e2-standard-2` — 2 vCPU y aproximadamente 8 GB de RAM.
- Disco raíz: 30 GB `pd-balanced`.
- IP externa estática: `34.9.149.41`.
- Red: VPC `default`, con acceso web preparado en los puertos 80 y 443.
- Verificación: acceso SSH exitoso mediante Google Cloud CLI.

> La IP es un dato de infraestructura, no una contraseña. Las credenciales y claves privadas no se guardarán en este repositorio.

## Bloque 3 — Odoo Community y PostgreSQL

- Odoo Community 18 desplegado mediante la imagen oficial `odoo:18.0`.
- PostgreSQL 16 desplegado en la misma VM mediante `postgres:16-alpine`.
- Base centralizada: `quetzalmart`.
- Empresa y administrador inicial configurados como QuetzalMart.
- Acceso público: `https://quetzalmart.34-9-149-41.sslip.io`.
- Certificado TLS válido de Let's Encrypt con renovación automática.
- HTTP redirige automáticamente a HTTPS.
- PostgreSQL no está expuesto a Internet.
- Los puertos internos 8069 y 8072 de Odoo solo escuchan en `127.0.0.1` y se publican mediante Nginx.
- Credenciales almacenadas localmente en `.secrets/odoo_credentials.txt`, carpeta excluida por `.gitignore`.
- Verificación SQL: base `quetzalmart`, compañía `QuetzalMart`, administrador `admin@quetzalmart.local` y 120 tablas iniciales.

## Entregable del bloque 1

La plantilla de trabajo se encuentra en el archivo generado dentro de `outputs/`. Incluye hojas para inicio, clientes, productos, empleados, cargos y departamentos, ventas, compras y documentos.
