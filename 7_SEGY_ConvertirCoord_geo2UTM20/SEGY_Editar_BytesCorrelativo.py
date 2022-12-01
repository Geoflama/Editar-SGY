# -*- coding: utf-8 -*-
"""
Creado por Sebastian Principi y Federico Esteban
06-01-2021 
Editar los bytes 71 y 89 de los Segy en UTM20S
"""

# Directorio a analizar
path=r"D:\M783a\Prueba"



# Inicio Script
# --------------------------------------------------------------
# 0. Importar librerias
import os
import segyio

# 1. Cambiar a la carpeta path
os.chdir(path)

# 2. Aplicar ciclo

for file in os.listdir(path):

    # A. Abrir todos los *.sgy de la carpeta
    if file.endswith(".sgy"):
        input_=str(file)

        # C. Abrir el archivo como read write
        with segyio.open(input_, "r+", ignore_geometry=True) as f:

            # D. Loop para convertir datos de navegacion            
            for i in range(0,len(f.header)):
                
                # E. Numerar (desde 1) los bytes 09 (FFID), 17 (SP) y 21 (CDP).
                f.header[i][segyio.TraceField.FieldRecord]=i+1
                f.header[i][segyio.TraceField.EnergySourcePoint]=i+1
                f.header[i][segyio.TraceField.CDP]=i+1
                
                
