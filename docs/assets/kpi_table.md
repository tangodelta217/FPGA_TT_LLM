# KPI demo TT (CPU)
Contexto: dims_out=4x4x4x4, dims_in=4x4x4x4, ranks=1-2-2-2-1|1-4-4-4-1|1-8-8-8-1|1-16-16-16-1, repeticiones=40, semilla=0
Modelo sintetico: pesos generados con TT base rank=1-8-8-8-1.
Medicion: host CPU (no FPGA). Tiempos en microsegundos, mediana de 40 repeticiones.

| rank | comp_ratio | comp_pct | rel_l2 | max_abs | dense_us | tt_us |
| --- | --- | --- | --- | --- | --- | --- |
| 1-2-2-2-1 | 341.33 | 99.7% | 8.852e-01 | 1.005e+03 | 4.10 | 27.15 |
| 1-4-4-4-1 | 102.40 | 99.0% | 7.184e-01 | 9.763e+02 | 4.10 | 30.10 |
| 1-8-8-8-1 | 28.44 | 96.5% | 3.080e-15 | 4.064e-12 | 4.10 | 38.30 |
| 1-16-16-16-1 | 7.53 | 86.7% | 2.545e-15 | 4.206e-12 | 4.10 | 63.70 |
