# KPI demo TT (CPU)
Contexto: dims_out=4x4x4x4, dims_in=4x4x4x4, ranks=1-2-2-2-1|1-4-4-4-1|1-8-8-8-1, repeticiones=30, semilla=0
Modelo sintetico: pesos generados con TT base rank=1-4-4-4-1.
Medicion: host CPU (no FPGA). Tiempos en microsegundos, mediana de 30 repeticiones.

| rank | comp_ratio | comp_pct | rel_l2 | max_abs | dense_us | tt_us |
| --- | --- | --- | --- | --- | --- | --- |
| 1-2-2-2-1 | 341.33 | 99.7% | 8.518e-01 | 6.268e+00 | 3.90 | 24.25 |
| 1-4-4-4-1 | 102.40 | 99.0% | 1.600e-15 | 1.066e-14 | 3.90 | 27.70 |
| 1-8-8-8-1 | 28.44 | 96.5% | 1.788e-15 | 2.043e-14 | 3.90 | 38.60 |
