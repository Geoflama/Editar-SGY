# -*- coding: utf-8 -*-
"""
Creado por Sebastian Principi y Federico Esteban
06-01-2021 
Crear SEGY pero con coordenadas en UTM20S. 
Los nuevos SEGY tienen el sufijo "_UTM20"
"""

# Variables a modificar
# --------------------------------------------------------------
# Directorio a analizar
path=r"E:\1.Meteor2009\M78a\M78-3a PS03\segy_unidos\Nueva carpeta"
path=r"/media/thor/Datos/SISMICA_3D/0_Datos_Ministerio/BDIH/Carina_1996/"
#path=r"/home/thor/Github/Geoflama/Editar-SGY/0_DatosPrueba/"

# Inicio Script
# --------------------------------------------------------------
# 0. Importar librerias
import os
import segyio
import shutil

# 1. Cambiar a la carpeta path
os.chdir(path)

# 2. Aplicar ciclo
for file in os.listdir(path):

    # A. Abrir todos los *.sgy de la carpeta
    if file.endswith(".sgy"):
        input_=str(file)
        
        # B. Abrir el archivo como read write
        with segyio.open(input_, "r+", ignore_geometry=True) as f:
            
            # D. Leer Numero compuesto (byte 21)
            #CDP = f.attributes(21)[:]
            #print(CDP)
            
            # D. Leer los header de X e Y y convertirlo de segundos de arco a grados.
            #sourceX = f.attributes(segyio.TraceField.SourceX)[:]/100000
            #sourceY = f.attributes(segyio.TraceField.SourceY)[:]/100000
            
            # E. Imprimir en la terminal
            #print(sourceX)
            #print(sourceY)

            # F. Loop para leer los datos
            for i in range(0,len(f.header)):
          
                # F1. Leer datos de CDP
                CDP = f.attributes(21)[i]
                               
                # F2. Extraer numero de Inline
                inline = CDP // 10000
                #print (inline)
                
                # F3. Extraer numero de Crossline
                xline = CDP - inline * 10000
                #print ('inline: ', inline, 'crossline:', xline)

                # Strings
                #CDP = str(f.attributes(21)[i])
                # Extrear crossline. Son los 4 últimos numeros del CDP
                #xline = CDP [-5:-1]
                #print(xline)
                
                # Extraer inline. Son los 4 primeros números del CDP
                #inline = CDP [:4]
                #print(inline)
                
                # H. Convertir de lat/lon (epsg 4326) a UTM20s (32720)
            #    transformer = Transformer.from_crs(4326, 32720)
            #    points=[(sourceY[i], sourceX[i])]
            #    for pt in transformer.itransform(points):'{:.3f} {:.3f}'.format(*pt)
                
                # J. pt es el XY convertido, lo modifico por el original
            #    f.header[i][segyio.TraceField.SourceX]=int(pt[0])
            #    f.header[i][segyio.TraceField.SourceY]=int(pt[1])

                # K. Escribir 1 (: coordendas planas) en Byte 89.
            #    f.header[i][segyio.TraceField.CoordinateUnits]=1
                
                # K. Escribir 1 en Byte 71 (sin factor).
            #    f.header[i][segyio.TraceField.SourceGroupScalar]=1