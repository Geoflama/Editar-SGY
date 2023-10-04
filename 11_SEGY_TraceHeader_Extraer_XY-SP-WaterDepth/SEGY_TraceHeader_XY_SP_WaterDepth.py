# -*- coding: utf-8 -*-
"""
Extraer datos de los trace headers
Particularidades:
1. Lee todos los archivos de la carpeta definida en path
2. Lee las coordenas X, Y, SP, Water Depth Source.
3. Genera una tabla para cada archivo
Creado por Federico Esteban.
29-09-2023

"""

# Variables a modificar
# --------------------------------------------------------------
# Directorio a analizar
#path=r"C:\Users\usuario\Desktop\Nueva carpeta"
path=r"//media/federico/Elements/GEOFLAMA_BaseDatos/0_Datos/SEGY/YCM-/"
path=r"//media/federico/Elements/GEOFLAMA_BaseDatos/0_Datos/SEGY/YCM-/"
path=r"/media/federico/Elements/GEOFLAMA_BaseDatos/0_Datos/SEGY/YCM-40_FINAL-MIGRATION_ZERO-PHASE/"

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

            # C1. Leer los header de X e Y.
            sourceX = f.attributes(segyio.TraceField.SourceX)[:]/100
            sourceY = f.attributes(segyio.TraceField.SourceY)[:]/100

            # C2. Leer Numero SP (byte 17-20) y Water Depth at Source (bytes 61-64)
            SP = f.attributes(17)[:]
            WDS = f.attributes(61)[:]*-1
        
        # D. Convierto las listas de valores a un dataframe
        df = pd.DataFrame(list(zip(sourceX, sourceY, SP, WDS)),columns =['#X', 'Y', "SP", "WDS"])
        
        # E. Imprimir en la terminal
        #print(SP)
                
        # F. Guardo los datos como archivos de texto (uno por cada segy) en un CCSV
        df.to_csv(input_+".txt", index=False,sep=",")

    # Referencias
    """
    *1: Ver pp. 18 de Hagelund (2017). SEG-Y_r2.0
    Coordinate units:
    1 = Length (meters or feet as specified in Binary File Header bytes 3255-3256
    and in Extended Textual Header if Location Data are included in the file)
    2 = Seconds of arc (deprecated)
    3 = Decimal degrees (preferred degree representation)
    4 = Degrees, minutes, seconds (DMS)
    """
        
    """
    *2: Ver pp. 18 de Hagelund (2017). SEG-Y_r2.0
    Scalar = 1, ±10, ±100, ±1000, or ±10,000.
    If positive (negative), scalar is used as a multiplier (divisor).
    A value of zero is assumed to be a scalar value of 1.
    """