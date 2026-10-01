# QuetzalMart

## Manual 1 — Instalación y operación del sistema

**Proyecto:** GEREN2 · Segundo semestre 2026  
**Versión del manual:** 1.0  
**Fecha:** 30 de septiembre de 2026  
**Plataforma:** Google Cloud Platform · Ubuntu 24.04 · Docker · Odoo Community 18 · PostgreSQL 16 · UiPath

> Este documento describe el entorno y los procedimientos del proyecto académico QuetzalMart. Los clientes, proveedores, empleados, pedidos y documentos de demostración son datos simulados. No se deben copiar contraseñas, llaves ni archivos de `.secrets` a este manual.

### Contenido

1. [Instalación del sistema](#1-instalación-del-sistema)
2. [Funcionamiento de los módulos](#2-funcionamiento-de-los-módulos)
3. [Carga de información y operación en Odoo](#3-carga-de-información-y-operación-en-odoo)
4. [RPA de UiPath: flujo, evidencia y ventajas](#4-rpa-de-uipath-flujo-evidencia-y-ventajas)
5. [Lista de evidencia para la entrega](#5-lista-de-evidencia-para-la-entrega)

---

# 1. Instalación del sistema

## 1.1 Arquitectura utilizada

El sistema se despliega en una máquina virtual de Google Cloud. Odoo y PostgreSQL se ejecutan como contenedores Docker en la misma VM. Nginx recibe el tráfico web y lo dirige a Odoo; el certificado HTTPS se administra con Let's Encrypt. La base de datos permanece en una red privada de Docker y no se publica en Internet.

| Componente | Configuración del proyecto |
|---|---|
| Proyecto de Google Cloud | `quetzalmart-geren2-2026` |
| VM | `quetzalmart-odoo` |
| Zona | `us-central1-a` |
| Sistema operativo | Ubuntu 24.04 LTS |
| Tipo de máquina | `e2-standard-2` (2 vCPU, 8 GB RAM) |
| Disco | 30 GB, `pd-balanced` |
| IP pública estática | `34.9.149.41` |
| Aplicación | Imagen oficial `odoo:18.0` |
| Base de datos | Imagen `postgres:16-alpine`; base `quetzalmart` |
| Proxy y HTTPS | Nginx y Let's Encrypt |
| Dirección web | [https://quetzalmart.34-9-149-41.sslip.io](https://quetzalmart.34-9-149-41.sslip.io) |

## 1.2 Requisitos previos

- Cuenta de Google Cloud con permiso para administrar el proyecto y la VM.
- Google Cloud CLI instalado en el equipo que administra la instancia.
- Acceso SSH a la VM autorizado por el proyecto.
- Este repositorio disponible localmente en el equipo administrador.
- UiPath Studio instalado en el equipo que ejecutará el robot.
- Google Chrome y la extensión de UiPath habilitada para la automatización del RPA. El flujo fue preparado para Chrome; no se deben recapturar selectores en otro navegador sin probarlos.
- Acceso a Internet para descargar imágenes de contenedor, módulos y el certificado HTTPS durante una instalación nueva.

## 1.3 Crear la VM y preparar la red

En Google Cloud Console:

1. Seleccionar el proyecto `quetzalmart-geren2-2026` y habilitar Compute Engine.
2. Crear una instancia en `us-central1-a`, con Ubuntu 24.04 LTS, `e2-standard-2` y disco de 30 GB `pd-balanced`.
3. Reservar una IP externa estática y asignarla a la VM. Para este proyecto se usa `34.9.149.41`.
4. Permitir tráfico entrante TCP por los puertos **80 y 443** para el sitio. Restringir SSH a operadores autorizados.
5. **No abrir el puerto 5432 a Internet.** PostgreSQL se mantiene dentro de la red privada de Docker. Para una comprobación administrativa puntual, usar un túnel SSH autorizado.
6. Confirmar que la IP responde y que el nombre `quetzalmart.34-9-149-41.sslip.io` resuelve a la IP reservada. El script del proyecto solicita el certificado HTTPS para ese nombre.

## 1.4 Instalar Docker, PostgreSQL, Odoo y HTTPS

Los archivos de despliegue están en `infra/`. El procedimiento siguiente describe una instalación nueva; **no volver a ejecutar el instalador en la VM que contiene la base operativa sin preparar y verificar antes un respaldo**.

Desde PowerShell, en la raíz del repositorio:

```powershell
gcloud config set project quetzalmart-geren2-2026
gcloud compute ssh quetzalmart-odoo --project=quetzalmart-geren2-2026 --zone=us-central1-a
```

Copiar los archivos de infraestructura al área temporal del servidor y ejecutar el instalador:

```powershell
gcloud compute ssh quetzalmart-odoo --project=quetzalmart-geren2-2026 --zone=us-central1-a --command="sudo mkdir -p /tmp/quetzalmart-deploy"
gcloud compute scp .\infra\docker-compose.yml .\infra\odoo.conf .\infra\nginx-quetzalmart.conf .\infra\deploy_odoo18.sh quetzalmart-odoo:/tmp/quetzalmart-deploy/ --project=quetzalmart-geren2-2026 --zone=us-central1-a
gcloud compute ssh quetzalmart-odoo --project=quetzalmart-geren2-2026 --zone=us-central1-a --command="sudo bash /tmp/quetzalmart-deploy/deploy_odoo18.sh"
```

El instalador del proyecto:

1. Instala Docker, Docker Compose, Nginx, Certbot y utilidades requeridas.
2. Copia la configuración a `/opt/quetzalmart` y configura Nginx.
3. Genera secretos aleatorios para PostgreSQL, Odoo y el administrador; los restringe a permisos de sistema.
4. Inicia PostgreSQL y espera a que esté listo.
5. En una base nueva, inicializa Odoo y la base `quetzalmart`.
6. Inicia Odoo y configura el certificado HTTPS.
7. Verifica que la página de inicio de sesión responda por HTTPS.

Los secretos generados no deben pegarse en el chat, capturas ni manual. En el servidor se almacenan fuera del repositorio, con permisos restringidos. El listado público de bases de datos de Odoo se desactiva y el filtro limita el servicio a la base `quetzalmart`.

## 1.5 Instalar las aplicaciones y los datos base

El archivo `infra/install_block4_modules.sh` instala los módulos funcionales y el complemento OCA DMS. `infra/run_block4_seed.sh` carga la configuración y los datos maestros. Para una instalación nueva, se copian esos archivos a `/tmp/quetzalmart-block4/` en la VM y se ejecutan en este orden:

1. `install_block4_modules.sh`
2. `run_block4_seed.sh`

El bloque instala Ventas, Compras, Inventario, Contabilidad, Empleados, Contratos, CRM, Comercio electrónico, Marketing por correo, localización de Guatemala, OCA DMS y el proveedor de pago de demostración.

Después, los datos comerciales se preparan mediante los scripts incluidos en `infra/`:

- `seed_block5.py` y `run_block5_seed.sh`: cotizaciones, órdenes, recepciones y facturas de venta y compra.
- `seed_block6.py` y `run_block6_seed.sh`: tienda, productos, envío, imágenes y flujo de pago.
- `seed_block7_ga4.py`: integración GA4 y eventos de comercio electrónico.

Estos scripts son parte de la implementación del proyecto. Deben ejecutarse con la base correcta y siguiendo las instrucciones de cada script; no se deben lanzar directamente sobre otra base ni durante una evaluación en curso. El robot UiPath, por separado, carga clientes y productos mediante la interfaz web de Odoo.

Para completar el archivo documental y el archivado automático de facturas:

1. Instalar OCA DMS y crear en Odoo la carpeta raíz **Documentos QuetzalMart** y sus subcarpetas/categorías.
2. Copiar el complemento `infra/odoo_addons/quetzalmart_invoice_dms/` al directorio adicional de Odoo, que se monta como `/mnt/extra-addons` dentro del contenedor.
3. Ejecutar `infra/install_invoice_dms_module.sh` para instalar o actualizar `quetzalmart_invoice_dms` en la base `quetzalmart`.
4. Importar los 50 PDFs históricos a **Documentos QuetzalMart → Facturas PDF** con `infra/archive_existing_invoices_to_dms.py`.
5. Publicar una factura de prueba y verificar que el PDF aparezca en esa carpeta. El módulo genera y archiva el PDF después de publicar una factura de cliente o proveedor.

Los 5 PDF de facturas de proveedores, 5 acuerdos simulados de outsourcing y 5 acuerdos simulados de empleados se clasifican también en DMS. Los acuerdos de empleados y proveedores son documentos académicos no firmados y no crean obligaciones legales.

## 1.6 Verificar el despliegue

1. Abrir la dirección HTTPS indicada en la tabla y confirmar que Odoo muestra la pantalla de inicio de sesión.
2. Iniciar sesión con la cuenta administrativa entregada al equipo por el medio seguro correspondiente. El manual no almacena la contraseña.
3. Abrir el menú de aplicaciones y comprobar que los módulos instalados estén disponibles.
4. Confirmar la presencia de las compañías, sucursales/almacenes, productos y contactos del proyecto.
5. Comprobar que el certificado del navegador sea válido y que HTTP redirija a HTTPS.
6. Comprobar que no exista una regla pública de firewall para PostgreSQL (5432).

**Archivos de instalación relacionados:** `infra/deploy_odoo18.sh`, `infra/docker-compose.yml`, `infra/odoo.conf`, `infra/nginx-quetzalmart.conf`, `infra/install_block4_modules.sh`, `infra/run_block4_seed.sh`.

---

# 2. Funcionamiento de los módulos

| Módulo | Para qué se usa en QuetzalMart | Datos y relación con otros módulos |
|---|---|---|
| **Ventas** | Crear cotizaciones, confirmar pedidos y generar facturas de cliente. | 20 cotizaciones y 150 pedidos confirmados; las ventas se relacionan con clientes, productos, inventario y contabilidad. |
| **Compras** | Solicitar precios, confirmar órdenes y controlar recepción de mercadería. | 20 cotizaciones de compra y 100 órdenes confirmadas y recibidas; cada compra se relaciona con una factura de proveedor. |
| **Inventario** | Administrar productos, existencias, ubicaciones y ajustes físicos. | 60 productos y tres almacenes: Guatemala, México y El Salvador. Los ajustes contados se aplican con motivo y confirmación. |
| **Facturación/Contabilidad** | Publicar y consultar facturas de clientes y proveedores, impuestos y saldos. | 150 facturas de cliente y 100 de proveedor. Hay 50 PDF de facturas de cliente en `outputs/facturas_pdf/`. |
| **Contactos y CRM** | Mantener datos de clientes/proveedores y registrar oportunidades comerciales, etapas y actividades. | 30 clientes y 25 proveedores de prueba. Las órdenes del portal se asocian al ERP y se sincronizan con el trabajo comercial del CRM. |
| **Empleados y Contratos** | Administrar fichas de personal, puestos, departamentos y contratos internos. | 35 empleados, 6 puestos, 5 departamentos y 35 contratos simulados. |
| **Sitio web y eCommerce** | Publicar el catálogo, permitir carrito, calcular envío/impuestos y recibir pedidos web. | Catálogo de 60 productos en GTQ; pago Demo, únicamente para pruebas. |
| **Marketing por correo** | Crear y enviar campañas diferenciadas de las comunicaciones transaccionales. | El sistema puede generar correos de pedido/factura y campaña. La captura de Mailpit prueba recepción local, no entrega a una cuenta externa. |
| **OCA DMS (Documentos)** | Centralizar y clasificar archivos por carpetas/categorías y etiquetas. | Complemento comunitario integrado a Odoo; incluye carpetas para facturas de proveedores, contratos de outsourcing y contratos de empleados. Los contratos simulados no están firmados ni tienen validez legal. |
| **Google Analytics 4** | Medir navegación y embudo de compra en la tienda. | Eventos `view_item`, `add_to_cart`, `begin_checkout` y `purchase`; segmentos, exploraciones y audiencias se documentan en el Manual 3. Los informes estándar pueden tardar en procesarse. |
| **Pago Demo** | Ensayar el checkout sin cobrar dinero. | Es un método de prueba, no una pasarela de pago real ni una captura de fondos. |

---

# 3. Carga de información y operación en Odoo

## 3.1 Dos mecanismos de carga

El proyecto utiliza dos mecanismos distintos, según el tipo de dato:

1. **Carga inicial reproducible:** los datos maestros y las transacciones del escenario académico se generan con los scripts de `infra/`. Esto evita crear manualmente cientos de registros y permite comprobar los conteos con consultas SQL.
2. **RPA evaluable:** UiPath lee los archivos Excel del auxiliar y realiza las importaciones de clientes y productos mediante la interfaz web de Odoo. No usa API de Odoo ni escribe directamente en PostgreSQL.

Los libros del auxiliar que se probaron están en `datos/prueba_rpa/lote_auxiliar/`. El robot detecta las hojas con nombre exacto `clientes` y `productos`; se deben respetar también los encabezados del archivo, no renombrar las hojas y revisar los campos relacionales contra los valores existentes en Odoo.

## 3.2 Importar clientes o productos desde Odoo

Estos pasos son útiles para revisar una importación o hacerla manualmente:

1. Iniciar sesión en Odoo y abrir **Contactos** para clientes o **Productos** para artículos.
2. Cambiar a vista de lista si Odoo abre las tarjetas.
3. Abrir **Acciones** y seleccionar **Importar registros**.
4. Elegir **Subir archivo de datos** y seleccionar el Excel correspondiente.
5. Verificar que la hoja detectada sea exactamente `clientes` o `productos` y que la primera fila tenga los encabezados.
6. Revisar el mapeo de cada columna. Las relaciones —por ejemplo, país, categoría o etiqueta— deben coincidir con un registro existente cuando el campo lo requiera.
7. Pulsar **Probar**. Resolver todos los errores que Odoo marque antes de continuar.
8. Pulsar **Importar** y esperar el resultado. Después buscar algunos registros recién cargados y confirmar nombre, referencia y datos clave.

> Un campo vacío no siempre produce error: depende de si es obligatorio en Odoo. No se debe inventar información para llenar columnas opcionales. En cambio, el nombre del producto y los datos requeridos del cliente deben venir completos. Una cantidad física sólo aplica a un producto almacenable/seguido por inventario; no se debe asignar cantidad a un servicio.

![Interfaz auténtica de importación de productos en Odoo](../capturas/manual_1/11_importacion_productos_odoo.png)

*Figura 1. Pantalla de Odoo para subir el archivo de productos. La imagen muestra la interfaz de importación, no un resultado exitoso por sí sola; el resultado se confirma después de probar, importar y buscar el registro.*

## 3.3 Clientes y uso del CRM

Para crear o revisar un cliente:

1. Abrir **Contactos** y pulsar **Nuevo**.
2. Seleccionar si el registro es una persona o una empresa.
3. Completar nombre, correo, teléfono, país/dirección e identificación fiscal cuando corresponda.
4. Definir las etiquetas de clasificación disponibles y guardar.
5. Abrir **CRM** para revisar oportunidades, etapa, responsable y actividades asociadas. Un contacto y una oportunidad son registros relacionados, pero no son lo mismo.
6. Para validar un cliente importado, buscarlo en Contactos por nombre o correo y abrir su ficha.

![Ficha real de un contacto de prueba en Odoo](../capturas/manual_1/03_contacto_cliente_crm.png)

*Figura 2. Ficha de un contacto de demostración con datos de dirección, correo y teléfono. El nombre “RPA Cliente Prueba Completa 2026” identifica datos de prueba, no una persona o compañía real.*

![Vista real del directorio de contactos en Odoo](../capturas/manual_1/14_directorio_contactos_odoo.png)

*Figura 3. Directorio de contactos de Odoo. En esta vista pueden coexistir clientes y proveedores; se deben usar los filtros de tipo de contacto para separar ambos grupos.*

## 3.4 Productos e inventario

Los 60 artículos del catálogo inicial utilizan referencias `QM-001` a `QM-060`. Para revisar un producto, abrir **Inventario → Productos** o **Ventas → Productos**, buscar por referencia y confirmar tipo de producto, unidad, precio, costo, categoría y seguimiento de existencias.

![Ficha de producto de demostración en Odoo](../capturas/manual_1/08_producto_demostracion.png)

*Figura 4. Ficha de un producto de demostración usado para probar la configuración de precio, costo y seguimiento de inventario. No debe confundirse con el conjunto maestro `QM-001` a `QM-060`.*

En la carga de inventario físico:

1. Abrir **Inventario → Operaciones → Ajustes de inventario**.
2. Importar/actualizar las cantidades contadas en las líneas que correspondan a productos almacenables.
3. Usar **Probar** antes de importar y corregir los errores de producto o tipo.
4. En la lista, revisar las cantidades contadas y la diferencia.
5. Si se usa **Aplicar todo**, Odoo abre el diálogo de motivo. Escribir el motivo reemplazando el texto predeterminado; no concatenarlo con `Quantity Updated`.
6. Pulsar **Actualizar cantidades** para confirmar el ajuste. Revisar después las existencias del producto/almacén.

![Lista real de ajustes de inventario](../capturas/manual_1/04_ajustes_inventario.png)

*Figura 5. Lista de ajustes de inventario y acción de aplicación.*

![Diálogo de motivo para aplicar ajustes](../capturas/manual_1/15_motivo_ajuste_inventario.png)

*Figura 6. Diálogo de Odoo que solicita el motivo del ajuste y la confirmación **Actualizar cantidades**.*

## 3.5 Órdenes de compra y recepción

Cada compra que cuenta para el requisito debe estar confirmada; una solicitud de cotización todavía no es una compra realizada.

1. Abrir **Compras → Órdenes** y localizar una solicitud o crear una nueva.
2. Seleccionar el proveedor y agregar productos, cantidades y precios.
3. Guardar y pulsar **Confirmar** para convertirla en orden de compra.
4. Abrir la recepción vinculada, revisar cantidades recibidas y pulsar **Validar**.
5. Desde la orden, pulsar **Crear factura**. Verificar proveedor, referencia y líneas.
6. Publicar la factura de proveedor. El estado publicado es el que demuestra que existe la factura contable asociada.

![Listado auténtico de solicitudes y órdenes de compra](../capturas/manual_1/05_ordenes_compra_listado.png)

*Figura 7. Vista de compras. La lista muestra 120 registros en esa captura; los indicadores superiores separan cotizaciones, órdenes y métricas de la vista.*

![Orden de compra P00120 con recepción y factura vinculadas](../capturas/manual_1/06_orden_compra_detalle.png)

*Figura 8. Orden `P00120`, asociada a un proveedor, con acceso a factura de proveedor y recepción.*

![Factura de proveedor vinculada a la orden P00120](../capturas/manual_1/07_factura_proveedor_odoo.png)

*Figura 9. Factura de proveedor `BILL/2026/08/0064`, asociada a la referencia de compra `B5-PO-100`. Para comprobarla, confirmar que el estado sea publicado/registrado.*

## 3.6 Ventas, cotizaciones y facturas de cliente

Para registrar una venta desde la interfaz:

1. Abrir **Ventas → Órdenes → Cotizaciones** y pulsar **Nuevo**.
2. Seleccionar un cliente, fecha y productos; revisar cantidad, precio e impuestos.
3. Guardar la cotización. Si el cliente acepta, pulsar **Confirmar** para obtener una orden de venta.
4. Desde la orden confirmada, elegir **Crear factura**, usar la modalidad normal y revisar las líneas.
5. Publicar la factura y, cuando se requiera evidencia documental, descargar/imprimir el PDF.

En los datos del proyecto hay **20 cotizaciones de venta** y **150 ventas confirmadas**. Las compras tienen su propio bloque de 20 cotizaciones de proveedor, separadas de las cotizaciones de venta.

![Listado de órdenes de venta de Odoo con el contador de registros](../capturas/manual_1/01_ventas_ordenes_162.png)

*Figura 10. Lista de órdenes de venta en Odoo. Se observan 162 registros en total, pedidos recientes y su estado de facturación. Para mostrar el detalle del proceso, todavía conviene añadir una captura de una orden de venta abierta y confirmada.*

## 3.7 Empleados y contratos

Para registrar a una persona del equipo:

1. Abrir **Empleados → Empleados** y pulsar **Nuevo**.
2. Completar nombre y datos de trabajo; asignar el puesto y departamento correctos.
3. Guardar y abrir la sección de contratos del empleado.
4. Crear el contrato de demostración con fechas, puesto y condiciones académicas; guardar.
5. Volver a la lista y usar filtros/agrupación para verificar empleados por departamento y puesto.

Los datos del proyecto contemplan 35 empleados activos, seis puestos, cinco departamentos y 35 contratos simulados. Los archivos de contratos del paquete documental son **borradores simulados sin firma**; no deben presentarse como contratos legales vigentes.

**Evidencia visual por añadir antes de exportar el manual:** captura de la lista de empleados con su total y de la configuración de puestos/departamentos. No hay una captura real de esas vistas en el conjunto de imágenes disponible.

## 3.8 Facturas y archivos PDF

- Facturas de cliente: abrir **Contabilidad → Clientes → Facturas** (enlace administrativo `/odoo/accounting/1/invoicing`).
- Facturas de proveedor: abrir **Contabilidad → Proveedores → Facturas** (enlace `/odoo/accounting/2/bills`).
- Para emitir un PDF manualmente: abrir una factura publicada, elegir **Imprimir** y seleccionar el reporte de factura.
- La carpeta local con los 50 PDF generados para la entrega es `outputs/facturas_pdf/`. El repositorio conserva un archivo por factura; por ejemplo, [`factura_quetzalmart_001.pdf`](../outputs/facturas_pdf/factura_quetzalmart_001.pdf).
- El complemento propio `quetzalmart_invoice_dms` archiva automáticamente en Odoo DMS el PDF oficial de una factura de cliente o proveedor después de publicarla. El destino es **Documentos QuetzalMart → Facturas PDF**; el archivo queda categorizado y etiquetado por tipo y año.
- Los 50 PDF existentes se incorporan al mismo archivo documental con `infra/archive_existing_invoices_to_dms.py`. La carpeta `outputs/facturas_pdf/` conserva además la copia del proyecto para entregar; no es la carpeta interna de Odoo.
- Para verificar una factura nueva: publicarla, abrir **Documentos**, entrar a **Facturas PDF** y buscar el nombre de la factura. La prueba automatizada está descrita en `infra/test_invoice_dms_auto_archive.py`; el módulo y su instalador están en `infra/odoo_addons/quetzalmart_invoice_dms/` e `infra/install_invoice_dms_module.sh`.

## 3.9 Correos y documentos

Las plantillas transaccionales y la campaña se consultan desde las aplicaciones de Ventas/Facturación y Marketing por correo. En el entorno de demostración, Mailpit sirve como buzón local de pruebas. La evidencia de Mailpit demuestra que Odoo generó y entregó el correo al capturador local; **no demuestra entrega a Gmail ni a un servidor SMTP externo**.

![Bandeja real de Mailpit con mensajes de prueba de QuetzalMart](../capturas/manual_1/13_correo_mailpit.png)

*Figura 11. Bandeja de Mailpit con mensajes de prueba. Es evidencia interna de generación/captura, no de recepción externa.*

Para documentos, abrir la aplicación OCA DMS y clasificar cada archivo en su carpeta/categoría, usando etiquetas para facilitar la búsqueda. La existencia de PDFs no convierte un contrato en firmado: los contratos del proyecto deben identificarse como simulados y no firmados.

---

# 4. RPA de UiPath: flujo, evidencia y ventajas

## 4.1 Objetivo y límites

El robot automatiza la lectura de hojas Excel del auxiliar y ejecuta las importaciones a través de las pantallas de Odoo. El flujo principal está en `rpa/QuetzalMart_RPA/Main.xaml`; dependencias y versión se describen en `rpa/QuetzalMart_RPA/project.json`.

El RPA **no usa una API de Odoo**, no ejecuta SQL y no escribe directamente en PostgreSQL. La carga de inventario también usa la interfaz de Odoo. Esta decisión respeta la indicación del auxiliar para la evaluación.

## 4.2 Preparación y ejecución

1. Abrir el proyecto `rpa/QuetzalMart_RPA` en UiPath Studio.
2. Confirmar que estén disponibles `UiPath.Excel.Activities 3.6.1`, `UiPath.System.Activities 25.10.3` y `UiPath.UIAutomation.Activities 26.10.4`.
3. Abrir Chrome, iniciar sesión en Odoo y dejar habilitada la extensión UiPath.
4. Ejecutar `Main.xaml`.
5. Cuando el robot solicite la carpeta raíz, seleccionar `datos\prueba_rpa\lote_auxiliar` para la prueba preparada. En la evaluación se selecciona la carpeta entregada por el auxiliar.
6. El flujo recorre subcarpetas, identifica libros Excel y procesa las hojas que tengan exactamente los nombres `clientes` y `productos`.
7. El robot elimina filas vacías, valida datos obligatorios, prepara un Excel temporal con la hoja que se va a importar y abre la pantalla de importación de Odoo.
8. En cada importación revisa el resultado de **Probar** antes de confirmar **Importar**.
9. Para las cantidades físicas, el flujo prepara la columna de conteo y navega a **Ajustes de inventario**. Después de importar, aplica el ajuste, reemplaza el motivo predeterminado por el motivo configurado y pulsa **Actualizar cantidades**.
10. Al terminar, revisar el panel **Salida** de UiPath y verificar en Odoo que los registros quedaron guardados. El aviso final del robot, por sí solo, no reemplaza esta comprobación.

![UiPath solicita seleccionar la carpeta raíz de los Excel](../capturas/manual_1/09_rpa_solicitud_carpeta.png)

*Figura 12. Diálogo de UiPath para seleccionar la carpeta que contiene los archivos del auxiliar.*

![Secuencia del flujo UiPath para navegar a Contactos e importar](../capturas/manual_1/10_rpa_flujo_importacion.png)

*Figura 13. Captura real del diseñador UiPath con la secuencia de apertura de Contactos y su flujo de importación.*

![Pantalla de Odoo usada por el RPA para importar productos](../capturas/manual_1/11_importacion_productos_odoo.png)

*Figura 14. El RPA ejecuta la importación en la interfaz web; la captura no proviene de una llamada API.*

![El flujo termina y solicita validar los registros en Odoo](../capturas/manual_1/12_rpa_fin_flujo.png)

*Figura 15. Mensaje final del flujo: indica expresamente que aún se deben validar los registros en Odoo. Para la demostración, mostrar también el resultado importado y el log de UiPath.*

## 4.3 Validaciones importantes

- Procesar únicamente hojas con nombres exactos `clientes` y `productos`; las variaciones de mayúsculas, espacios o tildes no son equivalentes.
- No importar nombres obligatorios vacíos.
- Dejar vacías las columnas opcionales sin dato en vez de insertar texto ficticio.
- No asignar “cantidad a la mano” a productos tipo servicio; el control de existencias corresponde a productos almacenables.
- Las columnas de relaciones, por ejemplo compañía o etiquetas, deben coincidir con valores reconocidos por Odoo. Si una referencia no existe, resolverla antes de importar.
- Si **Probar** devuelve un error, no confirmar la importación: corregir el Excel o su mapeo y probar de nuevo.
- Al trabajar con inventario, escribir el motivo sustituyendo el texto por defecto y confirmar con **Actualizar cantidades**. No basta con llegar a la pantalla ni pulsar **Aplicar todo** si aparece el diálogo de motivo.
- El flujo está ligado a selectores de Chrome; mantener Chrome como navegador de ejecución y no cambiarlo a Brave durante la presentación.

## 4.4 Ventajas de implementar el RPA

- Reduce la repetición manual de abrir libros, localizar hojas y cargar archivos.
- Procesa varias carpetas y libros en un mismo recorrido.
- Estandariza la carga por medio del importador oficial de Odoo.
- Reduce errores por filas vacías, valores requeridos ausentes y tipos de producto incompatibles con inventario.
- Deja registros de avance en la salida de UiPath y permite validar los datos en el ERP.
- No expone credenciales de base de datos ni requiere acceso directo a PostgreSQL.
- Hace que el proceso sea demostrable: archivo de entrada → lectura y validación → importación web → verificación en Odoo.

## 4.5 Resultado de la prueba del proyecto

El equipo reportó la ejecución final del RPA con la carpeta exacta `datos\prueba_rpa\lote_auxiliar` y comprobó en Odoo los registros de prueba de clientes `PRUEBA SS 1`, `PRUEBA SS 2`, `PRUEBA SS 3` y `PRUEBA SS 4`. Para presentar esta prueba, conviene abrir la carpeta, mostrar el log de salida de UiPath y buscar esos nombres en Odoo. Las capturas actuales de este manual ilustran el flujo y las pantallas; no sustituyen una captura de la corrida final con el resultado visible.

---

# 5. Lista de evidencia para la entrega

Las capturas incluidas son imágenes reales de las pantallas del proyecto, no ilustraciones generadas. Antes de convertir este Markdown a PDF, completar las evidencias marcadas como faltantes y comprobar que las imágenes se vean con suficiente resolución.

| Requisito del manual | Evidencia incluida o acción final |
|---|---|
| Instalación del sistema | Procedimiento reproducible y arquitectura descritos; adjuntar captura reciente de VM saludable y del login HTTPS si el docente pide evidencia visual de instalación. |
| Tienda/productos | Captura real del catálogo de productos. |
| Carga masiva de clientes/productos | Pantalla de importación y flujo RPA incluidos; completar con una captura del resultado de **Probar/Importar** sin errores y los registros ya visibles. |
| Órdenes de compra | Capturas reales de listado, orden confirmada y factura de proveedor. |
| Ventas | Captura real de la lista con 162 órdenes incluida. Añadir una vista de detalle de una orden confirmada para mostrar sus productos y acciones. |
| CRM/clientes | Capturas reales de directorio y ficha de un contacto de demostración. |
| Empleados | **Pendiente:** lista de empleados y vista con puestos/departamentos. |
| Facturas | Captura real de una factura de proveedor; 50 PDFs de cliente disponibles en `outputs/facturas_pdf/`. Para la evidencia de Odoo, agregar captura de una factura de cliente publicada y de la lista de facturas. |
| Archivo documental de facturas | La implementación automática está descrita y cuenta con módulo de Odoo; agregar captura reciente de **Documentos → Facturas PDF** con el total y un archivo nuevo posterior a su publicación. |
| RPA | Capturas reales de selección de carpeta, flujo y pantalla del importador. Añadir salida final del robot y registro importado si se va a mostrar la ejecución completa. |
| Ajuste de inventario | Captura real de la lista y del diálogo con motivo y **Actualizar cantidades**. |

## Capturas adicionales recomendadas

1. Google Cloud Console: VM `quetzalmart-odoo` en ejecución y configuración sin el puerto 5432 público.
2. Odoo: detalle de una orden de venta confirmada con sus líneas de productos.
3. Odoo: empleados, departamentos y puestos con sus cantidades.
4. Odoo: facturas de cliente publicadas y factura abierta con opción de impresión.
5. UiPath: salida de la corrida exitosa para `datos\prueba_rpa\lote_auxiliar`.
6. Odoo: búsqueda de los clientes y productos que acaba de importar el RPA.

> Antes de compartir el PDF, ocultar cualquier dirección de correo personal, identificador sensible, token, contraseña o dato de acceso que accidentalmente aparezca en las capturas. No incluir `.secrets/`, archivos `.env` ni claves de acceso.

---

## Referencias locales del proyecto

- Infraestructura: `infra/`.
- Datos maestros: `infra/seed_block4.py`.
- Ventas y compras: `infra/seed_block5.py`.
- Portal web: `infra/seed_block6.py` y `assets/brand/`.
- Google Analytics: `infra/seed_block7_ga4.py`.
- Robot: `rpa/QuetzalMart_RPA/Main.xaml`.
- Pruebas del RPA: `datos/prueba_rpa/lote_auxiliar/`.
- Consultas de verificación: `consultas_sql/`.
- PDFs de factura: `outputs/facturas_pdf/`.
- Evidencia digital DMS: `outputs/dms_verified/`.
- Capturas de este manual: `capturas/manual_1/`.
