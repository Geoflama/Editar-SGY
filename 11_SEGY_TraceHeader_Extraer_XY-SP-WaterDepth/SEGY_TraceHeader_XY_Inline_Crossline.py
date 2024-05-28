# -*- coding: utf-8 -*-
"""
Extraer datos de los trace headers
Particularidades:
1. Lee todos los archivos de la carpeta definida en path
2. Lee las coordenas X, Y, Inline, Crossline
3. Genera un archivo (con extensión txt) para cada segy en la misma carpeta donde esta el archivo.
Creado por Federico Esteban.
28-05-2024

"""

# Variables a modificar
# --------------------------------------------------------------
# Directorio a analizar
#path=r"/media/thor/Datos/SISMICA_3D/0_Datos_Ministerio/BDIH/Ara-Argo-Aries_1994/SGY/"
path=r"/media/thor/Datos/SISMICA_3D/0_Datos_Ministerio/BDIH/CAM1-CAM3_2003/SGY/"
#path=r"/media/thor/Datos/SISMICA_3D/0_Datos_Ministerio/BDIH/Carina_1996/SGY/"
#path=r"/media/thor/Datos/SISMICA_3D/0_Datos_Ministerio/BDIH/Hidra-Kaus_1995/SGY/"
#path=r"/media/thor/Datos/SISMICA_3D/0_Datos_Ministerio/BDIH/Magallanes_1993/SGY/"
#path=r"/media/thor/Datos/SISMICA_3D/0_Datos_Ministerio/BDIH/Vega-Pleyade_1998/SGY/"

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

        # B. Imprimir en la terminal el nombre del archivo que se esta procesando
        nombre=input_.removesuffix('.sgy')               
        print(nombre)
        
        # C. Abrir el archivo como read write
        with segyio.open(input_, "r+", ignore_geometry=True) as f:

            # C1. Leer los header de X e Y.
            sourceX = f.attributes(segyio.TraceField.SourceX)[:]
            sourceY = f.attributes(segyio.TraceField.SourceY)[:]

            # C2. Leer Numero SP (byte 17-20) y Water Depth at Source (bytes 61-64)
            SCALE = f.attributes(71)[:]
            NS = f.attributes(115)[:]
            SI = f.attributes(117)[:]
            XCDP = f.attributes(181)[:]
            YCDP = f.attributes(185)[:]
            INLINE = f.attributes(189)[:]
            XLINE = f.attributes(193)[:]
        
        # D. Convierto las listas de valores a un dataframe
        df = pd.DataFrame(list(zip(sourceX, sourceY, SCALE, NS, SI, XCDP, YCDP, INLINE, XLINE)),columns =['#X', 'Y', "SCALE", "NS", "SI", "XCDP", "YCDP", "Inline", "Xline"])
        
        # E. Guardo los datos como archivos de texto (uno por cada segy) en un CCSV
        nombre=input_.removesuffix('.sgy')               
        df.to_csv(nombre+".txt", index=False,sep=",")
        

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