# Extraer solamente los datos de una traza de un archivo SEG-Y
# Se agrega otra columna con las profundidades segun Sample Interval (SI)
# Creado por Federico D. Esteban
# 2022-11-20
# Herramientas: dd (unix) y GMT

# Datos de Entrada
# --------------------------------------------------------------
# Archivo SEG-Y
in=../0_DatosPrueba/test.sgy
#0_DatosPrueba

# Archivo de Salida de texto plano.
out=Trace.txt

# Numero de la traza a extraer
Traza=2

# 1. Extraer informacion del Bin Header y realizar calculos
# -----------------------------------------------------------------------------
# A. Extraer Numero de Muestras (NS) por traza (bytes 21-22)
NS=$(dd if=$in bs=2 count=1 skip=3220 iflag=skip_bytes status=none | gmt convert -bi1h+b)

# B1. Extraer Codigo de Data Sample Format (bytes 25-26) 
SF=$(dd if=$in bs=2 count=1 skip=3224 iflag=skip_bytes status=none | gmt convert -bi1h+b)

# B2. Indexed arrays (lista de bytes para Data Sample Format code según Tabla 2 de SEG-Y_r2.0 Hagelund (2017)
SFC=(0 4 4 2 4 4 8 3 1 8 4 2 8 0 0 3 1)
Bytes=${SFC[$SF]}

# B3. Crear indexed array con el codigo de GMT para convertir de Binario a ASCII segun el SFC.
# El index numero es 0 porque el index empieza a contar de 0.
# SOLO ESTA EL CODIGO PARA EL 5. Ver pagina 7 de Hagelund (2017)
BIN=(0 4IBM 4INT 2INT 4FIX 1f+b NaN NaN 1INT 0 0 0 0 0 0 0 0)
BIC=${BIN[$SF]}

# C. Realizar calculos para saber que bytes hay que extraer
BT0=$(($NS*$Bytes))			        # Cantidad de Bytes de la traza SIN encabezado.	
BT=$(($NS*$Bytes+240))	  	  	    # Cantidad de Bytes de la traza	CON encabezado.
BTI=$(($BT*($Traza-1)+3600+240)) 	# Numero de byte donde empiezan los datos de la traza a extraer


# 2. Extraer datos de la traza
# -----------------------------------------------------------------------------
# A. Con dd se extraen los datos.
# B. Con GMT convierto del formato binario a ascii.
dd if=$in skip=$BTI iflag=skip_bytes bs=1 count=$BT0 | gmt convert -bi$BIC > $out

# 3. Calcular TWTT (o profundidad) de la traza
# -----------------------------------------------------------------------------
# D. Extraer Sample Rate (SR) en microsegundos del Bin Header (en bytes 3217-3218)
SR=$(dd if=$in bs=2 count=1 skip=3216 iflag=skip_bytes status=none | gmt convert -bi1h+b)
echo SI= $SR

# Extraer bytes 109-110 (delay recording time)
DELAY=$(($BT*($Traza-1)+3600+108)) 	# Numero de byte donde esta el SR en el TRACE Header
QQ=$(dd if=$in bs=2 count=1 skip=$DELAY iflag=skip_bytes status=none | gmt convert -bi1h+b)
echo $QQ 

# WIP. Hay que crear una columna con valores empezando en offset
seq 0 $NS $(($NS*$SR*1000)) > TWTT.txt

paste TWTT.txt $out > QQ.txt

# 4. Prueba. Extraer informacion del archivo
# -----------------------------------------------------------------------------
#gmt psxy $out -png Test -Wred -Baf -Ra
echo Datos segun NS: $NS
echo Datos segun gmt info:
gmt info $out

# Referencias
# Hagelund (2017) https://seg.org/Portals/0/SEG/News%20and%20Resources/Technical%20Standards/seg_y_rev2_0-mar2017.pdf

# Bytes 109-110: Delay recording time — Time in milliseconds between
# initiation time of energy source and the time when recording
# of data samples begins. In SEG-Y rev 0 this entry was
# intended for deep-water work if data recording did not start at
# zero time.

