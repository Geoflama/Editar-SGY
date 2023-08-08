# -*- coding: utf-8 -*-
"""
Creado por Sebastian Principi y Federico Esteban
28-09-2022 
Crea una tabla con datos de Traza, cantidad de datos y sample interval.
GENERA UN CSV POR CADA SEGY
"""

# Variables a modificar
# --------------------------------------------------------------
# Directorio a analizar
#path=r"C:\Users\usuario\Desktop\Nueva carpeta"
#path=r"D:\M783a\4_Segy_UTM"
#path=r"/media/federico/geomapapp1/m783b/2_UnirSegy_SGY_UTM"
path=r"E:/Sismicas_LUANA/0_Originales"
#path=r"D:\M783a\Prueba"

# Inicio Script
# --------------------------------------------------------------
# 0. Importar librerias
import os
import segyio
import pandas as pd
import numpy as np

# 1. Cambiar al directorio path 
os.chdir(path)

# 2. Hacer un loop para cada archivo
for file in os.listdir(path):
    
    # A. Abir todos los .sgy de la carpeta.
    if file.endswith(".sgy"):
        input_=str(file)
        
        # B. Abrir el archivo como read write
        with segyio.open(input_, "r+", ignore_geometry=True) as f:
            
            # C1. Leer los header de X e Y.
            sample_count = f.attributes(115)[:]
            sample_interval = f.attributes(117)[:]

            # C2. Leer otros bytes
            CDP = f.attributes(21)[:]

        # D. Convierto las listas de valores a un dataframe
        df = pd.DataFrame(list(zip(CDP, sample_count, sample_interval )),columns =['#CDP', 'X', 'Y'])
        
        # E. Guardo los datos como archivos de texto (uno por cada segy) en un CSV
        df.to_csv(input_+".csv", index=False,sep=",")