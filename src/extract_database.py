"""
Structure :
cases = {
    "alpha-beta": {
    "cl": [it1, it2, it3, ...],
    "cd": [it1, it2, it3, ...]
    }
}

"""

import os
import json

def extract_iterations(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    cases = {}
    for i, l in enumerate(lines):
        if l.startswith("AoA_"):
            a = l.split()[-2]
            b = lines[i+1].split()[-2]
            name = f"{a}/{b}"
            j = i
            while j < len(lines) and not lines[j].strip().startswith("Iter"):
                j += 1
            if j >= len(lines):
                continue
            h = lines[j].split()
            idx = {}
            for n, k in enumerate(h):
                idx[k] = n
            cases[name] = {"cl": [], "cd": [], "l/d": [], "cmx": [], "cmy": [], "cmz": []}
            for d in lines[j+1:]:
                p = d.split()
                try:
                    cases[name]["cl"].append(float(p[idx["CLtot"]]))
                    cases[name]["cd"].append(float(p[idx["CDtot"]]))
                    cases[name]["l/d"].append(float(p[idx["L/D"]]))
                    cases[name]["cmx"].append(float(p[idx["CMxtot"]]))
                    cases[name]["cmy"].append(float(p[idx["CMytot"]]))
                    cases[name]["cmz"].append(float(p[idx["CMztot"]]))
                except:
                    break
    return cases

def load_all_files(folders_path):
    dataset = {}
    for folder in os.listdir(folders_path):
        for filename in os.listdir(os.path.join(folders_path, folder)):
            if filename.endswith(".history"):
                filepath = os.path.join(os.path.join(folders_path, folder), filename)
                key = os.path.splitext(filename)[0]
                key = key.replace("_VSPGeom", "")
                dataset[key] = extract_iterations(filepath)
    return dataset

def save_in_json_file(dataset, output_file):
    with open(output_file, 'w') as f:
        json.dump(dataset, f, indent=2)

def main():
    dataset = load_all_files(r"C:\Users\arthur\OneDrive - Education Vaud\TM\TM_Simulations\results")
    print(f"{len(dataset)} fichiers traités")
    save_in_json_file(dataset, "database.json")

if __name__ == "__main__":
    main()