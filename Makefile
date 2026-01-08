.PHONY: help setup lint test demo benchmarks indra-pack wow-audit

help:
	@echo "Targets:"
	@echo "  setup       Instala dependencias"
	@echo "  lint        Ejecuta ruff"
	@echo "  test        Ejecuta pytest"
	@echo "  demo        Genera evidencia funcional en docs/assets"
	@echo "  benchmarks  Ejecuta microbenchmarks CPU"
	@echo "  indra-pack  Empaqueta docs/indra y docs/assets"
	@echo "  wow-audit   Verifica evidencias minimas"

setup:
	python -m pip install -r requirements.txt

lint:
	python -m ruff check .

test:
	python -m pytest

demo:
	python -m scripts.demo_tt_linear

benchmarks:
	python -m scripts.run_benchmarks

indra-pack:
	python -m scripts.indra_pack

wow-audit:
	python -m scripts.wow_audit
