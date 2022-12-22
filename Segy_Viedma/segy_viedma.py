# -*- coding: utf-8 -*-
"""
Objetivo: 
Copiar las coordenas en el SEGY desde un archivo txt
Los nuevos SEGY tienen el prefijo "UTM19_"

Autores: 
Codigo por Sebastian Principi
Comentarios por Federico Esteban
20-12-2022
"""

# Variables a modificar
# --------------------------------------------------------------
# Directorio a analizar
path=r"C:\Users\usuario\Desktop\segy_viedma"
path=r"C:\Users\esteb\OneDrive\Desktop\Viedma_2022\429"

# Archivo Navegacion
NAV="429_utm_ffid.txt"

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
        
        # C. Leer archivo csv que los campos estan separados por tabulaciones
        #df = pandas.read_csv(input_[0:-4]+".txt", sep="\t", names=[ 'X', 'Y'])
        #df = pandas.read_csv(input_[0:-4]+".txt", sep="\t", names=[ 'FFID', 'X', 'Y'])
        df = pandas.read_csv(NAV, sep="\t", names=[ 'FFID', 'X', 'Y'])

        # D. Usar segyio para crear el archivo output, 
        with segyio.open(output_, "r+", ignore_geometry=True) as f:

            # Definir FFID
            FFID=f.attributes(segyio.TraceField.FieldRecord)[:]
            
            # Definir numero de registros
            n_field_records=FFID[-1]-FFID[0]
            
            # Definir n, i
            n=0
            i=0
            
            # Ciclo.
            while n<len(f.header):
                print("i: ",i)
                #for n in range(n,n+8):
                for n in range(n,n+cant_canales):
                    print("n: ",n)

                    # Copiar los valores X e Y (del datraframe) 
                    f.header[n][segyio.TraceField.SourceX]=int(df.X[i])
                    f.header[n][segyio.TraceField.SourceY]=int(df.Y[i])
                
                # Redefinir n e i sumando 1.
                i=i+1
                n=n+1