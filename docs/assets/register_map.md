# Register Map (TT Contraction Engine)

| Registro | Offset | Descripción |
| --- | --- | --- |
| CTRL | 0x00 | bit0 start, bit1 soft_reset, bit2 irq_en |
| STATUS | 0x04 | bit0 busy, bit1 done, bit2 error |
| IN_PTR | 0x08 | Dirección base de activaciones de entrada |
| OUT_PTR | 0x0C | Dirección base de salida |
| CORES_PTR | 0x10 | Dirección base de cores TT |
| DIMS | 0x14 | Packed dims (d0,d1,d2,d3) |
| RANKS | 0x18 | Packed ranks (r0,r1,r2,r3,r4) |
| SCALE_PTR | 0x1C | Dirección de escalas para cuantización |
| CYCLES | 0x20 | Contador de ciclos | 
| STALLS | 0x24 | Contador de stalls |
| ERR | 0x28 | Código de error latched |

## Secuencia de programación (ejemplo)
1. Escribir IN_PTR, OUT_PTR, CORES_PTR y SCALE_PTR.
2. Configurar DIMS y RANKS con los valores de la capa.
3. Limpiar STATUS leyendo el registro.
4. Escribir CTRL.start=1.
5. Esperar STATUS.done=1.
6. Leer CYCLES y STALLS para métricas.

## Supuestos explícitos
- Direcciones alineadas a 64 bytes.
- Tamaños soportados en múltiplos de 4 elementos.

## Límites actuales
- No soporta múltiples streams concurrentes.
- No soporta reconfiguración de precisión en caliente.
