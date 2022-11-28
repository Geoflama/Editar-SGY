# -*- coding: utf-8 -*-
"""
Creado por Sebastian Principi y Federico Esteban
28-09-2022 
Extrae las coordendas de los shotpoints en segundos de arco 
y los guarda en un archivo csv unico como grados decimales
y con los datos del FFID (byte 9 del trace header).
"""

# Variables a modificar
# --------------------------------------------------------------
# Directorio a analizar
#path=r"C:\Users\usuario\Desktop\Nueva carpeta"
path=r"C:\Users\sebap\Downloads\sgy"

# Inicio Script
# --------------------------------------------------------------
# 0. Importar librerias
import os
import segyio
import pandas as pd

# 1. Cambiar al directorio path 
os.chdir(path)

# 2. Creo un dataframe en blanco con los nombres de las columnas
df = pd.DataFrame(columns =['#Long', 'Lat', "FFID","Name"])

# 3. Hacer un loop para cada archivo
for file in os.listdir(path):
    
    # A. Abir todos los .sgy de la carpeta.
    if file.endswith(".sgy"):
        input_=str(file)
        
        
        # B. Abrir el archivo como read write
        with segyio.open(input_, "r+", ignore_geometry=True) as f:
            
            # C. Leer los header de X e Y y los paso de segundos de arco a grados
            
            factor=3600000
            sourceX = f.attributes(segyio.TraceField.SourceX)[:]/factor
            sourceY = f.attributes(segyio.TraceField.SourceY)[:]/factor

            # D. Leer datos de FFID (byte 9)
            ffid = f.attributes(segyio.TraceField.FieldRecord)[:]
            
            # E. Creo la columna con el nombre del archivo
            name=[input_]*len(ffid)
    
            # F. Imprimir en la terminal
            print(sourceX)
            print(sourceY)
            print (ffid)

        # G. Convierto las listas de valores a un dataframe auxiliar
        df_aux = pd.DataFrame(list(zip(sourceX, sourceY, ffid,name)),columns =['#Long', 'Lat', "FFID","Name"])
        
        # H. Concateno el dataframe auxiliar con el que contiene los datos de los otros segy
        df = pd.concat([df,df_aux])
        
# F. Guardo los datos como archivos de texto (uno por cada segy) en un CCSV
df.to_csv(input_+".csv", index=False,sep=",")
