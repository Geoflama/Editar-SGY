# Explicacion del script Segy_Sobreescribir_Header.sh

## Introduccion
Los archivos Segy tienen por definicion al inicio un encabezado textual (Text Header).
Ocupa 3200 bytes y sirve para escribir informacion sobre el archivo como por ejemplo
origen de los datos, procesamiento aplicado al segy, etc. 

El Text Header no es leido por los sofware para visualizar o procesar el segy. 
Por lo tanto es opcional.

## Script
Para editar el script se utiliza el programa de linux dd.




Referencias:

