"""Run the 18 VSPAERO simulations of the PC-7 MkII scale model automatically.

For every combination of outer-wing dihedral and airfoil thickness, the script:

1. creates one folder per model in ``OUTPUT_DIR``;
2. writes a modified copy of the base OpenVSP model (``BASE_VSP3``) and copies the
   VSPAERO settings (``VSPAERO_SETTINGS``);
3. runs CompGeom (mesh generation) through a .vspscript;
4. runs VSPAERO on each model, one after the other.

Then run ``extract_database.py OUTPUT_DIR`` to compile the results.

Requirements: OpenVSP 3.43.0 (Windows build used for the project) and its Python API
(``openvsp`` module), with the same Python version as the OpenVSP build.
Adapt the paths below (OUTPUT_DIR, OPENVSP_DIR) before running.
"""

import math
import os
import shutil
import subprocess
import time

import openvsp as vsp

# --- Paths to adapt --------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
# Base aircraft model
BASE_VSP3 = os.path.join(HERE, "..", "models", "PC7-MkII.vsp3")
# VSPAERO settings used for the project (Mach, alpha/beta sweep, reference values)
VSPAERO_SETTINGS = os.path.join(HERE, "origin.vspaero")
# Folder where one sub-folder per model is created
OUTPUT_DIR = r"C:\TM_Simulations\results"
# OpenVSP installation folder (contains vsp.exe and vspaero.exe)
OPENVSP_DIR = r"C:\OpenVSP-3.43.0-win64-Python3.9\OpenVSP-3.43.0-win64"

# --- Simulated configurations ---------------------------------------------
DIHEDRAL_ANGLES = [0, 5, 7, 10, 15, 20]   # outer-wing dihedral [deg]
THICKNESS_RATIOS = [0.10, 0.15, 0.20]     # thickness / chord
SPAN_EXT = 0.3762                          # outer-wing span [m]
CHORD = 0.188                              # chord used to normalise DeltaY [m]
OMP_THREADS = 10                           # CPU threads given to VSPAERO

LOG_FILE = os.path.join(os.path.abspath(OUTPUT_DIR), "simulations.log")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    printandwrite("[INFO] Lancement du script...")
    printandwrite("[INFO] Création des fichiers...")
    try:
        analysis_files = create_analysis_files()
    except Exception as e:
        printandwrite("[ERROR] Nous n'avons pas pu créer les fichiers d'analyse.")
        printandwrite(f"[ERROR] Détail : {e}")
        return
    printandwrite(f"[INFO] {len(analysis_files)} dossiers ont été créés.")
    printandwrite("[INFO] Génération des géométries...")
    compute_geometry(analysis_files)
    printandwrite("[INFO] Géométries calculées.")
    printandwrite("[INFO] Lancement des simulations")
    try:
        analyse(analysis_files)
    except subprocess.CalledProcessError as e:
        printandwrite(f"[ERROR] Il y a eu un problème pendant l'analyse : {e}")
        return
    printandwrite("[SUCCESS] Analyse terminée.")


def model_name(angle, thickness):
    # e.g. angle 10, thickness 0.15 -> "angle_10_TC_15"; 0.10 -> "TC_1"; 0.20 -> "TC_2"
    return f"angle_{angle}_TC_{thickness}".replace("0.", "")


def create_analysis_files():
    """Create one folder per model with its .vsp3 and .vspaero files."""
    analysis_files = []
    for angle in DIHEDRAL_ANGLES:
        for thickness in THICKNESS_RATIOS:
            name = model_name(angle, thickness)
            case_dir = os.path.join(OUTPUT_DIR, name)
            os.makedirs(case_dir, exist_ok=True)
            shutil.copyfile(VSPAERO_SETTINGS, os.path.join(case_dir, f"{name}_VSPGeom.vspaero"))

            vsp.ClearVSPModel()
            vsp.ReadVSPFile(BASE_VSP3)
            wing_id = vsp.FindGeom("Wing", 0)
            # Do not rotate the fuselage instead: VSPAERO computes in the XZ reference
            # plane, so rotating the aircraft breaks the physics. The flow angles
            # (alpha, beta) are set in the .vspaero file instead.
            dyc = math.tan(math.radians(angle)) * SPAN_EXT / CHORD
            vsp.SetParmVal(wing_id, "DeltaY", "XSecCurve_2", dyc)
            for section_index in [0, 1, 2]:
                vsp.SetParmVal(wing_id, "ThickChord", f"XSecCurve_{section_index}", thickness)
            vsp.Update()

            vsp.WriteVSPFile(os.path.join(case_dir, f"{name}.vsp3"), vsp.SET_ALL)
            analysis_files.append((case_dir, f"{name}_VSPGeom"))
            printandwrite(f"[INFO] Dossier créé : {name}")
    return analysis_files


def compute_geometry(analysis_files):
    """Run CompGeom on each model to create the files VSPAERO needs."""
    vsp_exe = os.path.join(OPENVSP_DIR, "vsp.exe")
    for case_dir, file in analysis_files:
        file_vsp3 = file.replace("_VSPGeom", ".vsp3")
        script_path = os.path.join(case_dir, "generate_geom.vspscript")
        with open(script_path, "w") as f:
            f.write(f'''// generate_geom.vspscript
void main()
{{
  ReadVSPFile("{file_vsp3}");

  // Run CompGeom to generate the geometry used by VSPAERO
  string compGeom = "VSPAEROComputeGeometry";
  SetAnalysisInputDefaults(compGeom);
  string compGeom_results = ExecAnalysis(compGeom);
}}
''')
        printandwrite(f"[INFO] Lancement de CompGeom pour {file}")
        result = subprocess.run([vsp_exe, "-script", script_path], cwd=case_dir)
        if result.returncode != 0:
            # vsp.exe often returns an error code even when the geometry is written
            printandwrite(f"[WARNING] vsp.exe a renvoyé le code {result.returncode} "
                          f"pour {file} (souvent sans conséquence, vérifier le dossier)")
        printandwrite(f"[SUCCESS] Terminé pour {file}")


def analyse(analysis_files):
    """Run VSPAERO on each model and print an estimate of the remaining time."""
    vspaero_exe = os.path.join(OPENVSP_DIR, "vspaero.exe")
    total = len(analysis_files)
    avg_time = 0
    for idx, (case_dir, file) in enumerate(analysis_files):
        start_time = time.time()
        printandwrite(f"[INFO] Lancement de VSPAERO pour {file}, fichier {idx + 1}/{total}")
        subprocess.run([vspaero_exe, "-omp", str(OMP_THREADS), "-dokt",
                        os.path.join(case_dir, file)], check=True, cwd=case_dir)
        elapsed = time.time() - start_time
        avg_time = (avg_time * idx + elapsed) / (idx + 1)
        remaining = (total - idx - 1) * avg_time
        printandwrite(f"[SUCCESS] Analyse terminée pour {file} en {elapsed:.1f} s")
        printandwrite(f"[INFO] Temps estimé restant : environ "
                      f"{int(remaining // 60)} min {int(remaining % 60)} s\n")


def printandwrite(msg):
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{msg}\n")


if __name__ == "__main__":
    main()
