# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 15:40:33 2024

@author: usuario
"""

import os
import segyio
import pandas as pd
import glob

path = r"D:\Sismicas_kingdom\prueba"
path=r"/media/thor/Datos/SISMICA_3D/0_Datos_Ministerio/BDIH/Carina_1996/SGY/"
path=r"/media/thor/Datos/SISMICA_3D/0_Datos_Ministerio/BDIH/Ara-Argo-Aries_1994/SGY/"
os.chdir(path)

# Contador para ver avance del script
number_of_segy = len(glob.glob1(path, "*.sgy"))
count = 1

# Dataframe para almacenar los resultados
d = pd.DataFrame()

# Lista para almacenar las líneas erróneas
lineas_erroneas = []

for file in os.listdir(path):
    # Abro todos los .sgy de la carpeta
    if file.endswith(".sgy"):
        input_ = str(file)

        with segyio.open(input_, "r+", ignore_geometry=True) as f:
            # Obtener los nombres de los headers
            headers = segyio.tracefield.keys
            # Obtener los valores del primer trace
            first_trace_headers = {header: f.header[0][key] for header, key in headers.items()}
            
            # Crear un dataframe con los headers y valores del primer trace
            df_trace = pd.DataFrame([first_trace_headers], index=[input_])
            
            # Agregar el dataframe al dataframe principal
            d = pd.concat([d, df_trace])



# Mostrar el dataframe resultante
print(d)

d.to_csv("primera_traza.csv", index=False,sep=",")  

