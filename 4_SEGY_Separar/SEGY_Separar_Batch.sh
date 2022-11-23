# Separar un SEG-Y en distintos archivos.
# Creado por Federico D. Esteban
# 2022-11-23.

# Datos de Entrada
# --------------------------------------------------------------
# Archivo a dividir (entrada)
in=1_Datos_Segy/m783a_all.sgy

folder=2_Splits_Segy/
# Lista con Valores de: Traza Inicial, Traza Final y Nombre del Segy.
#cat << 'EOF' > List
#1 2 001.sgy
#3 4 002.sgy
#EOF
cat << 'EOF' > List
1478334	1479635	SBP_M783a_187.sgy
EOF

# 1. Extraer informacion del Bin Header y realizar calculos
# -----------------------------------------------------------------------------
# 1A. Extraer Numero de Muestras (NS) por traza (bytes 21-22)
NS=$(dd if=$in bs=2 count=1 skip=3220 iflag=skip_bytes | gmt convert -bi1h+b)

# 1B. Extraer Codigo de Data Sample Format (bytes 25-26) 
SF=$(dd if=$in bs=2 count=1 skip=3224 iflag=skip_bytes | gmt convert -bi1h+b)
# Indexed arrays (lista de bytes para Data Sample Format code según Tabla 2 de SEG-Y_r2.0 Hagelund (2017)
SFC=(0 4 4 2 4 4 8 3 1 8 4 2 8 0 0 3 1)
Bytes=${SFC[$SF]}

# Leer variables de una lista y asignarlos como variables
while read -a line # IFS=" "
do
 echo Creando ${line[2]} desde la traza ${line[0]} hasta la ${line[1]}.

# 1C. Realizar calculos para saber que bytes hay que extraer
NT=$((${line[1]}-${line[0]}+1))	    # Cantidad de Trazas
BT=$(($NS*$Bytes+240))	            # Cantidad de Bytes por Traza (encabezado + header)
BTI=$(($BT*(${line[0]}-1)+3600))    # Numero de byte de la traza inicial

# 2. Crear el nuevo Segy
# -----------------------------------------------------------------------------
# 1. Copiar Header (son siempre los primeros 3600 bytes)
dd if=$in bs=3600 count=1 > $folder${line[2]}

# 2. Agregar datos de las trazas
dd if=$in skip=$BTI iflag=skip_bytes bs=$BT count=$NT >> $folder${line[2]}

done < List

# Borra Lista
#rm List