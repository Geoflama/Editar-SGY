# Extraer un subconjunto de trazas de un archivo SEG-Y
# Creado por Federico D. Esteban
# 2022-11-23.

# Datos de Entrada
# --------------------------------------------------------------
# Archivo SEG-Y
in=test.sgy

# Nombre del archivo de salida
out=001.sgy

# Traza inicial y final del archivo de salida
TraceI=1
TraceF=200

# 1. Extraer informacion del Bin Header y realizar calculos
# -----------------------------------------------------------------------------
# 1A. Extraer Numero de Muestras (NS) por traza (bytes 21-22)
NS=$(dd if=$in bs=2 count=1 skip=3220 iflag=skip_bytes status=none | gmt convert -bi1h+b)

# 1B. Extraer Codigo de Data Sample Format (bytes 25-26) 
SF=$(dd if=$in bs=2 count=1 skip=3224 iflag=skip_bytes status=none | gmt convert -bi1h+b)

# Indexed arrays (lista de bytes para Data Sample Format code según Tabla 2 de SEG-Y_r2.0 Hagelund (2017)
SFC=(0 4 4 2 4 4 8 3 1 8 4 2 8 0 0 3 1)
Bytes=${SFC[$SF]}

# 1C. Realizar calculos para saber que bytes hay que extraer
NT=$(($TraceF-$TraceI+1))	    # Cantidad de Trazas
BT=$(($NS*$Bytes+240))	        # Cantidad de Bytes por Traza (encabezado + header)
BTI=$(($BT*($TraceI-1)+3600))   # Numero de byte de la traza inicial

# 2. Crear el nuevo Segy
# -----------------------------------------------------------------------------
# 1. Copiar Header (son siempre los primeros 3600 bytes)
dd if=$in bs=3600 count=1 > $out

# 2. Agregar datos de las trazas
dd if=$in skip=$BTI iflag=skip_bytes bs=$BT count=$NT >> $out
