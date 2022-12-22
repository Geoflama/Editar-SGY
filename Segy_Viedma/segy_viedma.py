# -*- coding: utf-8 -*-
"""
Creado por Sebastian Principi y Federico Esteban
20-12-2022 
Copiar las coordenas en el SEGY desde un archivo txt
Los nuevos SEGY tienen el prefijo "UTM19_"
"""

# Variables a modificar
# --------------------------------------------------------------
# Directorio a analizar
path=r"C:\Users\usuario\Desktop\segy_viedma"

# Numero de canales usados en el relevamiento (monocanal = 1)
cant_canales=8      


# Inicio Script
# --------------------------------------------------------------
# 0. Importar librerias
import pandas
import segyio
import os
import shutil

# 1. Cambiar a la carpeta path
os.chdir(path)

# 2. Aplicar ciclo
for file in os.listdir(path):
    
    # A. Abro todos los .sgy de la carpeta
    if file.endswith(".sgy") and not file.startswith("UTM19_"):
        input_=str(file)

    # B. Crear una copia del archivo a modificar con el prefijo "output_"
        output_="UTM19_"+str(file)
        shutil.copyfile(input_, output_)
        filename=output_
        
        df = pandas.read_csv(input_[0:-4]+".txt", sep="\t", names=[ 'X', 'Y'])

        with segyio.open(output_, "r+", ignore_geometry=True) as f:

            FFID=f.attributes(segyio.TraceField.FieldRecord)[:]
            
            n_field_records=FFID[-1]-FFID[0]
            
            n=0
            i=0
            while n<len(f.header):
                print("i: ",i)
                for n in range(n,n+8):
                    print("n: ",n)
  
                    f.header[n][segyio.TraceField.SourceX]=int(df.X[i])
                    f.header[n][segyio.TraceField.SourceY]=int(df.Y[i])
                    
                i=i+1
                n=n+1