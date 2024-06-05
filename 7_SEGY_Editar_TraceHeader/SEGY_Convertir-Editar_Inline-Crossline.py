# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 09:55:24 2024

@author: Sebastian Principi
"""

# Variables a modificar
# --------------------------------------------------------------
# Directorio a analizar
path = r"/media/thor/Elements/SISMICA_3D/0_Datos_Ministerio/BDIH/Carina_1996/SGY_BackUp/"

# Inicio Script
# --------------------------------------------------------------
# 0. Importar librerias
import os
import segyio
import pandas as pd

# 1. Cambiar a la carpeta path
os.chdir(path)

# 2. Aplicar ciclo
for file in os.listdir(path):
    # A. Abrir todos los *.sgy de la carpeta
    if file.endswith(".sgy"):
        input_ = str(file)
        
        # B. Abrir el archivo como read write
        with segyio.open(input_, "r+", ignore_geometry=True) as f:

            # E. Modificar los valores de los headers
            for i in range(len(f.header)):
                # C0. Texto de la traza que se esta editando
                print('Editando trace header', i)
                
                # C1. Leer datos de CDP
                CDP = f.header[i][21]
                inline = CDP // 10000
                xline = CDP - inline * 10000
                
                # C3. Escribir en los nuevos bytes
                f.header[i][181] = f.header[i][185]
                f.header[i][185] = f.header[i][189]
                f.header[i][189] = inline
                f.header[i][193] = xline