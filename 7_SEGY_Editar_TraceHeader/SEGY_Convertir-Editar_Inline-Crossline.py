# -*- coding: utf-8 -*-
"""
Creado por Sebastian Principi y Federico Esteban
04-06-2024 
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
            
            # D. Leer los header de X e Y y convertirlo de segundos de arco a grados.
            #sourceX = f.attributes(185)[:]
            #sourceY = f.attributes(189)[:]
            
            # C. Loop para leer los datos
            for i in range(0,len(f.header)):
          
                print('Editando trace header',i)
                # C1. Leer datos de CDP
                CDP = f.attributes(21)[i]
                               
                # C2. Extraer numero de Inline
                inline = CDP // 10000
                
                # C3. Extraer numero de Crossline
                xline = CDP - inline * 10000
                #print ('inline: ', inline, 'crossline:', xline)
              
                # D. Escribir en los bytes 181 a 193
                # J1. Byte 181. CDP-X
                f.header[i][segyio.TraceField.CDP_X]=int(inline)
                # J2. Byte 1893. CDP-Y
                f.header[i][segyio.TraceField.CROSSLINE_3D]=int(xline)