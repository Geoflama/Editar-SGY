# -*- coding: utf-8 -*-
"""
Creado por Sebastian Principi y Federico Esteban
28-09-2022 
Extrae las coordendas de los shotpoints y crea un tabla con los datos de navegacion
Particularidades:
1. Lee los bytes del trace header que dice tipo de coordenadas (bytes 89-90) y escalar (71-72).
2. Genera tabla con datos del Long, Lat, Nombre SEGY, FFID.
3. Genera una unica tabla
"""

# Variables a modificar
# --------------------------------------------------------------
# Directorio a analizar
#path=r"C:\Users\usuario\Desktop\Nueva carpeta"
path=r"/home/federico/Github/Geoflama/SEGY/0_DatosPrueba"

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

            # D. Leer los bytes con informacion de los trace header
            # Scalar to All Coordinates (byte 71-72)
            #SAC = f.attributes(segyio.TraceField.SAC)[:]
            SAC = f.attributes(71)[:]
            # if 0, then s x1, 1

            # Coordinates Units (byte 89-90) *1 
            CU = f.attributes(89)[:]
            # 1 : lenm/ft, 2: secarc, 3: decimal degrees, 4: DDMMSS

            # C. Leer los header de X e Y y los paso de segundos de arco a grados
            sourceX = f.attributes(segyio.TraceField.SourceX)[:]/36000000
            sourceY = f.attributes(segyio.TraceField.SourceY)[:]/36000000

            # Leer datos de FFID (byte 9)
            ffid = f.attributes(segyio.TraceField.FieldRecord)[:]
    
            # D. Imprimir en la terminal
            print(sourceX)
            print(sourceY)
            print (ffid)

        # E. Convierto las listas de valores a un dataframe
        df = pd.DataFrame(list(zip(sourceX, sourceY, ffid)),columns =['#Long', 'Lat', "FFID"])
        

        # F. Guardo los datos como archivos de texto (uno por cada segy) en un CCSV
        df.to_csv(input_+".csv", index=False,sep=",")


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