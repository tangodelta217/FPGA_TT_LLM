# TFM Co-diseno IA+FPGA: Tensor-Train (TT) y kernel de contracción en FPGA

## Problema
- Las capas lineales dominan el coste en escenarios bandwidth-bound y penalizan SWaP / determinismo / soberanía.
- El acceso a memoria externa limita la latencia y la repetibilidad temporal.

## Solución
- Compresión Tensor-Train (TT) de pesos y ejecución con kernel de contracción TT en FPGA.
- Pipeline en streaming para reducir tráfico a DDR y estabilizar latencia.

## Qué se entrega
- Demo CPU reproducible de TT para capas lineales con métricas de compresión y error.
- IP skeleton HLS/RTL con interfaces AXI y mapa de registros.
- Plan de V&V con golden model en Python y pruebas automáticas.

## KPIs
| KPI | Definición | Estado |
| --- | --- | --- |
| Compresión efectiva TT (demo CPU) | Ratio dense/TT para ranks evaluados | Medido (ver [kpi_table.md](../assets/kpi_table.md)) |
| Error relativo L2 (demo CPU) | Error relativo de salida vs dense | Medido (ver [kpi_table.md](../assets/kpi_table.md)) |
| Tiempo TT vs dense (us, demo CPU) | Mediana en host CPU | Medido (ver [kpi_table.md](../assets/kpi_table.md)) |
| Latencia por contracción TT (us) | Tiempo por llamada del kernel de contracción TT en FPGA | Objetivo (TBD) |
| Throughput efectivo (GFLOP/s) | Rendimiento sostenido del kernel de contracción TT | Objetivo (TBD) |
| Uso de recursos FPGA (LUT/FF/BRAM/DSP, %) | Porcentaje de utilización del dispositivo objetivo | Objetivo (TBD) |
| Consumo medio (W) | Potencia media bajo carga representativa | Objetivo (TBD) |
| Determinismo (jitter p99, us) | Variación temporal p99 por llamada | Objetivo (TBD) |

## Estado actual
- Demo TT en CPU con outputs en `docs/assets/` y tabla KPI generada por `make benchmarks`.
- Skeleton HW (HLS/RTL) y documentación de interfaces y registros.

## Siguiente incremento
- Implementar kernel HLS con pipeline estable y backpressure.
- Integrar DMA/DDR y validar layout de cores TT en memoria.

## Plan (3 hitos)
1. Kernel de contracción TT en HLS con pruebas unitarias básicas.
2. Integración HW/SW con DMA y validación de interfaces AXI.
3. Medición de latencia, determinismo y recursos en FPGA (KPIs HW).

## Riesgos y mitigación
- Riesgo: error numérico por cuantización. Mitigación: golden model y tolerancias por rango.
- Riesgo: ancho de banda insuficiente. Mitigación: streaming y double buffering.

## Qué necesito de Indra
- Revisión de requisitos de interfaz y plataforma FPGA objetivo.
- Feedback sobre KPIs prioritarios y perfiles de carga reales.

## Contacto
[TU_NOMBRE] - [TU_EMAIL]
