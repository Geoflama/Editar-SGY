# -*- coding: utf-8 -*-
"""
Creado por Sebastian Principi y Federico Esteban
06-01-2021 
Editar los bytes 71 y 89 de los Segy en UTM20S
"""

# Variables a modificar
# --------------------------------------------------------------
# Directorio a analizar
#path=r"E:\1.Meteor2009\M78a\M78-3a PS03\segy_unidos\Nueva carpeta"
path=r"D:\4_Segy_UTM"
#path=r"D:\Prueba"

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
                
                # E. Escribir 1 (: coordendas planas) en Byte 89.
                f.header[i][segyio.TraceField.CoordinateUnits]=1
                
                # F. Escribir 1 en Byte 71 (sin factor).
                f.header[i][segyio.TraceField.SourceGroupScalar]=1