# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 11:42:01 2023

@author: Diego Caron
"""

import pandas as pd
from pathlib import Path

in_folder = Path("H://Demo//")

merged = []

brain = input("brain:")
region = input("region:")
path = "*" + brain + "*" + region + "*" + "_table.csv"
print(path)


for in_file in in_folder.glob(path):
        read = pd.read_csv(in_file)
        merged.append(read)

result = pd.concat(merged)

df = pd.DataFrame(result)

c = df['Predicted Class'].value_counts(normalize=True)*100

print(c)

a = result.append(c)

df2 = pd.DataFrame(a)

writer = pd.ExcelWriter("H://Demo_Output//" + brain + "_" + region + "_SML.xlsx", engine = 'xlsxwriter')           
df2.to_excel(writer, sheet_name = 'SML', index = False)
writer.close()