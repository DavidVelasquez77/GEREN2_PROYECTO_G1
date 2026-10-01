# QUETZALMART

## Manual 3 — Inteligencia de negocios con Google Analytics 4

**Proyecto:** Implementación ERP y comercio electrónico  
**Versión:** 1.0  
**Fecha del corte analizado:** 30 de septiembre de 2026  
**Fuente:** Propiedad GA4 «QuetzalMart Web»  
**Formato:** Markdown con gráficos vectoriales SVG

---

## 1. Resumen ejecutivo

Este análisis utiliza el informe **Adquisición de tráfico: Campaña de la sesión** de GA4, filtrado para el 30 de septiembre de 2026. En el corte observado, el informe presenta **21 sesiones**, **237 eventos** y **Q144,98 de ingresos totales**. La campaña `beneficios_temporada_2026` aparece atribuida con **Q106,42** y un evento clave.

El principal hallazgo de calidad de datos es que el informe muestra **21 sesiones en el total**, mientras las filas de campaña suman **26**. Además, GA4 marca `(not set)` con una advertencia de atribución. Por esa diferencia, el gráfico conserva los números tal como aparecen, pero no interpreta las filas como un reparto reconciliado de todas las sesiones.

> **Conclusión para negocio:** la campaña de temporada ya aparece en GA4 con ingresos atribuidos; sin embargo, hay que corregir y volver a comprobar la atribución de sesiones antes de usar el reparto de tráfico como indicador definitivo.

---

## 2. Fuente y alcance de los datos

| Campo | Valor del informe observado |
|---|---|
| Propiedad / flujo | QuetzalMart Web |
| Informe | Adquisición de tráfico |
| Dimensión principal | Campaña de la sesión |
| Periodo | 30 de septiembre de 2026 |
| Estado indicado por GA4 | Datos prácticamente completos |
| Moneda | Quetzales (Q) |

Los datos son una **fotografía de un solo día**, no una tendencia mensual. GA4 puede actualizar informes después del momento de consulta. Por eso, las cifras deben presentarse con la fecha del corte y no mezclarse con periodos diferentes.

### Indicadores generales observados

| Indicador | Resultado | Lectura |
|---|---:|---|
| Sesiones | 21 | Sesiones mostradas en el total del informe. |
| Sesiones con interacción | 3 | Sesiones que GA4 clasificó como con interacción. |
| Porcentaje de interacciones | 14,29 % | 3 sesiones con interacción sobre 21 sesiones del total. |
| Tiempo de interacción medio por sesión | 6 min 13 s | Promedio presentado por GA4 para el periodo. |
| Eventos por sesión | 11,29 | Promedio presentado por GA4. |
| Número de eventos | 237 | Eventos contabilizados en el informe. |
| Eventos clave | 2 | GA4 agrupa aquí los eventos marcados como clave. |
| Tasa de evento clave de sesión | 9,52 % | Tasa mostrada por GA4; no debe llamarse tasa de compra hasta confirmar el nombre del evento clave. |
| Ingresos totales | Q144,98 | Ingresos atribuidos por GA4 para el periodo; contrastarlos con las facturas de Odoo. |

---

## 3. Análisis visual de adquisición y rendimiento

### 3.1 Sesiones atribuidas por campaña

![Sesiones que GA4 muestra por campaña de sesión](graficos/01_sesiones_por_campana.svg)

Las filas visibles muestran `beneficios_temporada_2026` con 2 sesiones y `(not set)` con 12. Sin embargo, al sumar las ocho filas se obtienen **26**, frente a **21** sesiones en el total. Las proporciones mostradas por fila tampoco representan un reparto que sume 100 %. Por eso, este gráfico sirve para localizar valores y anomalías, no para afirmar la participación exacta de cada fuente sobre un total reconciliado.

GA4 presenta una advertencia para `(not set)` indicando que faltan datos de sesión para atribuir correctamente algunas interacciones. El dato debe tratarse como una señal de calidad de instrumentación, no como una campaña real.

### 3.2 Ingresos atribuidos por campaña

![Ingresos totales de GA4 por campaña de sesión](graficos/02_ingresos_por_campana.svg)

La fila `beneficios_temporada_2026` registra **Q106,42**, equivalente al **73,4 %** de los Q144,98 del total. La fila `(not set)` registra **Q38,56** —el **26,6 %** restante— sin un nombre de campaña atribuible. La suma de estas dos filas coincide con el total de ingresos del informe.

Este resultado demuestra atribución de ingresos a la campaña identificada en GA4. El informe observado agrupa el conteo en **Eventos clave**; para afirmar que ese evento fue específicamente `purchase`, se debe abrir el desglose por nombre del evento y mostrarlo junto al informe de compras. Los ingresos de GA4 tampoco equivalen automáticamente a ingresos netos contables: se contrastan con las facturas y los pagos en Odoo.

### 3.3 Actividad medida por campaña

![Eventos registrados por campaña de sesión](graficos/03_eventos_por_campana.svg)

GA4 contabiliza **237 eventos**. De ellos, 131 aparecen en `(not set)` y 46 en `beneficios_temporada_2026`. La suma de los eventos por fila sí coincide con el total. Esto permite ver que una parte importante de la actividad todavía no tiene una campaña atribuida, aunque el informe ya registra actividad e ingresos para la campaña de temporada.

---

## 4. Detalle de filas del informe

Los valores siguientes transcriben las filas que se ven en GA4 para el mismo periodo. Las columnas de sesiones se conservan tal como aparecen; debido a la falta de conciliación descrita arriba, no se deben sumar para calcular participación de tráfico.

| Campaña de la sesión | Sesiones mostradas | Sesiones con interacción | Eventos | Eventos clave | Tasa de evento clave de sesión | Ingresos |
|---|---:|---:|---:|---:|---:|---:|
| `validacion_ga4_sep2026` | 1 | 1 | 15 | 0 | 0 % | Q0,00 |
| `ga4_demostracion_v2` | 2 | 0 | 4 | 0 | 0 % | Q0,00 |
| `ga4_demo_utm_2026` | 1 | 0 | 2 | 0 | 0 % | Q0,00 |
| `campana_validacion_20260930` | 1 | 0 | 2 | 0 | 0 % | Q0,00 |
| `beneficios_temporada_2026` | 2 | 1 | 46 | 1 | 50 % | Q106,42 |
| `(not set)` | 12 | 0 | 131 | 1 | 8,33 % | Q38,56 |
| `(direct)` | 4 | 1 | 29 | 0 | 0 % | Q0,00 |
| `(cross-network)` | 3 | 0 | 8 | 0 | 0 % | Q0,00 |
| **Total mostrado por GA4** | **21** | **3** | **237** | **2** | **9,52 %** | **Q144,98** |

**Control de consistencia:** las sesiones de las filas suman 26; el total del informe es 21. Las demás columnas mostradas sí concilian con el total (sesiones con interacción, eventos, eventos clave e ingresos). Este control se incluye deliberadamente para no ocultar la advertencia de atribución.

---

## 5. Hallazgos y decisiones de negocio

### Hallazgo 1: la campaña de temporada genera ingresos medibles

`beneficios_temporada_2026` aparece en el informe y se asocia con Q106,42, 46 eventos y un evento clave. Su tasa de evento clave de sesión reportada es 50 %. Es una señal positiva para evaluar la campaña, pero el informe por sí solo no identifica en esta tabla el nombre exacto del evento clave ni proporciona costo publicitario.

**Decisión recomendada:** conservar el nombre UTM de la campaña en los enlaces de correo y publicidad; comparar en GA4 sus sesiones, evento `purchase` e ingresos por periodos equivalentes. No presentar retorno sobre inversión publicitaria (ROAS) sin registrar también el gasto de la campaña.

### Hallazgo 2: `(not set)` concentra una advertencia relevante

GA4 muestra 12 sesiones, 131 eventos, un evento clave y Q38,56 en esa fila, pero advierte que faltan datos de sesión para atribuir correctamente. Esa fila representa el problema más claro para mejorar la lectura de adquisición y la atribución de ingresos.

**Decisión recomendada:** revisar la configuración de consentimiento y que los eventos de la tienda se envíen con su contexto de sesión. Después de corregirla, generar nuevas visitas de prueba y volver a comparar el resumen con las filas por campaña. La corrección afecta principalmente datos futuros; los informes anteriores no necesariamente se reconstruyen.

### Hallazgo 3: actividad y atribución no son lo mismo

Que GA4 registre eventos no demuestra por sí mismo que la sesión tenga una campaña identificable, ni que cada evento corresponda a una compra terminada. Para evaluar el embudo se debe comprobar cada nombre de evento y su secuencia.

**Decisión recomendada:** validar `view_item`, `add_to_cart`, `begin_checkout` y `purchase` en los informes de eventos y en una exploración de embudo. Registrar como compra completada solo las sesiones que alcancen `purchase`.

### Hallazgo 4: faltan costos para medir rentabilidad de marketing

El informe observado presenta ingresos y adquisición, pero no el gasto de cada campaña. Sin costo no se puede calcular con estos datos el ROAS, el costo por adquisición ni la rentabilidad neta.

**Decisión recomendada:** si se desea evaluar rentabilidad y no solo tráfico/ingresos atribuidos, incorporar el costo de campañas con la función de importación de costos o mantenerlo en un reporte financiero separado.

---

## 6. Cómo completar la lectura del comercio electrónico

El informe de adquisición usado para estos gráficos no presenta nombres de productos ni el conteo desglosado de cada evento del embudo. Para completar el análisis de comercio electrónico en GA4, revisar estos datos en los informes correspondientes:

| Pregunta de negocio | Dato que se debe mostrar en GA4 | Interpretación |
|---|---|---|
| ¿Qué productos atraen interés? | Evento `view_item` y reporte por nombre/ID del artículo. | Productos vistos y su proporción frente a los agregados al carrito. |
| ¿Qué productos se agregan al carrito? | Evento `add_to_cart` y artículos agregados. | Demanda inicial por producto. |
| ¿Dónde se abandona la compra? | Pasos `add_to_cart` → `begin_checkout` → `purchase` en una exploración de embudo. | Pérdida de usuarios entre pasos; revisar si el embudo está abierto o cerrado según la pregunta. |
| ¿Qué productos se venden más? | Informe de compras de comercio electrónico, con nombre/ID del artículo, unidades e ingresos del artículo. | Ranking por unidades vendidas e ingresos; no inferirlo solo a partir de sesiones o vistas. |
| ¿Qué proporción completa la compra? | Usuarios o sesiones que llegan a `purchase` frente al conjunto definido como inicio del embudo. | Tasa de conversión, indicando siempre denominador y periodo. |

Las tasas de un embudo se deben calcular a partir de usuarios/sesiones consistentes en el mismo periodo; no es correcto dividir cantidades de eventos de distinto tipo y llamarlas automáticamente tasa de conversión. Una exploración de carrito abandonado debe incluir sesiones con `add_to_cart` que no llegaron a `purchase` dentro del criterio temporal del informe.

---

## 7. Uso de segmentos y exploraciones para decisiones

Los segmentos permiten comparar grupos de usuarios o sesiones. Las exploraciones convierten esa comparación en preguntas operativas. Para la exposición se recomienda mostrar dos análisis:

1. **Exploración de embudo de compra:** aplicar los segmentos de usuarios y comparar visualizaciones de producto, carrito, inicio de pago y compra. Mostrar usuarios/sesiones por paso y abandono entre pasos.
2. **Exploración de campaña y carrito:** comparar las sesiones con campaña `beneficios_temporada_2026` frente a `(not set)` y tráfico directo; incluir carrito, `purchase` e ingresos, con el mismo intervalo de fechas.

Los segmentos y exploraciones deben estar seleccionados en el informe y tener datos para el periodo presentado. Que estén guardados en GA4 no significa que cada tabla tenga datos. Si una exploración aparece vacía, ampliar el periodo a días con actividad y revisar que los filtros no excluyan las sesiones de prueba.

---

## 8. Guía breve para presentar los resultados

1. Abrir GA4 y seleccionar la propiedad **QuetzalMart Web**.
2. Entrar a **Informes → Adquisición → Adquisición de tráfico**.
3. Elegir el periodo del corte que se presenta y la dimensión **Campaña de la sesión**.
4. Mostrar las métricas de sesiones, sesiones con interacción, eventos clave e ingresos totales.
5. Buscar `beneficios_temporada_2026` y señalar los Q106,42 atribuidos; luego abrir el desglose del evento clave para demostrar si corresponde a `purchase`.
6. Mostrar la advertencia de `(not set)` y explicar que las filas por campaña no concilian con el total de sesiones en este corte.
7. Abrir los informes de eventos y de compras de comercio electrónico para demostrar nombres de productos, artículos vendidos y los eventos del embudo.
8. Abrir las dos exploraciones con el mismo periodo y los segmentos seleccionados.
9. Comparar la compra web y su factura con el pedido y la factura de Odoo; GA4 mide comportamiento, mientras Odoo conserva los registros comerciales.

### Nota de interpretación

El porcentaje de interacciones, la tasa de evento clave de sesión y la tasa de conversión de compra son métricas distintas. En la presentación se debe conservar el nombre de cada métrica de GA4 y especificar periodo, dimensión y denominador. Los gráficos adjuntos reproducen únicamente el informe de adquisición del 30 de septiembre de 2026.

---

## Anexo — Archivos de gráficos

El documento utiliza tres gráficos SVG guardados en `manual_3/graficos/`. Para conservarlos al mover o convertir el manual, mantener la carpeta `graficos` junto al archivo Markdown. Los gráficos se pueden ampliar sin perder nitidez y usan los valores visibles en GA4 para el corte indicado.

