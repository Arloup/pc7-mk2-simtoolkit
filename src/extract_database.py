"""Compile the VSPAERO ``.history`` files of every case into one JSON database.

Structure of the output file::

    {
        "angle_10_TC_15": {               # model: dihedral 10 deg, thickness 15 %
            "-10.0000000/0.0000000": {    # case: "alpha/beta" in degrees
                "cl":  [it1, it2, ...],   # value at each solver iteration
                "cd":  [...],
                "l/d": [...],
                "cmx": [...], "cmy": [...], "cmz": [...]
            },
            ...
        },
        ...
    }

Usage::

    python extract_database.py <results_folder> [-o database.json]

``<results_folder>`` is the ``output_dir`` of ``simulations_main.py``
(one sub-folder per model).
"""

import argparse
import json
import os

HISTORY_SUFFIX = "_VSPGeom.history"


def extract_iterations(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    cases = {}
    for i, line in enumerate(lines):
        if not line.startswith("AoA_"):
            continue
        alpha = line.split()[-2]
        beta = lines[i + 1].split()[-2]
        name = f"{alpha}/{beta}"
        j = i
        while j < len(lines) and not lines[j].strip().startswith("Iter"):
            j += 1
        if j >= len(lines):
            continue
        header = lines[j].split()
        idx = {key: n for n, key in enumerate(header)}
        cases[name] = {"cl": [], "cd": [], "l/d": [], "cmx": [], "cmy": [], "cmz": []}
        for row in lines[j + 1:]:
            p = row.split()
            try:
                cases[name]["cl"].append(float(p[idx["CLtot"]]))
                cases[name]["cd"].append(float(p[idx["CDtot"]]))
                cases[name]["l/d"].append(float(p[idx["L/D"]]))
                cases[name]["cmx"].append(float(p[idx["CMxtot"]]))
                cases[name]["cmy"].append(float(p[idx["CMytot"]]))
                cases[name]["cmz"].append(float(p[idx["CMztot"]]))
            except (IndexError, ValueError):
                # End of the iteration table for this case
                break
    return cases


def load_all_files(results_path):
    dataset = {}
    for folder in sorted(os.listdir(results_path)):
        folder_path = os.path.join(results_path, folder)
        if not os.path.isdir(folder_path):
            continue
        for filename in os.listdir(folder_path):
            # Only the solver histories: skips logs such as output.history
            if filename.endswith(HISTORY_SUFFIX):
                key = filename[: -len(HISTORY_SUFFIX)]
                dataset[key] = extract_iterations(os.path.join(folder_path, filename))
    return dataset


def save_in_json_file(dataset, output_file):
    with open(output_file, "w") as f:
        json.dump(dataset, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("results_folder", help="folder containing one sub-folder per model")
    parser.add_argument("-o", "--output", default="database.json", help="output JSON file")
    args = parser.parse_args()

    dataset = load_all_files(args.results_folder)
    print(f"{len(dataset)} fichiers traités")
    save_in_json_file(dataset, args.output)


if __name__ == "__main__":
    main()
