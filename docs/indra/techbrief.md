# TFM Co-diseño IA+FPGA: Tensor-Train (TT) y kernel de contracción TT en FPGA

## Alcance
Este tech brief define el kernel de contracción TT para capas lineales y la arquitectura HW/SW asociada. El foco es reducir tráfico a DDR y mejorar SWaP / determinismo / soberanía en escenarios bandwidth-bound.

## Definición del kernel TT (capas lineales)
- Operación: y = W x, con W en Tensor-Train (TT).
- Cores TT con forma (r_in, n_out, n_in, r_out) y contracción secuencial por modo.
- Alcance: dims factorizadas y ranks fijos; sin batch dinámico.

## Layout de datos y export
- Cores TT linealizados por core para lectura secuencial.
- Dims y ranks empaquetados en registros (ver `docs/assets/register_map.md`).
- Export desde SW con `ml/tt.py` y scripts de demo/benchmarks.

## Arquitectura HLD
- DMA desde DDR hacia buffers de entrada y cores TT.
- Double buffering para solapar transferencia y cómputo.
- MAC array y acumulador con política de saturación definida en HW.
- Output buffer con backpressure por AXI-Stream y contadores de cycles/stalls.

## Interfaces
- AXI4-Lite: control, arranque, estado y contadores.
- AXI-Stream: activaciones de entrada y salida.
- DMA/DDR: cores TT y buffers.

Mapa de registros: [register_map.md](../assets/register_map.md).

## Verificación
- Golden model en Python con referencia TT (`ml/tt.py`).
- Tests unitarios (`tests/test_tt.py`) y ejecución con `make test`.
- Comparación de error relativo y checks de estabilidad.

## Plan de demo CPU + FPGA
1. Validar compresión/error y tiempos en CPU (`make demo`, `make benchmarks`).
2. Integrar kernel HLS con interfaz AXI y testbench RTL.
3. Medir latencia, determinismo y recursos en FPGA y alimentar KPIs HW.

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
- Demo CPU con resultados en `docs/assets/` y tabla KPI reproducible.
- Skeleton HLS/RTL con interfaces y contadores definidos.

## Siguiente incremento
- Implementación funcional del kernel HLS con pipeline estable.
- Testbench RTL con trazas y comparación automática.

## Limitaciones
- No hay bitstream FPGA ni mediciones de recursos/consumo.
- No hay soporte de precisión mixta ni ranks dinámicos por batch.

## Contacto
[TU_NOMBRE] - [TU_EMAIL]
