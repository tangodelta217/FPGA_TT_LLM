# Diagrama de bloques HW

```mermaid
flowchart LR
    DMA[DMA] --> INBUF[Input Buffer]
    INBUF --> MAC[MAC Array]
    MAC --> ACC[Accumulator]
    ACC --> OUTBUF[Output Buffer]
```
