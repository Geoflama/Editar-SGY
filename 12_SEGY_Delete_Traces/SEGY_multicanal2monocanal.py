# -*- coding: utf-8 -*-
"""
Creado por Federico Esteban
2025-128-18
Crear un archivo unicamante con un canal
Este SCRIPT procesa un unico archivo SEGY en una carpeta
"""

# Variables a modificar
# --------------------------------------------------------------
# Directorio a analizar
path=r"/home/esteban82/Github/"
archivo_entrada = "UTM19_40662.sgy"
archivo_salida = "UTM19_40662_canal3.sgy"
canal_objetivo = 3

# 0. Importar librerias
import os
import segyio

# 1. Cambiar a la carpeta path
os.chdir(path)

# Abrir el archivo en modo lectura
with segyio.open(archivo_entrada, "r", ignore_geometry=True) as src:

    # ----------------------------------------------------------
    # Contar cuántas trazas corresponden al canal 3
    # ----------------------------------------------------------
    n_traces_canal3 = 0
    for i in range(src.tracecount):
        hdr = src.header[i]
        canal = hdr[segyio.TraceField.TraceNumber]
        if canal == 3:
            n_traces_canal3 += 1

    # ----------------------------------------------------------
    # Definir especificación del archivo de salida
    # ----------------------------------------------------------
    spec = segyio.spec()                # copiar especificaciones (muestras, formato, etc.)
    spec.sorting    = src.sorting
    spec.format     = src.format        # formato de datos (ej: IBM float, int, etc.)
    spec.samples    = src.samples       # vector de tiempos/muestras
    spec.tracecount = src.tracecount

    #with segyio.create(archivo_salida, spec) as dst:
    with segyio.create(archivo_salida, spec) as dst:
        dst.text[0] = src.text[0]        # copiar encabezado EBCDIC
        dst.bin = src.bin                # copiar encabezado binario
        #dst.header = src.header          # copiar definición de headers

        out_tr = 0
        for i, trace in enumerate(src.trace):
            # Leer el header del trace
            hdr = src.header[i]
            canal = hdr[segyio.TraceField.TraceNumber]

            # Copiar SOLO canal 3
            if canal == canal_objetivo:
                dst.trace[out_tr] = trace
                dst.header[out_tr] = hdr
                out_tr += 1
