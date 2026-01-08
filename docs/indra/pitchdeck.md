---
marp: true
title: TFM Co-diseno IA+FPGA: Tensor-Train (TT) y kernel de contracci?n en FPGA
---

# TFM Co-diseno IA+FPGA: Tensor-Train (TT) y kernel de contracci?n en FPGA
## Co-diseno IA+FPGA para capas lineales

---

## Problema
- Capas lineales bandwidth-bound y coste dominante en inferencia.
- Necesidad de SWaP / determinismo / soberan?a en borde.

---

## Soluci?n
- Compresi?n Tensor-Train (TT) para pesos de capas lineales.
- Kernel de contracci?n TT en FPGA con streaming y control AXI.

---

## Arquitectura (HLD)
- AXI4-Lite para control y estado.
- AXI-Stream/DMA para activaciones y cores TT.
- Buffers locales y pipeline de MAC + acumulaci?n.

---

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

---

## Evidencia (demo CPU)
![Tradeoff TT](../assets/bench_tradeoff.png)

Tabla KPI: [kpi_table.md](../assets/kpi_table.md)

---

## Plan
1. Kernel HLS con pipeline y backpressure.
2. Integraci?n HW/SW con DMA y layout de cores TT.
3. Medici?n de KPIs HW en plataforma objetivo.

---

## Ask to Indra
- Validaci?n de plataforma FPGA y restricciones de interfaz.
- Definici?n de perfiles de carga y l?mites de SWaP / determinismo / soberan?a.
- Mentorizaci?n t?cnica y revisi?n de V&V.
