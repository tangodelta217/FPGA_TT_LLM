# TFM Co-diseno IA+FPGA: Tensor-Train (TT) y kernel de contracción en FPGA

![CI](docs/assets/ci_badge.svg)

## Problema
- Las capas lineales dominan el coste en escenarios bandwidth-bound y penalizan SWaP / determinismo / soberanía.
- El acceso a memoria externa limita la latencia y la repetibilidad temporal.

## Solución
- Compresión Tensor-Train (TT) de pesos y ejecución con kernel de contracción TT en FPGA.
- Pipeline en streaming para reducir tráfico a DDR y estabilizar latencia.

## Qué se entrega
- Demo CPU reproducible de TT para capas lineales con métricas de compresión y error.
- IP skeleton HLS/RTL con interfaces AXI y mapa de registros.
- Paquete Indra con onepager, pitchdeck, techbrief y evidence pack.

## Quickstart
```bash
python -m pip install -r requirements.txt
make demo
make benchmarks
make test
```
Salidas principales: `docs/assets/demo_output.txt`, `docs/assets/kpi_table.md`, `docs/assets/bench_tradeoff.png`.

## Arquitectura
```mermaid
flowchart LR
    CPU[CPU / Host SW]
    DMA[DMA/AXI]
    BUF[Buffers on-chip]
    KERNEL[kernel de contracción TT]

    CPU -->|control AXI-Lite| KERNEL
    CPU -->|DMA/AXI-MM| DMA
    DMA <--> BUF
    BUF <--> KERNEL
```

## KPIs
| KPI | Definición | Estado |
| --- | --- | --- |
| Compresión efectiva TT (demo CPU) | Ratio dense/TT para ranks evaluados | Medido (ver [kpi_table.md](docs/assets/kpi_table.md)) |
| Error relativo L2 (demo CPU) | Error relativo de salida vs dense | Medido (ver [kpi_table.md](docs/assets/kpi_table.md)) |
| Tiempo TT vs dense (us, demo CPU) | Mediana en host CPU | Medido (ver [kpi_table.md](docs/assets/kpi_table.md)) |
| Latencia por contracción TT (us) | Tiempo por llamada del kernel de contracción TT en FPGA | Objetivo (TBD) |
| Throughput efectivo (GFLOP/s) | Rendimiento sostenido del kernel de contracción TT | Objetivo (TBD) |
| Uso de recursos FPGA (LUT/FF/BRAM/DSP, %) | Porcentaje de utilización del dispositivo objetivo | Objetivo (TBD) |
| Consumo medio (W) | Potencia media bajo carga representativa | Objetivo (TBD) |
| Determinismo (jitter p99, us) | Variación temporal p99 por llamada | Objetivo (TBD) |

## Evidence
![Tradeoff TT](docs/assets/bench_tradeoff.png)

Activos generados con `make benchmarks`:
- `docs/assets/bench_results.csv`
- `docs/assets/bench_tradeoff.png`
- `docs/assets/kpi_table.md`

Activos generados con `make demo`:
- `docs/assets/demo_output.txt`

## Indra Package
- [onepager.md](docs/indra/onepager.md)
- [pitchdeck.md](docs/indra/pitchdeck.md)
- [techbrief.md](docs/indra/techbrief.md)
- [evidence_pack.md](docs/indra/evidence_pack.md)

## Repo map
- `ml/`: prototipos de compresión Tensor-Train (TT) y validación.
- `hw/README.md`: descripción de interfaces HW, layout de cores y plan de V&V.
- `hw/`: skeleton HW con `hls/` y `rtl/`.
- `sw/`: integración SW y drivers (placeholder).
- `scripts/`: demos, benchmarks y empaquetado Indra.
- `docs/indra/`: documentos ejecutivos para Indra.
- `docs/assets/`: salidas reproducibles y evidencias.

## Reproducibilidad y limitaciones
Los scripts fijan seeds y guardan outputs en `docs/assets`. No se versionan pesos grandes; se usan datos sintéticos reproducibles.

### Decisiones de diseño
- Separación SW/HW para aislar V&V y facilitar integración incremental.
- Interfaz HW/SW planificada con control AXI-Lite y flujo de datos por DMA/AXI.
- Evidencias versionadas: outputs deterministas y auditables en `docs/assets`.

### Limitaciones actuales
- No hay kernel HLS ni bitstream FPGA; el HW está en skeleton.
- Benchmarks actuales son CPU con NumPy; no representan rendimiento FPGA.
- No se incluyen pesos grandes ni datasets reales por tamaño o licencias.

## Contacto
[TU_EMAIL] | [TU_LINKEDIN]
