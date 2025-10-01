# pc7-mk2-simtoolkit
From simulation to sky: building and flying a reduced PC-7 MkII.
# 🛩️ PC-7 MkII – Reduced Model & Aerodynamic Analysis

**Reduced-scale PC-7 MkII: from CFD simulations to 3D-printed flight.**

![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?logo=python&logoColor=white)
![3D Modeling](https://img.shields.io/badge/3D-Modeling-blue)
![CFD](https://img.shields.io/badge/CFD-Simulation-orange)

## 📖 Project Overview

This repository presents the entire process of modeling and building a reduced **Pilatus PC-7 MkII**, focusing on aerodynamic principle analysis and digital-to-physical realization.  
Central themes include rigorous **3D modeling, analytical and empirical simulation**, and the practical construction of a **3D-printed radio-controlled aircraft**.[1]

### Highlights
- **Aerodynamic geometry construction** with OpenVSP and Fusion 360, including manual profile extraction and parametric design.[1]
- **Automated CFD workflow** for exploring lift, drag, and moment behavior across 18 model and flight scenarios.[1]
- **Python-powered pipeline**: scripting simulation batches, extracting results, and generating comparative analysis automatically.[1]
- **Functional assembly**: print-optimized design accounting for both structure and electronics, tested in real conditions.[1]
- **Open-source sharing**: CAD models, simulation scripts, datasets, and build documentation provided for community contribution.[1]

## 🚀 Main Features

- In-depth evaluation of aerodynamic coefficients ($$C_L$$, $$C_D$$, $$C_M$$) for various configurations.[1]
- Analysis of Reynolds number and scale model effects (dynamic similarity and practical limitations).[1]
- Fully automated CFD case management with Python and vsppytools (batching, extraction, plotting).[1]
- 3D printing plans tailored for practical RC model flight and mechanical customization.[1]
- Clear walk-through of methods, technical difficulties, and empirical findings.[1]

## 📂 Repository Structure

```plaintext
📦 pc7-mk2-simtoolkit
┣ 📁 src/          # Simulation and analysis scripts (Python)
┣ 📁 models/       # CAD files (OpenVSP, Fusion360, STL/STEP)
┣ 📁 simulations/  # Raw results and post-processed datasets
┣ 📁 docs/         # Diagrams, methodology, references
┣ 📁 construction/ # 3D print plans and assembly guides
┗ README.md
```

## 🖥️ Software & Methods

- **OpenVSP**: Parametric airframe modeling, aerodynamic analysis, and mesh generation (VSPAERO).[1]
- **Fusion 360**: Surfacic and parametric CAD for print-ready models and compartment design.[1]
- **Python:** (NumPy, Matplotlib, Pandas, vsppytools) Automation of case setup, script-enabled result handling, batch post-processing.[1]
- **3D Printing:** FDM, PLA/LW-PLA, customized for minimal support and strong, lightweight assembly.[1]

***

## 📊 Simulation Results & Empirical Insights

- Determined optimal wing configuration balancing lift, drag, and stability for cruise scenario.[1]
- Validated simulated trends against aerodynamic theory; highlighted limitations of VSPAERO at this scale and practical discrepancies.[1]
- Documented the technical and empirical adjustments required for high-fidelity printing and robust RC flight (including electronics integration, assembly constraints, and in-flight feedback).[1]

***

## 🛠️ Getting Started

To reproduce or adapt the workflow:

1. Clone and set up the repository:
   ```bash
   git clone https://github.com/your-username/pc7-mk2-simtoolkit.git
   cd pc7-mk2-simtoolkit
   ```
2. Explore `src/` for Python automation scripts (simulations, data formatting, batch processing).[1]
3. Use CAD files in `models/` for custom geometry or print adaptation (Fusion 360, OpenVSP).[1]
4. Review `docs/` for methodological notes, empirical results, and references to theory and practical guides.[1]
5. Print and assemble using detailed plans in `construction/`, integrating recommended electronic components for RC flight.[1]

***

## Notes on Methodology and Contribution
The methodology follows an interdisciplinary approach—combining fluid mechanics, 3D design, programming, and hands-on manufacturing. Each step and challenge, from parametric modeling to batch simulation automation, is documented to support transparency and reproducibility.  
All models, scripts, datasets, and build notes are released for community improvement, error correction, and further empirical exploration.[1]

***

For more exhaustive principles, practical details, and full technical background, see `/docs` and the referenced report ("Travail de Maturité", 2025).

[1](/docs/tm.pdf)
