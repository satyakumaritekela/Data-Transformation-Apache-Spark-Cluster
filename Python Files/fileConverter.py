import csv
import json
import sys
import pandas as pd


def changeToText(ipfile, opfile, textfile):
    
    # checking for input and output file
    if ipfile is not None and opfile is not None:
        
        inputFile = ipfile
        outputFIle = opfile
        
        # opening json file
        with open(inputFile, 'r', encoding='UTF-8', errors='strict') as ip_File:
            # loading json
            data = json.load(ip_File)
            
        
        # loading csv file
        op_FIle = open(outputFIle, 'w', encoding='utf-8')
        
        # close the input file
        ip_File.close()
        
        # create a csv.writwe
        output = csv.writer(op_FIle, delimiter=',', lineterminator='\n')
        
        # writing the header row
        output.writerow(data[0].keys())
        
        # writing all the data
        for row in data:
            output.writerow(row.values())
        op_FIle.close()
        
        df = pd.read_csv(opfile, delimiter=",", encoding='utf-8')
            
        df.to_csv(textfile, index = None, header = True)
                
