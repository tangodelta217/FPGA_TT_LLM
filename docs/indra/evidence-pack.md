# TFM Co-diseno IA+FPGA: Tensor-Train (TT) y kernel de contraccion en FPGA

## Evidencias actuales
- docs/assets/demo_output.txt: salida de demo funcional de contraccion TT en CPU (generada con `make demo`).

## Como reproducir
1. `make setup`
2. `make demo`

## KPIs
| KPI | Definicion | Estado |
| --- | --- | --- |
| Latencia por contraccion TT (us) | Tiempo por llamada del kernel de contraccion TT en FPGA | Objetivo (TBD) |
| Throughput efectivo (GFLOP/s) | Rendimiento sostenido del kernel de contraccion TT | Objetivo (TBD) |
| Uso de recursos FPGA (LUT/FF/BRAM/DSP, %) | Porcentaje de utilizacion del dispositivo objetivo | Objetivo (TBD) |
| Consumo medio (W) | Potencia media bajo carga representativa | Objetivo (TBD) |
| Determinismo (jitter p99, us) | Variacion temporal p99 por llamada | Objetivo (TBD) |

## Limitaciones
- Evidencia centrada en validacion funcional en SW; no hay bitstream FPGA.
- No hay mediciones de potencia o recursos en hardware.

## Contacto
[TU_NOMBRE] - [TU_EMAIL]
