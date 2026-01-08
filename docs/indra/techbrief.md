# TFM Co-diseno IA+FPGA: Tensor-Train (TT) y kernel de contracción en FPGA

## Objetivo tecnico
Implementar un flujo SW/HW para capas lineales comprimidas con Tensor-Train (TT), con un kernel de contracción TT en FPGA orientado a mejorar SWaP y determinismo en escenarios con requisitos de soberanía.

## Arquitectura propuesta
- SW: generacion de cores TT, validacion funcional y empaquetado de datos de entrada.
- HW: kernel de contracción TT con interfaz de memoria y control a definir (AXI/MM y AXI-Lite).
- V&V: pruebas unitarias en SW, pruebas de integracion HW/SW y trazabilidad de resultados.

## Kernel de contracción TT
- Operacion base: contracción secuencial de cores TT con vectores de entrada.
- Foco en reutilizacion de datos y pipeline para reducir latencia.
- Parametros objetivo: tamanos de TT, rangos y precision configurable.

## Interfaces HW/SW
- Entrada: cores TT serializados y vectores por modo.
- Salida: escalares o tensores intermedios segun el modo de uso.
- Validacion: checksum y comparacion contra referencia en SW.

## KPIs
| KPI | Definición | Estado |
| --- | --- | --- |
| Latencia por contracción TT (us) | Tiempo por llamada del kernel de contracción TT en FPGA | Objetivo (TBD) |
| Throughput efectivo (GFLOP/s) | Rendimiento sostenido del kernel de contracción TT | Objetivo (TBD) |
| Uso de recursos FPGA (LUT/FF/BRAM/DSP, %) | Porcentaje de utilización del dispositivo objetivo | Objetivo (TBD) |
| Consumo medio (W) | Potencia media bajo carga representativa | Objetivo (TBD) |
| Determinismo (jitter p99, us) | Variación temporal p99 por llamada | Objetivo (TBD) |

## Plan de verificacion y validacion
- Pruebas unitarias de contracción TT en SW con seeds fijos.
- Pruebas de regresion con casos pequenos y trazas guardadas en docs/assets.
- Pruebas HW/SW con medicion repetida de latencia y reporte de mediana.

## Limitaciones actuales
- No hay bitstream FPGA ni resultados de temporizacion o consumo.
- No hay mediciones de recursos del dispositivo objetivo.

## Riesgos y mitigaciones
- Riesgo: desajuste numerico entre SW y HW. Mitigacion: pruebas con tolerancia y seeds fijos.
- Riesgo: limitaciones de ancho de banda. Mitigacion: layout de memoria y streaming.

## Contacto
[TU_NOMBRE] - [TU_EMAIL]
