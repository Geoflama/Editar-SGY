# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 08:51:28 2022

Creaado por Sebastian Principi
"""

import os
import segyio
import pandas as pd
import glob

path=r"D:"
path=r"/media/thor/Datos/SISMICA_3D/0_Datos_Ministerio/BDIH/Carina_1996/SGY/"
path=r"/media/thor/Datos/SISMICA_3D/0_Datos_Ministerio/BDIH/Ara-Argo-Aries_1994/SGY/"
os.chdir(path)

#Contador para ver avance del script
number_of_segy = len(glob.glob1(path,"*.sgy"))
count=1

#Dataframe con coordenadas
d=pd.DataFrame()

df_lineas_erroneas=pd.DataFrame()

#Lista donde irán las lineas erroneas
for file in os.listdir(path):
    
    #abro todos los .gy de la carpeta
    if file.endswith(".sgy"):
        input_=str(file)
        
        #contador
        print("File "+str(count)+"/"+str(number_of_segy))
        count=count+1
        
        #Intento abrir el archivo con segio
        try:
            with segyio.open(input_, "r+", ignore_geometry=True) as f:
                
                #Guardo las coordenadas X e Y
                CDPY = f.attributes(segyio.TraceField.CDP_Y)[:]
                inline3d = f.attributes(segyio.TraceField.INLINE_3D)[:]
                cdp= f.attributes(segyio.TraceField.CDP)[:]
                
                temp=pd.DataFrame(
                    {   "#CDPY":CDPY,
                        "INLINE3D":inline3d,
                        "CDP": cdp,
                        "Line name":[input_]*len(CDPY),
                        })
                d=pd.concat([d,temp])
                
                
        #Si me tira error, imprimo el nombre de la linea y continuo con el for
        except RuntimeError:
            print("Linea erronea: " + input_)
            
            temp_error=pd.DataFrame(
                {   
                    "Linea_erronea": input_}
                )
            df_lineas_erroneas=pd.concat([d,temp])
                
                
            pass



d.to_csv("coordenadas_segy.csv", index=False,sep=",")  
df_lineas_erroneas.to_csv("lineas_erroneas_segy.csv", index=False,sep=",")  
