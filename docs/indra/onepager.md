# TFM Co-diseno IA+FPGA: Tensor-Train (TT) y kernel de contraccion en FPGA

## Resumen ejecutivo
Proyecto de TFM orientado a co-diseno IA+FPGA para acelerar capas lineales mediante Tensor-Train (TT) y un kernel de contraccion TT en FPGA. El foco es reducir SWaP y mejorar determinismo en escenarios con restricciones de soberania y despliegue en borde.

## Alcance
- Descomposicion TT/MPS de pesos para capas lineales y canalizacion de contracciones.
- Kernel de contraccion TT en FPGA con interfaz controlada desde SW.
- Plan de V&V con pruebas funcionales en software y pruebas de integracion HW/SW.

## KPIs
| KPI | Definicion | Estado |
| --- | --- | --- |
| Latencia por contraccion TT (us) | Tiempo por llamada del kernel de contraccion TT en FPGA | Objetivo (TBD) |
| Throughput efectivo (GFLOP/s) | Rendimiento sostenido del kernel de contraccion TT | Objetivo (TBD) |
| Uso de recursos FPGA (LUT/FF/BRAM/DSP, %) | Porcentaje de utilizacion del dispositivo objetivo | Objetivo (TBD) |
| Consumo medio (W) | Potencia media bajo carga representativa | Objetivo (TBD) |
| Determinismo (jitter p99, us) | Variacion temporal p99 por llamada | Objetivo (TBD) |

## Estado actual
- Skeleton de repo con tooling, pruebas y scripts base.
- Flujo SW listo para validar contraccion TT en CPU.
- Interfaz HW/SW definida a nivel de plan de pruebas y contratos de datos.

## Limitaciones actuales
- No hay bitstream FPGA ni mediciones de recursos o potencia.
- No hay resultados de rendimiento en hardware; las metricas permanecen como Objetivo (TBD).

## Proximos pasos
- Implementar kernel de contraccion TT en HLS y validar interfaces.
- Integrar pruebas de latencia y determinismo con medicion repetida y reporte de mediana.

## Contacto
[TU_NOMBRE] - [TU_EMAIL]
