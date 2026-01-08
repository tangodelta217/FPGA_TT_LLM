# TFM Co-diseno IA+FPGA: Tensor-Train (TT) y kernel de contracción en FPGA

## Evidencias actuales
- docs/assets/demo_output.txt: salida de demo funcional de contracción TT en CPU (generada con `make demo`).
- docs/assets/bench_results.csv: resultados de benchmarks en CPU (generada con `make benchmarks`).
- docs/assets/bench_tradeoff.png: gráfico de trade-off compresión vs error (generado con `make benchmarks`).
- docs/assets/kpi_table.md: tabla KPI de compresión, error y tiempos en CPU (generada con `make benchmarks`).

## Gráfico y tabla
![Tradeoff TT](../assets/bench_tradeoff.png)

Tabla KPI: `../assets/kpi_table.md`

## Demo output
Archivo: `../assets/demo_output.txt`
```text
Demo TT para capa lineal
Contexto: dims_out=4x4x4x4, dims_in=4x4x4x4, ranks=1-2-2-2-1|1-4-4-4-1|1-8-8-8-1, repeticiones=30, semilla=0
Modelo sintetico: pesos generados con TT base rank=1-4-4-4-1.
Medicion: host CPU (no FPGA). Tiempos en microsegundos, mediana de 30 repeticiones.
Dense baseline (us): 3.90

| rank | comp_ratio | comp_pct | rel_l2 | max_abs | tt_us |
| --- | --- | --- | --- | --- | --- |
| 1-2-2-2-1 | 341.33 | 99.7% | 8.518e-01 | 6.268e+00 | 24.25 |
| 1-4-4-4-1 | 102.40 | 99.0% | 1.600e-15 | 1.066e-14 | 27.70 |
| 1-8-8-8-1 | 28.44 | 96.5% | 1.788e-15 | 2.043e-14 | 38.60 |
```

## KPIs
| KPI | Definición | Estado |
| --- | --- | --- |
| Latencia por contracción TT (us) | Tiempo por llamada del kernel de contracción TT en FPGA | Objetivo (TBD) |
| Throughput efectivo (GFLOP/s) | Rendimiento sostenido del kernel de contracción TT | Objetivo (TBD) |
| Uso de recursos FPGA (LUT/FF/BRAM/DSP, %) | Porcentaje de utilización del dispositivo objetivo | Objetivo (TBD) |
| Consumo medio (W) | Potencia media bajo carga representativa | Objetivo (TBD) |
| Determinismo (jitter p99, us) | Variación temporal p99 por llamada | Objetivo (TBD) |

## Limitaciones
- Evidencia centrada en validación funcional en SW; no hay bitstream FPGA.
- No hay mediciones de potencia o recursos en hardware.

## Contacto
[TU_NOMBRE] - [TU_EMAIL]
