# %% [markdown]
# IMPORTANT
# 
# ROIs should be saved as Staining Method_Genotype_Gender_Brain_Slide_Region (e.g., ThioS_hTauNLF_M_1116097_S1_HIP).
# 
# Make sure to set the right ilastik project directories for your computer.
# 
# Whenever ilastik is called, change project directory to whichever project you need for the brains you have (i.e., if you are quantifying NLGF brains, change 'NLF_Segmentation.ilp' to 'NLGF_Segmentation.ilp').
# %%
from pathlib import Path
import subprocess

#Folder containing ROIs and folder for Ilastik outputs.
in_folder = Path("E:\\260306_AxonaThioS_Tiffs\\Headless_Test_In")
out_folder = Path("E:\\260306_AxonaThioS_Tiffs\\Headless_Test_Out")

#Ilastik segmentation.
for in_file in in_folder.glob("*.tif"):
    out_file = out_folder / in_file.name.replace(".tif", "_Probabilities.h5")
    print(f"Processing {in_file} -> {out_file}")
    command = [
    "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\ilastik-1.4.2b6\\ilastik.lnk",
    '--headless',
    '--project=E:\\260306_AxonaThioS_Tiffs\\NLGF_Segmentation.ilp',
    '--output_format=hdf5',
    '--export_source=Probabilities',
    '--raw_data=' + str(in_file),
    '--output_filename_format=' + str(out_file)
]


    print("COMMAND=", "  ".join(command))

    process = subprocess.run(command, check = True)
# %%
#Percentage of coverage quantification
from pathlib import Path
import h5py
import pandas as pd
import numpy as np

h5_files = out_folder.glob("*_Probabilities.h5")

h5_dict = {}

for in_file in h5_files:
    filename = in_file.stem
    parts = filename.split("_")
    if len(parts) >= 6:
        staining_method = parts[0]
        genotype = parts[1]
        gender = parts[2]
        brain = parts[3]
        slide = parts[4]
        region = parts[5]

        print(f"Processing: {filename}")

        # Open HDF5 file
        with h5py.File(in_file, 'r') as f:
            # Prefer dataset named "Probabilities" if it exists
            if "Probabilities" in f.keys():
                dataset_name = "Probabilities"
            else:
                dataset_name = list(f.keys())[0]  # fallback to first dataset
            data = f[dataset_name][:]  # read entire dataset into a NumPy array

        # Compute percentage coverage (value 3 over 2+3)
        percentage_coverage = (np.count_nonzero(data == 3) /
                               (np.count_nonzero(data == 3) + np.count_nonzero(data == 2)) * 100)

        unique_key = f"{staining_method}_{genotype}_{gender}_{brain}_{region}"

        if unique_key not in h5_dict:
            h5_dict[unique_key] = {'slide': [], 'a': []}

        h5_dict[unique_key]['slide'].append(slide)
        h5_dict[unique_key]['a'].append(percentage_coverage)

# Write results to Excel
for key, value in h5_dict.items():
    slide = value['slide']
    a = value['a']
    total_percentage_coverage = sum(a) / len(a)
    a.append(total_percentage_coverage)
    slide.append("AVERAGE")
    b = key.replace("*", "_")

    e = zip(slide, a)

    df = pd.DataFrame(e, columns=["Slide", "Percentage Coverage"])

    output_filename = f"{b}_Percentage_Of_Coverage.xlsx"
    output_path = out_folder / output_filename

    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Percentage of Coverage', index=False)

    print(f"Saved Excel file: {output_filename}")

# %%
#Ilastik plaque classification
for in_file in in_folder.glob("*.tif"):
    out_file_1 = out_folder / in_file.name.replace(".tif", "_Object_Predictions.h5")
    out_file_2 = out_folder / in_file.name.replace(".tif", "_Table.csv")
    pred = out_folder / in_file.name.replace(".tif", "_Probabilities.h5")
    print(f"Processing {in_file} -> {out_file}")
    command = [
    "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\ilastik-1.4.2b6\\ilastik.lnk",
    '--headless',
    '--project=E:\\260306_AxonaThioS_Tiffs\\NLGF_Plaque_Classification.ilp',
    '--table_filename=' + str(out_file_2),
    '--output_format=hdf5',
    '--export_source=Object Predictions',
    '--raw_data=' + str(in_file),
    '--prediction_maps=' + str(pred),
    '--output_filename_format=' + str(out_file)
]


    print("COMMAND=", "  ".join(command))

    process = subprocess.run(command, check = True)
# %%
#Quantification of plaque classification
csv_files = out_folder.glob("*.csv")

csv_dict = {}

for in_file in csv_files:
    filename = in_file.stem
    parts = filename.split("_")

    if len(parts) >= 6:
        staining_method = parts[0]
        genotype = parts[1]
        gender = parts[2]
        brain = parts[3]
        slide = parts[4]
        region = parts[5]

        unique_key = f"{brain}_{region}"

        if unique_key not in csv_dict:
            csv_dict[unique_key] = {'data': []}

        read = pd.read_csv(in_file)
        csv_dict[unique_key]['data'].append(read)

for key, value in csv_dict.items():
    data = pd.concat(value['data'])
    c = data['Predicted Class'].value_counts(normalize=True) * 100

    class_dist_row = pd.DataFrame([c], columns=c.index)
    result = pd.concat([class_dist_row, data], ignore_index=True)

    output_filename = f"{key}_SML.xlsx"
    output_path = out_folder / output_filename

    writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
    result.to_excel(writer, sheet_name='SML', index=False)
    writer.close()