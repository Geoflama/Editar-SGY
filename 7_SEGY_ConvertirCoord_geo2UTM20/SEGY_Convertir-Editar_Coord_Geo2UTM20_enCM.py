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
path=r"/home/federico/Github/Geoflama/SEGY/0_DatosPrueba"
path=r"E:\Github\Geoflama\SEGY\0_DatosPrueba"

# Inicio Script
# --------------------------------------------------------------
# 0. Importar librerias
import os
import segyio
import shutil
from pyproj import Transformer

# 1. Cambiar a la carpeta path
os.chdir(path)

# 2. Aplicar ciclo
for file in os.listdir(path):

    # A. Abrir todos los *.sgy de la carpeta
    if file.endswith(".sgy") and not file.endswith('_UTM20.sgy'):
        input_=str(file)
        output_=str(file)[:-4]+'_UTM20.sgy'
        
        # B. Crear una copia del archivo a modificar con el prefijo "output_"
        shutil.copyfile(input_, output_)
        filename=output_
        
        # C. Abrir el archivo como read write
        with segyio.open(output_, "r+", ignore_geometry=True) as f:
            
            # D. Leer los header de X e Y y convertirlo de segundos de arco a grados.
            sourceX = f.attributes(segyio.TraceField.SourceX)[:]/100000
            sourceY = f.attributes(segyio.TraceField.SourceY)[:]/100000
            
            # E. Imprimir en la terminal
            print(sourceX)
            print(sourceY)

            # F. Loop para convertir datos de navegacion            
            for i in range(0,len(f.header)):
                # H. Convertir de lat/lon (epsg 4326) a UTM20s (32720)
                transformer = Transformer.from_crs(4326, 32720)
                points=[(sourceY[i], sourceX[i])]
                for pt in transformer.itransform(points):'{:.3f} {:.3f}'.format(*pt)
                
                # J. pt es el XY convertido, lo modifico por el original. 
                # Lo multiplico por M para tener precision centimetrica (tambien modifico byte 71, ver K.).
                f.header[i][segyio.TraceField.SourceX]=int(pt[0]*100)
                f.header[i][segyio.TraceField.SourceY]=int(pt[1]*100)

                # K. Escribir -100 en Byte 71 (que signifca que a los valores hay que dividirlos por 100) para obtener las coordenadas.
                f.header[i][segyio.TraceField.SourceGroupScalar]=-100
                
                # L. Escribir 1 (: coordendas planas) en Byte 89.
                f.header[i][segyio.TraceField.CoordinateUnits]=1
                