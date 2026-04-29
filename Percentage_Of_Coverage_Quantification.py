# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 14:24:01 2023

@author: Diego
"""
import numpy as np
import pandas as pd
from pathlib import Path

in_folder = Path("D://NLF_17_20_Ilastik_06_06//Simple Segmentation//")

a = []
b = []

brain = input("brain:")
region = input("region:")
path = "ThioS_" + brain + "*" + region + "_Simple Segmentation.npy"
print(path)


for in_file in in_folder.glob(path):
    data = np.load(str(in_file))
    percentage_coverage = ((np.count_nonzero(data == 3) / (np.count_nonzero(data == 3) + np.count_nonzero(data == 2) + np.count_nonzero(data == 4))) * 100)
    a.append(percentage_coverage)
    c = str(Path(in_file)).replace("D://NLF_17_20_Ilastik_06_06//Simple Segmentation//","")
    d = c.replace("_Simple Segmentation.npy","")
    b.append(d)
    
total_percentage_coverage = sum(a)/len(a)
a.append(total_percentage_coverage)
b.append("Average")
e = zip(b,a)

df = pd.DataFrame(e)

writer = pd.ExcelWriter("D://NLF_17_20_Ilastik_06_06//POC//" + brain + "_" + region + "_Percentage_Of_Coverage.xlsx", engine = 'xlsxwriter')           
df.to_excel(writer, sheet_name = 'Percentage of Coverage', index = False)
writer.close()

#ThioS_hTauNLF_M_1116530_S1_CTX_Simple Segmentation.npy