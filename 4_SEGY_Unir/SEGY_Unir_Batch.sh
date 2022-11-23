# Unir un conjunto de archivos SEG-Y
# Creado por Federico D. Esteban
# 2022-11-23.

# Todos los segy deben tener el MISMO LARGO (en profundidad).

# Datos de Entrada
# --------------------------------------------------------------
# Crear lista de archivos a unir dentro de una carpeta
ls *.sgy > List

# Archivo de Salida
out=out/Unir_batch_join.sgy

# 1. Crear el nuevo Segy
# -----------------------------------------------------------------------------
# 1. Copiar encabezado del archivo 1 de la lista
head $(head -n1 List) --bytes=3600 > $out

# 2. Loop que copia sucesivamente las trazas de cada SEG-Y de la lista
# Copia todos los SEG-Y desde el byte 3601 hasta el final. 
while read -a line # IFS=" "
do
 echo Copiando arhivo ${line[0]}.
tail ${line[0]} --bytes=+3601 >> $out
done < List

# Borra List
rm List
