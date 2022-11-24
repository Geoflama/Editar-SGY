# Chequear el tamaño del SEGY
# Creado por Federico D. Esteban
# 2022-11-24.

# La cantidad de Bytes de un SEGY queda definido por el:
# 1. Cantidad de trazas
# 2. Cantidad de muestras por traza
# 3. Cantidad de bytes por muestra

# Este script chequea que el tamaño (en bytes) es coherente con los datos. 
# Asume que todas las trazas tienen la misma longitud.

# Datos de Entrada
# --------------------------------------------------------------
# Archivo analizar
in=test.sgy

# 1. Extraer informacion del Bin Header y realizar calculos
# -----------------------------------------------------------------------------
# 1A. Extraer Numero de Muestras (NS) por traza (bytes 21-22)
NS=$(dd if=$in bs=2 count=1 skip=3220 iflag=skip_bytes status=none | gmt convert -bi1h+b)

# 1B. Extraer Codigo de Data Sample Format (bytes 25-26) 
SF=$(dd if=$in bs=2 count=1 skip=3224 iflag=skip_bytes status=none | gmt convert -bi1h+b)
# Indexed arrays (lista de bytes por dato (BTD) segun el Data Sample Format code siguiendo a Tabla 2 de SEG-Y_r2.0 Hagelund (2017)
SFC=(0 4 4 2 4 4 8 3 1 8 4 2 8 0 0 3 1)
BPD=${SFC[$SF]}

# 1C. Obtener tamaño del archivo
byte=$(wc --byte < $in)

# 2A. Calcular cantidad de bytes por traza incluyendo encabezado (BT)
BT=$(($NS*$BPD+240))
echo $BT

# 2B. Calcular cantidad de trazas:
Trazas=$((($byte-3600)/$BT))
echo Cantidad de trazas: $Trazas

# 3. Calcular cantidad de Bytes de Mas (BDM)
BDM=$((($byte-3600)%$BT))
echo Bytes de Mas: $BDM

# 4. Calcular cantidad de datos en traza defectuosa
echo Numero de Muestras
echo Cantidad de Datos en las trazas: $NS
echo Cantidad de Dato en las trazas defectuosa: $((($BDM-240)/$BPD))
echo Cantidad trazas faltantes en traza defectuosa: $((($NS-($BDM-240)/$BPD)))

# 2. Crear nuevo Segy SIN los bytes de mas
# -----------------------------------------------------------------------------
#head --byte=-$BDM $in > Nuevo.sgy