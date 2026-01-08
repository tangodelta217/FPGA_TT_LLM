# TFM Co-diseño IA+FPGA: Tensor-Train (TT) y kernel de contracción TT en FPGA

## Problema
- En inferencia en borde, las capas lineales son bandwidth-bound y el coste de memoria domina; esto penaliza SWaP / determinismo / soberanía.
- La dependencia de DDR/DMA introduce latencia variable y limita la repetibilidad temporal.

## Solución
- Compresión Tensor-Train (TT) de pesos y ejecución con kernel de contracción TT en FPGA.
- Streaming con buffers locales para reducir tráfico a DDR y estabilizar la latencia.

## Qué se entrega
- Demo CPU reproducible en NumPy (TT-SVD + referencia densa) con salidas en `docs/assets/`.
- Skeleton HLS/RTL con AXI4-Lite/AXI-Stream y mapa de registros.
- Plan de V&V con golden model en Python y pruebas automatizadas.

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
- Demo CPU ejecutable con `make demo` y `make benchmarks`; tabla KPI y gráfico en `docs/assets/`.
- Skeleton HW documentado (interfaces, register map y supuestos explícitos).

## Siguiente incremento
- Implementar kernel HLS funcional con pipeline y backpressure.
- Integrar DMA/DDR y validar layout de cores TT en memoria.

## Plan (3 hitos)
1. Kernel de contracción TT en HLS con pruebas unitarias y golden model.
2. Integración HW/SW con DMA y validación de interfaces AXI.
3. Medición de latencia, determinismo y recursos en FPGA (KPIs HW).

## Riesgos y mitigación
- Riesgo: error numérico con ranks bajos. Mitigación: barrido de ranks y validación con golden model.
- Riesgo: cuello de banda DDR. Mitigación: streaming y double buffering.

## Qué necesito de Indra
- Confirmación de plataforma FPGA y restricciones de interfaz.
- Perfiles de carga reales y KPIs prioritarios.

## Contacto
[TU_NOMBRE] - [TU_EMAIL]
