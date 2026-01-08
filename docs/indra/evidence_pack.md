# TFM Co-diseño IA+FPGA: Tensor-Train (TT) y kernel de contracción TT en FPGA

## Enlaces clave
- README del repo: [README.md](../../README.md)
- Demo script: [demo_tt_linear.py](../../scripts/demo_tt_linear.py)
- Benchmarks script: [run_benchmarks.py](../../scripts/run_benchmarks.py)

## Evidencias (comando + archivo + interpretación)
- Demo TT CPU: comando `make demo`; archivo [demo_output.txt](../assets/demo_output.txt); interpretación: valida compresión, error y tiempos en host CPU para ranks definidos.
- Benchmarks TT CPU: comando `make benchmarks`; archivos [bench_results.csv](../assets/bench_results.csv), [bench_tradeoff.png](../assets/bench_tradeoff.png), [kpi_table.md](../assets/kpi_table.md); interpretación: resume trade-off compresión/error y tiempos medianos en CPU por rank.

## Gráfico y tabla KPI (demo CPU)
![Tradeoff TT](../assets/bench_tradeoff.png)

Tabla tomada de `docs/assets/kpi_table.md`:

## KPI demo TT (CPU)
Contexto: dims_out=4x4x4x4, dims_in=4x4x4x4, ranks=1-2-2-2-1|1-4-4-4-1|1-8-8-8-1|1-16-16-16-1, repeticiones=40, semilla=0
Modelo sintetico: pesos generados con TT base rank=1-8-8-8-1.
Medicion: host CPU (no FPGA). Tiempos en microsegundos, mediana de 40 repeticiones.

| rank | comp_ratio | comp_pct | rel_l2 | max_abs | dense_us | tt_us |
| --- | --- | --- | --- | --- | --- | --- |
| 1-2-2-2-1 | 341.33 | 99.7% | 8.852e-01 | 1.005e+03 | 4.10 | 27.15 |
| 1-4-4-4-1 | 102.40 | 99.0% | 7.184e-01 | 9.763e+02 | 4.10 | 30.10 |
| 1-8-8-8-1 | 28.44 | 96.5% | 3.080e-15 | 4.064e-12 | 4.10 | 38.30 |
| 1-16-16-16-1 | 7.53 | 86.7% | 2.545e-15 | 4.206e-12 | 4.10 | 63.70 |


## Snippet de demo_output.txt
```text
Demo TT para capa lineal
Contexto: dims_out=4x4x4x4, dims_in=4x4x4x4, ranks=1-2-2-2-1|1-4-4-4-1|1-8-8-8-1, repeticiones=30, semilla=0
Modelo sintetico: pesos generados con TT base rank=1-4-4-4-1.
Medicion: host CPU (no FPGA). Tiempos en microsegundos, mediana de 30 repeticiones.
Dense baseline (us): 5.40

| rank | comp_ratio | comp_pct | rel_l2 | max_abs | tt_us |
| --- | --- | --- | --- | --- | --- |
| 1-2-2-2-1 | 341.33 | 99.7% | 8.518e-01 | 6.268e+00 | 26.85 |
| 1-4-4-4-1 | 102.40 | 99.0% | 1.600e-15 | 1.066e-14 | 30.70 |
| 1-8-8-8-1 | 28.44 | 96.5% | 1.788e-15 | 2.043e-14 | 38.80 |
```

## Checklist de reproducibilidad
- `make demo`
- `make benchmarks`
- `make test`

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

## Limitaciones
- Evidencia centrada en validación funcional en SW; no hay bitstream FPGA.
- No hay mediciones de potencia o recursos en hardware.

## Contacto
[TU_NOMBRE] - [TU_EMAIL]
