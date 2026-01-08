# TFM Co-diseno IA+FPGA: Tensor-Train (TT) y kernel de contraccion en FPGA

## Slide 1: Contexto y problema
- Necesidad de acelerar capas lineales con restricciones de SWaP / determinismo / soberania.
- Limitaciones de despliegue cuando el costo energetico y la latencia son criticos.

## Slide 2: Propuesta tecnica
- Descomposicion Tensor-Train (TT) aplicada a pesos.
- Kernel de contraccion TT en FPGA con control desde SW.
- Metodologia de V&V con pruebas funcionales y de integracion.

## Slide 3: Arquitectura
- Pipeline SW para generar y validar cores TT.
- Bloque HW para contraccion TT, con interfaces AXI planificadas.
- Mecanismos de trazabilidad de datos y reproducibilidad.

## Slide 4: KPIs
| KPI | Definicion | Estado |
| --- | --- | --- |
| Latencia por contraccion TT (us) | Tiempo por llamada del kernel de contraccion TT en FPGA | Objetivo (TBD) |
| Throughput efectivo (GFLOP/s) | Rendimiento sostenido del kernel de contraccion TT | Objetivo (TBD) |
| Uso de recursos FPGA (LUT/FF/BRAM/DSP, %) | Porcentaje de utilizacion del dispositivo objetivo | Objetivo (TBD) |
| Consumo medio (W) | Potencia media bajo carga representativa | Objetivo (TBD) |
| Determinismo (jitter p99, us) | Variacion temporal p99 por llamada | Objetivo (TBD) |

## Slide 5: Estado actual
- Repo estructurado, scripts de demo y pruebas base.
- Interfaces HW/SW definidas a nivel de especificacion.

## Slide 6: Riesgos y mitigaciones
- Complejidad del kernel en HLS: mitigacion con prototipos incrementales.
- Variabilidad de mediciones: mitigacion con repeticion y reporte de mediana.

## Slide 7: Roadmap
- Hito 1: kernel de contraccion TT funcional en HLS.
- Hito 2: integracion HW/SW y primeras mediciones.
- Hito 3: optimizacion de SWaP y determinismo.

## Contacto
[TU_NOMBRE] - [TU_EMAIL]
