#!/usr/bin/env python3
"""Reproducer TRIVIAL del starter del tutorial.

NO entrena ni carga datos: emite un `metrics.json` plano cuyo valor depende de
`params.yaml:seed`. Es el mecanismo MÁS BARATO para que el motor MIDA un control
(`venth run`) sin GPU/dataset, de modo que `venth reconstruct` pueda derivar el ciclo
ISO 23894 (requiere >=1 control medido con `risk_id`). Material de demostración.

Contrato: `metrics.json` es un objeto plano `{ <id-de-la-medida>: <valor> }` — la CLAVE
es el `id` de la medida en venth.yaml, NO el campo `metric:`.

Arco del tutorial (diferencia de paridad demográfica del control de equidad):
  seed=1 -> 0.21  (ROJO: 0.21 no es < 0.03 -> el control bloqueante falla, gate rojo)
  seed=2 -> 0.01  (VERDE: 0.01 < 0.03 -> el control pasa, gate verde)
Bumpear `seed` mueve la staleness del modelo -> `venth run` re-mide en V2.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

# Diferencia de paridad demográfica por semilla. Determinista: el tutorial necesita un
# arco rojo->verde reproducible, no aleatoriedad.
DEMOGRAPHIC_PARITY_DIFF_BY_SEED = {
    1: 0.21,  # V1 sin mitigar — el control de equidad falla
    2: 0.01,  # V2 mitigado — el control de equidad pasa
}


def main() -> None:
    params = yaml.safe_load(Path("params.yaml").read_text(encoding="utf-8")) or {}
    seed = int(params.get("seed", 1))
    dp_diff = DEMOGRAPHIC_PARITY_DIFF_BY_SEED.get(seed, 0.21)

    # La clave DEBE ser el `id` de la medida (`unfair-credit-exclusion`), no su `metric:`.
    # Forma "WithPower": además del valor, un intervalo de confianza determinista
    # (semilla+B fijos). Cubre la clausula prEN 18228 §8.1 (evidencia `power_stats` presente).
    # El IC es ficticio pero coherente (estrecho, n grande) — material de demostración.
    metrics = {
        "unfair-credit-exclusion": {
            "value": dp_diff,
            "power": {
                "n": 1000,
                "ci_low": round(max(0.0, dp_diff - 0.005), 4),
                "ci_high": round(dp_diff + 0.005, 4),
                "ci_level": 0.95,
                "method": "bootstrap",
                "n_boot": 1000,
                "seed": seed,
            },
        }
    }
    Path("metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
