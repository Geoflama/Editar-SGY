#!/usr/bin/env -S bash -e

# Para utilizar el Script Segy_Split_dd_Batch es necesario crear una tabla con 3 columnas (Traza Inicial, Traza Final, Nombre del Segy)-
# Este script permite crear dicha lista a partir otra lista únicamente con los trazas final de cada segmento de segy a crear.

# Archivo con navegacion simplificada
in=NAV_T.txt

# 1. Extraer datos de traza final de cada segmento (que luego sera un perfil segy). Con 
#  -o: solo se extrae la columna con datos de Trazas
#  -q~0+s: NO escribe el primer registro de cada segmento (+s)
#  -T: NO escribe el header de cada segmento (el > que separa los segmentos en este caso).
gmt convert $in -o2 -q~0+s -T > TraceF

# 2. Traza inciales. El primer registro se asume que es 1.	
echo 1 > F0

# 3. Agregar otras Trazas. Con head quitar ultima traza y luego con awk
head TraceF -n -1 > F3
awk '{print $1+1}' F3 >> F0

# 4. Crear secuencia de nombres de los archivos de salida. Usar wc para contar las lineas
seq -f "SBP_M783a_%03g.sgy" $(wc -l < $in) > F2

# 5. Unir todas las columnas. 
paste F0 $in F2 > List

# Borrar archivos temporales
rm F?

# Calcular tamanio de los SEGY
#awk '{print $1-$2+1}' List
