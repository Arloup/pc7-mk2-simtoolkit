# pc7-mk2-simtoolkit
From simulation to sky: building and flying a reduced PC-7 MkII.
# 🛩️ PC-7 MkII – Reduced Model & Aerodynamic Optimization

**Reduced-scale PC-7 MkII: from CFD simulations to 3D-printed flight.**

![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?logo=python&logoColor=white)
![3D Modeling](https://img.shields.io/badge/3D-Modeling-blue)
![CFD](https://img.shields.io/badge/CFD-Simulation-orange)


## 📖 Overview

This repository documents the aerodynamic modeling and reduced-scale construction of the **Pilatus PC-7 MkII**, a Swiss turboprop trainer aircraft.  
The project combines **3D modeling, numerical simulation, and empirical optimization** to design and build a functional **3D-printed flying model**.

Key elements include:
- ✈️ **3D aerodynamic modeling** with *OpenVSP* and *Fusion 360*.  
- 🔬 **Automated CFD simulations** for lift, drag, and moment analysis.  
- 🐍 **Python scripting** for simulation automation and data processing.  
- 🛠️ **3D printing & assembly** of a functional reduced-scale aircraft.  
- 🌍 **Open-source contribution** of all models, scripts, results, and construction plans.

## 🚀 Features

- Aerodynamic study of lift, drag, and moment coefficients (CL, CD, CM).  
- Exploration of Reynolds number effects on reduced-scale aircraft.  
- Automated pipeline for running CFD simulations with Python.  
- 3D-printable model adapted for radio-controlled flight.  
- Documentation of challenges, methods, and results.  

## 📂 Repository Structure
📦 pc7-mk2-sim-opt
┣ 📁 src/ # Python scripts for simulations & data analysis
┣ 📁 models/ # 3D CAD files (OpenVSP, Fusion 360, STL/STEP)
┣ 📁 simulations/ # CFD results and processed data
┣ 📁 docs/ # Diagrams, methodology notes, and references
┣ 📁 construction/ # 3D printing plans and assembly guides
┗ README.md


## 🖥️ Tools & Technologies

- **OpenVSP** → Parametric aircraft modeling and aerodynamic analysis  
- **Fusion 360** → 3D CAD for printable model design  
- **Python (NumPy, Matplotlib, Pandas)** → Automation & data processing  
- **3D Printing** → FDM with PLA filament  

---

## 📊 Results & Insights

- Achieved an optimized wing configuration for cruise efficiency.  
- Demonstrated correlation between simulated and theoretical aerodynamic behavior.  
- Highlighted limitations of reduced-scale models in Reynolds similarity.  
- Built and flight-tested a functional **RC model of the PC-7 MkII**.  

---

## 🛠️ How to Use

1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/pc7-mk2-sim-opt.git
   cd pc7-mk2-sim-opt
