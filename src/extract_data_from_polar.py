"""Read VSPAERO ``.polar`` files (final results, one row per flow condition)."""

import os

import numpy as np

# Column name in the .polar file -> key in the returned dictionary
COLUMNS = {
    "AoA": "alpha",
    "CL": "cl",
    "CLtot": "cl",
    "CDtot": "cdtot",
    "L/D": "ld",
    "CMx": "cmx",
    "CMy": "cmy",
    "CMz": "cmz",
    "CMxtot": "cmx",
    "CMytot": "cmy",
    "CMztot": "cmz",
}


def extract_data_from_polar(file_name):
    """Return the columns of interest of a .polar file as float arrays."""
    with open(file_name) as f:
        lines = [line for line in f if line.strip()]

    keys = lines[0].split()
    data = {key: [] for key in keys}
    for line in lines[1:]:
        values = line.split()
        if len(values) != len(keys):
            continue
        for key, value in zip(keys, values):
            data[key].append(float(value))

    output = {}
    for key, name in COLUMNS.items():
        if key in data:
            output[name] = np.array(data[key])
    return output


def load_all_polar(folder_path):
    """Load every .polar file of a folder, keyed by model name."""
    dataset = {}
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".polar"):
            key = os.path.splitext(filename)[0].replace("_VSPGeom", "")
            dataset[key] = extract_data_from_polar(os.path.join(folder_path, filename))
    return dataset
