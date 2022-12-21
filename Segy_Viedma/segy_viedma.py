# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 12:27:27 2019

@author: sebastian principi
"""

import pandas
import segyio
import os
import shutil

path=r"C:\Users\usuario\Desktop\segy_viedma"
os.chdir(path)

cant_canales=8

for file in os.listdir(path):
    
    #abro todos los .gy de la carpeta
    if file.endswith(".sgy") and not file.startswith("UTM19_"):
        input_=str(file)
        output_="UTM19_"+str(file)
        shutil.copyfile(input_, output_)
        filename=output_
        
        df = pandas.read_csv(input_[0:-4]+".txt", sep="\t", names=[ 'X', 'Y'])

        with segyio.open(output_, "r+", ignore_geometry=True) as f:

            FFID=f.attributes(segyio.TraceField.FieldRecord)[:]
            
            n_field_records=FFID[-1]-FFID[0]
            
            n=0
            i=0
            while n<len(f.header):
                print("i: ",i)
                for n in range(n,n+8):
                    print("n: ",n)
  
                    f.header[n][segyio.TraceField.SourceX]=int(df.X[i])
                    f.header[n][segyio.TraceField.SourceY]=int(df.Y[i])
                    
                i=i+1
                n=n+1


    
    
