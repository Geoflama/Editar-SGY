# -*- coding: utf-8 -*-
"""
Creado por Sebastian Principi y Federico Esteban
28-09-2022 
Herramientas Unix: head, tail, while
Lee todos los segy de una carpeta y extrae sus coordenadas X e Y de 
los shotpoints y los guarda en un archivo csv.
"""

# Variables a modificar
# --------------------------------------------------------------
# Directorio a analizar
#path=r"C:\Users\usuario\Desktop\Nueva carpeta"
path=r"E:\m783b\0_DatosCrudos\1_SGY"


# Inicio Script
# --------------------------------------------------------------
# 0. Importar librerias
import os
import segyio
import pandas as pd

# 1. Cambiar al directorio path 
os.chdir(path)

# 2. Hacer un loop para cada archivo
for file in os.listdir(path):
    
    # A. Abir todos los .sgy de la carpeta.
    if file.endswith(".sgy"):
        input_=str(file)
        
        # B. Abrir el archivo como read write
        with segyio.open(input_, "r+", ignore_geometry=True) as f:
            
            # C. Leer los header de X e Y y los paso de segundos de arco a grados
            sourceX = f.attributes(segyio.TraceField.SourceX)[:]
            sourceY = f.attributes(segyio.TraceField.SourceY)[:]
            
            # D. Imprimir en la terminal? los valores.
            print(sourceX)
            print(sourceY)

# ????
df = pd.DataFrame(list(zip(sourceX, sourceY)),
               columns =['X', 'Y'])

# Crear csv ??
df.to_csv(input_+".csv", index=False,sep=",")  
df.to_csv(input_+".txt", index=False,sep=",") 
