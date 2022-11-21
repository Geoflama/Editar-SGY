# Extraer solamente los datos de una traza de un archivo SGY
# Creado por Federico D. Esteban
# 2022-11-20
# Herramientas: dd (unix) y GMT

# Datos de Entrada
# --------------------------------------------------------------
# Archivo SEGY
in=test.sgy

# Archivo de Salida
out=Trace.txt

# Numero de traza a extraer
TraceI=2

# 1. Extraer informacion del Bin Header y realizar calculos
# -----------------------------------------------------------------------------
# 1A. Extraer Numero de Muestras (NS) por traza (bytes 21-22)
NS=$(dd if=$in bs=2 count=1 skip=3220 iflag=skip_bytes status=none | gmt convert -bi1h+b)

# 1B. Extraer Codigo de Data Sample Format (bytes 25-26) 
SF=$(dd if=$in bs=2 count=1 skip=3224 iflag=skip_bytes status=none | gmt convert -bi1h+b)
echo $SF

# Indexed arrays (lista de bytes para Data Sample Format code según Tabla 2 de SEG-Y_r2.0 Hagelund (2017)
SFC=(0 4 4 2 4 4 8 3 1 8 4 2 8 0 0 3 1)
Bytes=${SFC[$SF]}
echo $Bytes

# Crear indexed array con el codigo de GMT para convertir de Binario a ASCII segun el SFC.
# El index numero es 0 porque el index empieza a contar de 0.
# SOLO ESTE EL CODIGO PARA EL 5.
BIN=(0 0 0 0 0 1f+b 0 0 0 0 0 0 0 0 0 0 0)
BIC=${BIN[$SF]}
echo $BIC
# 1= 4-byte IBM Floating Point
# 2= 4-byte integer
# 3= 2-byte integer
# 4= 4-byte fixed-point with gain (obsolete)
# 5= 1f+b: 4-byte IEEE Floating point
# 6 y 7= NO USADOS
# 8. 1-byte integer


# 1C. Realizar calculos para saber que bytes hay que extraer
BT0=$(($NS*$Bytes))			        # Cantidad de Bytes de la traza SIN encabezado.	
BT=$(($NS*$Bytes+240))	  	  	    # Cantidad de Bytes de la traza	CON encabezado.
BTI=$(($BT*($TraceI-1)+3600+240)) 	# Numero de byte donde empiezan los datos de la traza a extraer

# 2. Extraer datos de la traza
# -----------------------------------------------------------------------------
# A. Con dd se extraen los datos.
# B. Con GMT convierto del formato binario (correspondiente al codigo 5) a ascii.

dd if=$in skip=$BTI iflag=skip_bytes bs=1 count=$BT0 | gmt convert -bi$BIC > $out

#gmt psxy $out -png Test -Wred -Baf -Ra