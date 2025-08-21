# -*- coding: utf-8 -*-
"""
Creado por Federico Esteban
21-08-2025
Crear un archivo borrando los traces de los canales 6 y 8
"""

# Variables a modificar
# --------------------------------------------------------------
# Directorio a analizar
path=r"/home/esteban82/Dropbox/Facu/Patagonia_2025/2_Sismicas_con_Coordenadas/"
archivo_entrada = "UTM19_91816.sgy"
archivo_salida = "UTM19_91816_remove.sgy"

# 0. Importar librerias
import os
import segyio

# 1. Cambiar a la carpeta path
os.chdir(path)

# Abrir el archivo en modo lectura
with segyio.open(archivo_entrada, "r", ignore_geometry=True) as src:
    #spec = segyio.spec(archivo_entrada)   # copiar especificaciones (muestras, formato, etc.)
    spec = segyio.spec()   # copiar especificaciones (muestras, formato, etc.)
    with segyio.open(path) as src:
        spec = segyio.spec()
        spec.sorting = src.sorting
        spec.format = src.format
        spec.samples = src.samples[:len(src.samples)]
        spec.ilines = src.ilines
        spec.xline = src.xlines
        with segyio.create("/home/esteban82/Dropbox/Facu/Patagonia_2025/2_Sismicas_con_Coordenadas/nuevo/", spec) as dst:
            dst.text[0] = src.text[0]
            dst.bin = src.bin
            # this is writing a sparse file, which might be slow on some
            # systems
            dst.header = src.header
            dst.trace = src.trace
