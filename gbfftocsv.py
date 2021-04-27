#! python

'''
Created on April 2021 for Programming course, EAFIT University
author: Santiago Alvarez, BSc
'''

#Importar las librerias de interés para el código

from Bio import Entrez
from Bio import Seq
import random
import pandas as pd
import time
from input_lanes import opt_input

#Inicio del contador de Tiempo, el resultado será dado en minutos
inicio=time.time()

#Inicio de los comandos de búsqueda de Entrez y creación de la lista de IDs

def search(query:str):

    q, email, rm, rs = opt_input()
    print(q,email,rm,rs)

    Entrez.email = email
    handleSearch = Entrez.esearch(db="Nucleotide", retmax=rm, retstart=rs, term=query)
    rec = Entrez.read(handleSearch)
    idlist = rec["IdList"]
    return idlist

#Recopilación de la información contenida en cada record haciendo uso de las E-utilities de Biopython Entrez

def query_record(idr)->dict:
    mydata = {}
    handleFetch = Entrez.efetch(db="nucleotide", retype="gb", id=idr, retmode="xml")
    record = Entrez.parse(handleFetch).__next__()
    mydata["idr"] = idr
    mydata["locus"] = record["GBSeq_locus"]
    mydata["bioproject"] = record["GBSeq_project"] if "GBSeq_project" in record else ""
    mydata["length"] = int(record["GBSeq_length"])
    mydata["strandedness"] = record["GBSeq_strandedness"]
    mydata["moltype"] = record["GBSeq_moltype"]
    mydata["topology"] = record["GBSeq_topology"]
    mydata["division"] = record["GBSeq_division"]
    mydata["source"] = record["GBSeq_source"]
    mydata["organism"] = record["GBSeq_organism"]
    mydata["taxonomy"] = record["GBSeq_taxonomy"]
    mydata["comment"] = record["GBSeq_comment"]
    mydata["sequence"] = record["GBSeq_sequence"] if "GBSeq_sequence" in record else ""
    mydata["a"] = mydata["sequence"].count('a')
    mydata["c"] = mydata["sequence"].count('c')
    mydata["g"] = mydata["sequence"].count('g')
    mydata["t"] = mydata["sequence"].count('t')
    mydata["protein"] = Seq.translate(record["GBSeq_sequence"] if "GBSeq_sequence" in record else "")
    mydata["features"] = record['GBSeq_feature-table']
    return mydata

#Recopilación de la data contenida en cada lista agregándola a su respectiva columna en el futuro CSV (listas)

def append_record_to_table(data,rec):
    data["idr"].append(rec["idr"])
    data["locus"].append(rec["locus"])
    data["bioproject"].append(rec["bioproject"])
    data["length"].append(rec["length"])
    data["strandedness"].append(rec["strandedness"])
    data["moltype"].append(rec["moltype"])
    data["topology"].append(rec["topology"])
    data["division"].append(rec["division"])
    data["source"].append(rec["source"])
    data["organism"].append(rec["organism"])
    data["taxonomy"].append(rec["taxonomy"])
    data["comment"].append(rec["comment"])
    data["sequence"].append(rec["sequence"])
    data["a"].append(rec["a"])
    data["c"].append(rec["c"])
    data["g"].append(rec["g"])
    data["t"].append(rec["t"])
    data["protein"].append(rec["protein"])

#Diccionario de la data recopilada con anterioridad.

def do_query(query):
    myDataDictionary = {"idr":[],"locus":[], "bioproject":[], "length":[],"strandedness":[],"moltype":[],
    "topology":[],"division":[],"source":[],"organism":[],"taxonomy":[],"comment":[],
    "a":[],"c":[],"g":[],"t":[],"sequence":[],"protein":[],}
    idlist = search(query)

#Información de procesamiento, conteo de registros y aplicación.

    print("proccessing {} records...".format(len(idlist)))
    for i in range(0,len(idlist)):
        print("querying rec #{} {}".format(i,idlist[i]),end='')
        record = query_record(idlist[i])
        print("...({0:6.2f}%) done.".format((i+1)/len(idlist)*100))
        append_record_to_table(myDataDictionary,record)
    df0bj = pd.DataFrame(myDataDictionary)
    return df0bj

#introducción término de búsqueda y conversión a CSV separado por tabulador.

if __name__ == "__main__":
    #q="q"
    q='all[filter] AND ((viruses[filter] OR archaea[filter] OR bacteria[filter] OR protists[filter]) AND refseq[filter] AND ("2000/01/01"[PDAT] : "2001/12/31"[PDAT]))'
    #'all[filter] AND ((viruses[filter] OR archaea[filter] OR bacteria[filter] OR protists[filter]) AND refseq[filter] AND ("2000/01/01"[PDAT] : "2010/12/31"[PDAT]))'
    d = do_query(q)
    d.to_csv("test1.csv",sep='\t')

#Fin del conteo de tiempo e impresión de tiempo total.

fin = time.time()
print("Total time ",((fin-inicio)/60),"minutos")
