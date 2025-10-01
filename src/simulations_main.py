import openvsp as vsp
import os
import math
import shutil
import subprocess
import time

origin_vsp3 = "test.vsp3"
output_dir = r"C:\TM_Simulations\results"
delta_yc_values = [0, 5, 7, 10, 15, 20]
Span_ext = 0.3762
Chord = 0.188
thickoverchord = [0.10, 0.15, 0.20]
analysis_file = []

os.makedirs(output_dir, exist_ok=True)
initial_dir = os.getcwd()

def main():
    printandwrite("[INFO]Lancement du script...")
    printandwrite("[INFO]Création des fichiers...")
    try:
        create_analysis_files()
    except Exception as e:
        printandwrite("[ERROR]Nous n'avons pas pu créer les fichiers d'analyse.")
        printandwrite(f"[ERROR]Détail : {e}")
        return
    printandwrite(f"[INFO]{len(analysis_file)} fichiers ont été créés.")
    printandwrite("[INFO]Copie des fichiers de paramétrages des simulations réussis.")
    printandwrite(" [INFO]Génération des géométries...")
    compute_geometry(analysis_file)
    os.chdir(r"C:\TM_Simulations")
    printandwrite("[INFO]Gemoétrie computée.")
    printandwrite("[INFO]Lancement des simulations")
    try:
        analyse(analysis_file)
    except Exception as e:
        printandwrite(f"[ERROR]Il y a eu un problème pendant l'analyse : {e}")
        return
    printandwrite("[SUCCESS]Analyse terminée.")


def create_analysis_files():
    for angle in delta_yc_values:
        for TC in thickoverchord:
            combo_name = f"angle_{angle}_TC_{TC}"
            combo_name = combo_name.replace("0.", "")
            case_dir = os.path.join(output_dir, combo_name)
            os.makedirs(case_dir, exist_ok=True)
            copy_vspaero_settings(case_dir, f"{combo_name}_VSPGeom")

            vsp.ClearVSPModel()
            vsp.ReadVSPFile(origin_vsp3)

            wing_id = vsp.FindGeom("Wing", 0)
            #fuse_id = vsp.FindGeom("Fuselage", 0) A ne pas faire car VSPAERO calcul selon le plan référence XZ et si on tourne l'avion la physique se casse
            #vsp.SetParmVal(fuse_id, "X_Rel_Rotation", "XForm", theta)
            dyc = math.tan(math.radians(angle)) * Span_ext / Chord
            vsp.SetParmVal(wing_id, "DeltaY", "XSecCurve_2", dyc)
            
            for section_index in [0, 1, 2]:
                vsp.SetParmVal(wing_id, "ThickChord", f"XSecCurve_{section_index}", TC)

            vsp.Update()
            new_vsp3 = os.path.join(case_dir, f"{combo_name}.vsp3")
            analysis_file.append((case_dir, f"{combo_name}_VSPGeom"))
            vsp.WriteVSPFile(new_vsp3, vsp.SET_ALL)
            printandwrite("[INFO]1 dossier créé")
        
def copy_vspaero_settings(dir, file):
    src = "origin.vspaero"
    dir_dst = os.path.join(dir, file)
    dir_dst += ".vspaero"
    shutil.copyfile(src, dir_dst)
    
def compute_geometry(list_dir):
    for dir, file in list_dir:
        src = "generate_geom.vspscript"
        dir_dst = os.path.join(dir, src)
        shutil.copyfile(src, dir_dst)
        file_vsp3 = file.replace("_VSPGeom", ".vsp3")
        vspscript_content = f'''// generate_geom.vspscript
void main()
{{
  ReadVSPFile("{file_vsp3}");

  // Run CompGeom to generate geometry
  string compGeom = "VSPAEROComputeGeometry";
  SetAnalysisInputDefaults(compGeom);
  string compGeom_results = ExecAnalysis(compGeom);
}}
'''
        with open(dir_dst, "w") as f:
            f.write(vspscript_content)
        printandwrite(f"[INFO] Lancement de Compute Geométry pour {file}")
        cmd = rf"C:\OpenVSP-3.43.0-win64-Python3.9\OpenVSP-3.43.0-win64\vsp.exe -script {dir_dst}"
        try:
            os.chdir(dir)
            subprocess.run(cmd, check=True)
        except:
            printandwrite("Il dit que c'est une erreur mais non let's go...")
        printandwrite(f"[SUCCESS] Terminé pour {file}")

def analyse(list_dir):
    total = len(list_dir)
    avg_time = 0
    for idx, (dir, file) in enumerate(list_dir):
        start_time = time.time()
        printandwrite(f"[INFO] Lancement de VSPAERO pour {file}, file {idx+1} / {total}")
        cmd = rf"C:\OpenVSP-3.43.0-win64-Python3.9\OpenVSP-3.43.0-win64\vspaero.exe -omp 10 -dokt {os.path.join(dir, file)}"
        subprocess.run(cmd, check=True, cwd=dir)
        elapsed = time.time() - start_time
        avg_time = elapsed if idx == 0 else (avg_time * idx + elapsed) / (idx + 1)
        remaining = (total - idx - 1) * avg_time

        printandwrite(f"[SUCCESS] Analyse terminée pour {file} en {elapsed:.1f} s")
        printandwrite(f"[INFO] Temps estimé restant : environ {int(remaining // 60)} min {int(remaining % 60)} s\n")
        printandwrite(f"[SUCCESS] Analyse terminé pour {file}, file {idx+1} / {len(list_dir)}")

def printandwrite(msg):
    print(msg)
    with open("output.history", "a", encoding="utf-8") as f:
        f.write(f"{msg}\n")
main()