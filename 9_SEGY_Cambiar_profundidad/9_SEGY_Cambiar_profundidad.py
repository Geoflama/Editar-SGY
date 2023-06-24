# -*- coding: utf-8 -*-
"""
Creado por Sebastian Principi
24-06-2023 
Cambia la profundidad de un archivo segy
"""

# Variables a modificar
# --------------------------------------------------------------
# Directorio a analizar
path=r"D:\Sismicas_kingdom\prueba"

# Sismica a modificar
file=path+"\\"+"ycc02_110.sgy"

#Nueva longitud
NewTimeLength=5000

# --------------------------------------------------------------

# Inicio Script
# --------------------------------------------------------------
# 0. Importar librerias

import segyio
import shutil

# 1. Creo una copia del segy
file_copy=str(file)[:-4]+'_copy.sgy'

shutil.copyfile(file, file_copy)
        
# 2. Abrir el archivo como read write
with segyio.open(file_copy, "r+", ignore_geometry=True) as f:
    
    #A. Determino la cantidad de samples
    Samples=f.bin[segyio.BinField.Samples]
    
    #B. Calculo el nuevo sample interval
    New_SampleInterval = int(NewTimeLength*1000 / (Samples))
    
    #C. Asigno el nuevo sample interval al bin header
    f.bin[segyio.BinField.Interval]=New_SampleInterval
    
    
    # D. Loop para asignar el nuevo sample interval al trace header           
    for i in range(0,len(f.header)):
        f.header[i][segyio.TraceField.TRACE_SAMPLE_INTERVAL]=New_SampleInterval