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
    spec.sorting = src.sorting
    spec.format = src.format        # formato de datos (ej: IBM float, int, etc.)
    spec.samples = src.samples      # vector de tiempos/muestras
    spec.tracecount = src.tracecount

    #with segyio.create(archivo_salida, spec) as dst:
    with segyio.create(archivo_salida, spec) as dst:
        dst.text[0] = src.text[0]        # copiar encabezado EBCDIC
        dst.bin = src.bin                # copiar encabezado binario
        dst.header = src.header          # copiar definición de headers

        out_tr = 0
        for i, trace in enumerate(src.trace):
            # Leer el header del trace
            hdr = src.header[i]

            # Número de canal. Puede ser tracl (número absoluto de traza)
            # o tracf (número de canal dentro del gather)
            canal = hdr[segyio.TraceField.TRACF]

            # Copiar todas las trazas excepto canal 6 y 8
            if canal not in (6, 8):
                dst.trace[out_tr] = trace
                dst.header[out_tr] = hdr
                out_tr += 1
