# TFM Co-diseno IA+FPGA: Tensor-Train (TT) y kernel de contracci?n en FPGA

## Alcance
Este tech brief define el kernel de contracci?n TT para capas lineales y la arquitectura HW/SW asociada. El objetivo es mejorar SWaP / determinismo / soberan?a en escenarios bandwidth-bound.

## Definici?n del kernel TT (capas lineales)
- Operaci?n: y = W x, donde W se representa en Tensor-Train (TT).
- Cores TT con forma (r_in, n_out, n_in, r_out) y contracci?n secuencial por modo.
- Alcance: capas lineales con dims factorizadas (p.ej. 4x4x4x4).

## Layout de datos y export
- Cores TT linealizados por core y rank para acceso secuencial.
- Metadatos de dims y ranks empaquetados en registros o descriptor.
- Export desde SW usando `ml/tt.py` y scripts de demo.

## Arquitectura HLD
- DMA desde DDR hacia buffers de entrada y cores TT.
- Double buffering para solapar transferencia y c?mputo.
- MAC Array y acumulador con control de saturaci?n.
- Output buffer con backpressure por AXI-Stream.

## Interfaces
- AXI4-Lite: control, arranque, estado y contadores.
- AXI-Stream: activaciones de entrada y salida.
- DMA/DDR: cores TT y buffers.

Mapa de registros: [register_map.md](../assets/register_map.md).

## Verificaci?n
- Golden model en Python con referencia TT (`ml/tt.py`).
- Tests unitarios (`tests/test_tt.py`) y ejecuci?n con `make test`.
- Comparaci?n de error relativo y checks de estabilidad.

## Plan de demo CPU + FPGA
1. Validar compresi?n/error y tiempos en CPU (`make demo`, `make benchmarks`).
2. Integrar kernel HLS con interfaz AXI y testbench RTL.
3. Medir latencia y determinismo en FPGA y alimentar KPIs HW.

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
- Demo CPU con resultados en `docs/assets/` y tabla KPI reproducible.
- Skeleton HLS/RTL con interfaces y contadores definidos.

## Siguiente incremento
- Implementaci?n funcional del kernel HLS con pipeline estable.
- Testbench RTL con trazas y comparaci?n autom?tica.

## Limitaciones
- No hay bitstream FPGA ni mediciones de recursos/consumo.
- No hay soporte de precisi?n mixta ni ranks din?micos por batch.

## Contacto
[TU_NOMBRE] - [TU_EMAIL]
