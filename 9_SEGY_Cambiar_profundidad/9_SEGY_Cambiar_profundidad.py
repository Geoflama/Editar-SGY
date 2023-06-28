# -*- coding: utf-8 -*-
"""
Creado por Sebastian Principi
24-06-2023 
Cambia la profundidad de un archivo segy
"""

# --------------------------------------------------------------

# Inicio Script
# --------------------------------------------------------------
# 0. Importar librerias

import segyio
import shutil
from tkinter import filedialog as fd

#1. Elijo al segy 
input("Presione una tecla para elejir el segy a modificar")
file = fd.askopenfilename()

#2.Nueva longitud
print("Nueva profundidad en milisegundos: ")
NewTimeLength=int(input())

# 3. Creo una copia del segy
file_copy=str(file)[:-4]+'_copy.sgy'

shutil.copyfile(file, file_copy)
        
# 4. Abrir el archivo como read write
with segyio.open(file_copy, "r+", ignore_geometry=True) as f:
    
    #A. Determino la cantidad de samples
    Samples=f.bin[segyio.BinField.Samples]
    
    #B. Calculo el nuevo sample interval
    New_SampleInterval = int(NewTimeLength*1000 / (Samples-1))
    
    #C. Asigno el nuevo sample interval al bin header
    f.bin[segyio.BinField.Interval]=New_SampleInterval
    
    # D. Loop para asignar el nuevo sample interval al trace header           
    for i in range(0,len(f.header)):
        f.header[i][segyio.TraceField.TRACE_SAMPLE_INTERVAL]=New_SampleInterval