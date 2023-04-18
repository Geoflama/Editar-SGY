# Separar un SEG-Y en distintos archivos.
# Creado por Federico D. Esteban
# 2023-04-18.

# Datos de Entrada
# --------------------------------------------------------------
# Archivo a dividir (entrada)
in=../0_DatosPrueba/test.sgy

# Cantidad de divisiones del SEGY
N=2
#folder=2_Splits_Segy/

# 1. Crear archivo con solo el header (primeros 3600 bytes)
head $in --bytes=3600 > tmp_head

# 2. Crear nuevo archivo sin encabezado (primeros 3600 bytes)
tail $in --bytes=+3601 > tmp_file.sgy
split tmp_file.sgy -n $N -d tmp_qqq

ls tmp_qqq* > tmp_list2
seq $N > tmp_seq
paste tmp_seq tmp_list2 > tmp_list

while read -a line # IFS=" ";
do
cat tmp_head ${line[1]} > ${line[0]}.sgy
done < tmp_list

# Borrar archivos temporales
#rm tmp_*
