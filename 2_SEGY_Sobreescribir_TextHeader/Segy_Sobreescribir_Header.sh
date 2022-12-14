# Sobreescribir el Text Header de un archivo SEG-Y.
# Creado por Federico D. Esteban
# 2022-11-23.

# Archivo a sobreescribir
out=test.sgy

# Nuevo encabezado (Text Header)
# Editar archivo NewTextHeader.txt.
# NOTA: Escribir SOLO 3200 bytes (40 filas de 80 caracteres).


# Escribir con 0 (borrar) el comienzo (los 3200 bytes iniciales) del archivo de salida.
dd conv=notrunc if=/dev/zero of=$out bs=3200 count=1

# Sobreescribir (notrunc) solo el comienzo (los 3200 bytes iniciales) del archivo de salida.
dd conv=notrunc if=NewTextHeader.txt of=$out bs=3200 count=1 #conv=notrunc