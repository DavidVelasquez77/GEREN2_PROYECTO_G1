# QuetzalMart — Proyecto GEREN2

Repositorio de trabajo para la implementación del proyecto en Odoo Community, UiPath y Google Cloud.

## Estructura

- `datos/`: archivos de carga y datos de prueba separados por proceso.
- `rpa/`: proyecto de UiPath.
- `consultas_sql/`: consultas para la validación en PostgreSQL durante la evaluación.
- `capturas/`: evidencias organizadas para los tres manuales.
- `manual_1/`, `manual_2/`, `manual_3/`: documentos finales.
- `BLOQUE_7_GOOGLE_ANALYTICS.md`: configuración y evidencia del bloque de GA4.
- `BLOQUE_8_RPA.md`: flujo, restricciones y evidencia del robot de UiPath.
- `outputs/`: entregables generados por Codex.
- `tmp/`: archivos temporales de construcción y verificación.

## Reglas importantes del proyecto

- Odoo debe usar una única base de datos PostgreSQL en la nube.
- La carga de clientes y productos con UiPath debe hacerse mediante la interfaz de Odoo; no se utilizará API de Odoo desde UiPath.
- Las hojas de carga deben conservar exactamente los nombres exigidos por el enunciado: `clientes` y `productos`.
- Las evidencias se tomarán durante la implementación y se asociarán al manual correspondiente.

## Guía de lectura y reproducción

El proyecto utiliza Odoo Community 18, PostgreSQL 16 y un robot de UiPath. La infraestructura Docker, los scripts de operación y los datos de demostración acompañan a estos entregables:

- [Manual 1: instalación y operación](manual_1/Manual_1_Instalacion_y_Operacion.md).
- [Manual 2: diagramas de procesos](manual_2/Manual_2_Diagramas_de_Flujo.md).
- [Manual 3: inteligencia de negocios con GA4](manual_3/Manual_3_Inteligencia_de_Negocios_GA4.md).
- [Infraestructura](BLOQUE_2_INFRAESTRUCTURA.md), [Odoo y PostgreSQL](BLOQUE_3_ODOO_POSTGRESQL.md) y [robot UiPath](BLOQUE_8_RPA.md).

Los manuales describen el entorno de la entrega y sus evidencias. Para reproducirlo, comenzar por el Manual 1: requiere Docker Compose, un entorno Linux para los scripts de despliegue y Windows/UiPath Studio para el robot. Los recursos y cuentas de Google Cloud y GA4 deben pertenecer al entorno autorizado para la práctica.

`infra/docker-compose.yml` monta `./config/odoo.conf` y `./addons` relativos a su carpeta. Esas rutas se preparan mediante `infra/deploy_odoo18.sh`, que toma las fuentes desde `/tmp/quetzalmart-deploy` y escribe en `/opt/quetzalmart`. Por ello, ejecutar `docker compose up` directamente desde un clon sin preparar configuración, credenciales y carpetas no reproduce la instalación. Revisar las rutas, dominio y operaciones del script antes de usarlo en una máquina de pruebas.

## Archivos locales y herramientas auxiliares

Las credenciales, archivos `.env`, instalaciones `node_modules/` y estados de herramientas de escritorio quedan fuera de nuevos commits. Las capturas, los manuales, el proyecto UiPath y los archivos de carga siguen siendo entregables versionados.

`spreadsheet_work/` contiene scripts auxiliares de preparación de hojas, con rutas del equipo original y dependencia de `@oai/artifact-tool`, un runtime privado del entorno en el que se generaron. No constituye una aplicación npm instalable desde este repositorio. Las hojas entregadas pueden revisarse sin ese runtime; para regenerarlas hay que disponer de él y adaptar las rutas. La instalación copiada de `node_modules` se retira del índice, sin borrar las copias locales ni reescribir el historial.

El trabajo y los manuales pertenecen al equipo del proyecto. La existencia de evidencia histórica de despliegue no garantiza que una URL de demostración siga activa ni verifica nuevamente operaciones en la nube.
