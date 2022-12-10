# Sobreescribir el Text Header de un archivo SEG-Y.
# Creado por Federico D. Esteban
# 2022-11-23.

# Crear lista de archivos SEG-Y a sobreescribir el text header.
# Lo mas practico es poner todos los archivos dentro de una carpeta y usar:
ls *.sgy > List

# Nuevo encabezado (Text Header)
# Editar archivo NewTextHeader.txt.
# NOTA: Escribir SOLO 3200 bytes (40 filas de 80 caracteres).


# 2. Loop que sobreescribe los text header de cada SEG-Y de la lista
while read -a line
do
 echo Sobreescribiendo encabezado del archivo ${line[0]}.

# Sobreescribir (notrunc) solo el comienzo (los 3200 bytes iniciales) del archivo de salida.
dd conv=notrunc if=NewTextHeader.txt of=${line[0]} bs=3200 count=1 conv=notrunc
done < List

# Borra List
rm List