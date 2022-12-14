# Sobreescribir el Text Header de un archivo SEG-Y.
# Creado por Federico D. Esteban
# 2022-11-23.

# Archivo a sobreescribir
out=test.sgy

# Nuevo encabezado (Text Header)
# Editar archivo NewTextHeader.txt.
# NOTA: Escribir SOLO 3200 bytes (40 filas de 80 caracteres).

# Escribir con 0 (borrar) los 3200 bytes iniciales (los del TextHeader) del archivo de salida.
dd conv=notrunc bs=3200 count=1 of=$out if=/dev/zero

# Incluir el texto del archivo NewTextHaeder.txt como TextHeader
dd conv=notrunc bs=3200 count=1 of=$out if=NewTextHeader.txt