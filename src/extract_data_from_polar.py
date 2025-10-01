import numpy as np
import os

def extract_data_from_polar(file_name):
    with open(file_name) as f:
        lines = f.readlines()

    data = {}
    for idx, line in enumerate(lines):
        if idx == 0:
            keys = line.split()
            for key in keys:
                data[key] = []
            break
        values = line.split()
        for id, value in enumerate(values):
            data[keys[id]].append(value)
    output = {}
    for key in data:
        if key == "AoA":
            output["alpha"] = np.array(data[key])
        if key == "CL":
            output["cl"] = np.array(data[key])
        if key == "CDtot":
            output["cdtot"] = np.array(data[key])
        if key == "L/D":
            output["ld"] = np.array(data[key])
        if key == "CMy":
            output["cmy"] = np.array(data[key])
        if key == "CMx":
            output["cmx"] = np.array(data[key])
        if key == "CMz":
            output["cmz"] = np.array(data[key])
    return output

def load_all_polar(folder_path):
    dataset = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".polar"):
            filepath = os.path.join(folder_path, filename)
            key = os.path.splitext(filename)[0]
            key = key.replace("_VSPGeom", "")
            dataset[key] = extract_data_from_polar(filepath)
    return dataset
