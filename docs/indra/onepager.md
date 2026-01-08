# TFM Co-diseno IA+FPGA: Tensor-Train (TT) y kernel de contracci?n en FPGA

## Problema
- Las capas lineales dominan el coste en escenarios bandwidth-bound y penalizan SWaP / determinismo / soberan?a.
- El acceso a memoria externa limita la latencia y la repetibilidad temporal.

## Soluci?n
- Compresi?n Tensor-Train (TT) de pesos y ejecuci?n con kernel de contracci?n TT en FPGA.
- Pipeline en streaming para reducir tr?fico a DDR y estabilizar latencia.

## Qu? se entrega
- Demo CPU reproducible de TT para capas lineales con m?tricas de compresi?n y error.
- IP skeleton HLS/RTL con interfaces AXI y mapa de registros.
- Plan de V&V con golden model en Python y pruebas autom?ticas.

## KPIs
| KPI | Definici?n | Estado |
| --- | --- | --- |
| Compresi?n efectiva TT (demo CPU) | Ratio dense/TT para ranks evaluados | Medido (ver [kpi_table.md](../assets/kpi_table.md)) |
| Error relativo L2 (demo CPU) | Error relativo de salida vs dense | Medido (ver [kpi_table.md](../assets/kpi_table.md)) |
| Tiempo TT vs dense (us, demo CPU) | Mediana en host CPU | Medido (ver [kpi_table.md](../assets/kpi_table.md)) |
| Latencia por contracci?n TT (us) | Tiempo por llamada del kernel de contracci?n TT en FPGA | Objetivo (TBD) |
| Throughput efectivo (GFLOP/s) | Rendimiento sostenido del kernel de contracci?n TT | Objetivo (TBD) |
| Uso de recursos FPGA (LUT/FF/BRAM/DSP, %) | Porcentaje de utilizaci?n del dispositivo objetivo | Objetivo (TBD) |
| Consumo medio (W) | Potencia media bajo carga representativa | Objetivo (TBD) |
| Determinismo (jitter p99, us) | Variaci?n temporal p99 por llamada | Objetivo (TBD) |

## Estado actual
- Demo TT en CPU con outputs en `docs/assets/` y tabla KPI generada por `make benchmarks`.
- Skeleton HW (HLS/RTL) y documentaci?n de interfaces y registros.

## Siguiente incremento
- Implementar kernel HLS con pipeline estable y backpressure.
- Integrar DMA/DDR y validar layout de cores TT en memoria.

## Plan (3 hitos)
1. Kernel de contracci?n TT en HLS con pruebas unitarias b?sicas.
2. Integraci?n HW/SW con DMA y validaci?n de interfaces AXI.
3. Medici?n de latencia, determinismo y recursos en FPGA (KPIs HW).

## Riesgos y mitigaci?n
- Riesgo: error num?rico por cuantizaci?n. Mitigaci?n: golden model y tolerancias por rango.
- Riesgo: ancho de banda insuficiente. Mitigaci?n: streaming y double buffering.

## Qu? necesito de Indra
- Revisi?n de requisitos de interfaz y plataforma FPGA objetivo.
- Feedback sobre KPIs prioritarios y perfiles de carga reales.

## Contacto
[TU_NOMBRE] - [TU_EMAIL]
