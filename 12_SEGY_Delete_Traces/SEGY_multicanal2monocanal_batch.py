# -*- coding: utf-8 -*-
"""
Creado por Federico Esteban
2025-128-18
Crear un archivo unicamante con un canal
Este SCRIPT procesa TODOS los archivos SEGY en una carpeta
"""
# --------------------------------------------------------------
# Variables a modificar
# --------------------------------------------------------------
# Directorio a analizar
path=r"/home/esteban82/Github/"
canal_objetivo = 3

# Importar librerías
# ------------------
import os
import segyio

# Cambiar al directorio de trabajo
# --------------------------------
os.chdir(path)

# Buscar archivos SEG-Y
# ---------------------
segy_files = sorted([
    f for f in os.listdir(path)
    if f.lower().endswith((".sgy", ".segy"))
])

if not segy_files:
    raise RuntimeError("No se encontraron archivos SEG-Y en el directorio")

# Procesar cada archivo
# ---------------------
for archivo_entrada in segy_files:

    base, ext = os.path.splitext(archivo_entrada)
    archivo_salida = f"{base}_canal{canal_objetivo}{ext}"

    print(f"Procesando: {archivo_entrada} → {archivo_salida}")

    with segyio.open(archivo_entrada, "r", ignore_geometry=True) as src:

        # Contar trazas del canal objetivo
        # --------------------------------
        n_traces = 0
        for i in range(src.tracecount):
            hdr = src.header[i]
            canal = hdr[segyio.TraceField.TraceNumber]
            if canal == canal_objetivo:
                n_traces += 1

        if n_traces == 0:
            print(f"  ⚠ No se encontraron trazas del canal {canal_objetivo}")
            continue

        # ------------------------------------------------------
        # Definir especificación de salida
        # ------------------------------------------------------
        spec = segyio.spec()
        spec.sorting    = src.sorting
        spec.format     = src.format
        spec.samples    = src.samples
        spec.tracecount = n_traces

        # ------------------------------------------------------
        # Crear archivo de salida
        # ------------------------------------------------------
        with segyio.create(archivo_salida, spec) as dst:
            dst.text[0] = src.text[0]
            dst.bin     = src.bin

            out_tr = 0
            for i, trace in enumerate(src.trace):
                hdr = src.header[i]
                canal = hdr[segyio.TraceField.TraceNumber]

                if canal == canal_objetivo:
                    dst.trace[out_tr]  = trace
                    dst.header[out_tr] = hdr
                    out_tr += 1

    print(f"  ✓ Trazas copiadas: {n_traces}\n")