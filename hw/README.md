# TFM Co-diseno IA+FPGA: Tensor-Train (TT) y kernel de contracción en FPGA

## Visión general
El bloque HW es un TT Contraction Engine orientado a acelerar capas lineales comprimidas en Tensor-Train (TT). El objetivo es ejecutar contracciones TT en streaming con control por AXI4-Lite y transferencia de datos por AXI-Stream/DMA.

## Interfaces previstas
- AXI4-Lite: control, configuración y lectura de contadores.
- AXI-Stream: entrada/salida de activaciones y resultados.
- DMA/DDR: acceso a cores TT y buffers de entrada/salida.

## Data layout (alto nivel)
- Cores TT almacenados como tensores 4D con forma (r_in, n_out, n_in, r_out).
- Orden linealizado por core, modo y rank para acceso secuencial en streaming.
- Metadatos (dims, ranks) en registros o descriptor de DMA.

## Supuestos explícitos
- Ancho de palabra: 16 bits fijo (Q1.14) para datos y pesos.
- Formato de stream: AXI-Stream con tdata empaquetado en 32 bits (2 muestras de 16 bits).
- Política de saturación: saturación aritmética en acumuladores de 32 bits.

## Límites actuales
- No se soporta precisión mixta ni formatos FP16/FP32.
- No hay soporte para ranks dinámicos por batch.
- No hay bitstream ni implementación HLS/RTL funcional, solo skeleton.

## Plan de verificación
- Golden model en Python con referencia TT (ml/tt.py).
- Testbench RTL con estímulos sintéticos y comparación contra golden.
- Métricas de V&V: exactitud relativa, latencia por transacción, conteo de stalls.

## Qué está implementado hoy
- Estructura HW, mapas de registros y skeleton HLS/RTL.
- Scripts SW de demo/bench para validar contracción TT en CPU.

## Roadmap
- Implementar kernel HLS con pipeline y streaming completo.
- Integrar DMA/DDR y layout definitivo de cores TT.
- Añadir mediciones de latencia/recursos en FPGA y cerrar KPIs.
