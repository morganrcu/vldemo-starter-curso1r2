# vldemo-starter — Starter de la Especialización Venturalítica

Proyecto de IA **mínimo y ejecutable** para recorrer el **Curso 1**: un clasificador de crédito con
un control de equidad que **falla** (V1, gate ROJO) y se **trata** versionando un commit en git
(V2, gate VERDE). Sin GPU ni datos reales: el reproducer es trivial y determinista.

Es material de demostración. La entidad (`Example Tutorial Corp`) es ficticia.

## Prerrequisitos

- Linux o WSL.
- Python 3 con `venv`.
- `git`.
- El binario `venth` instalado y en el `PATH` (ver el Curso 1, paso «Instala venth»).

## El arco en seis pasos

```bash
# 1. Clona y entra
git clone https://github.com/Venturalitica/vldemo-starter && cd vldemo-starter

# 2. Crea el entorno y mide (genera metrics.json segun params.yaml:seed)
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/dvc repro

# 3. Compila el contrato del gate (genera el plan OSCAL)
venth compile

# 4. Corre el gate -> ROJO (el control de equidad falla: 0.21 no es < 0.03). Sale != 0.
venth run

# 5. TRATA: bumpea la semilla y commitea (git cierra el bucle de tratamiento, ISO 23894 §6.5)
sed -i 's/seed: 1/seed: 2/' params.yaml
git commit -am "treat: bump seed 1->2 para cerrar el control de equidad"
.venv/bin/dvc repro

# 6. Corre el gate -> VERDE (0.01 < 0.03). Sale 0.
venth run
```

Tras el arco puedes proyectar la conformidad (`venth conformance`) y reconstruir el ciclo de vida
ISO 23894 por replay de git (`venth reconstruct`).

## Sigue el tutorial guiado

Recorre este repo paso a paso, por carriles (portal · desarrollador · responsable de
conformidad), en el **Curso 1** de la documentación:
<https://docs.venturalitica.ai/empezar/curso-1/>
