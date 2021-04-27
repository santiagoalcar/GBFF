#! python

'''
Created on April 2021 for Programming course, EAFIT University

autor: Santiago Alvarez, BSc
'''

from sys import argv

#

def opt_input():
    q=""
    email="nobody@idk.com"
    rm=10
    rs=0

    print(argv)
    for info in argv[1:]:
        if info.startswith("q="):
            q=info.split("=")[1]
        if info.startswith("email="):
            email=info.split("=")[1]
        if info.startswith("rm="):
            try:
                rm=int(info.split("=")[1]) 
               # rm in range(1:100000)
            except:
                print("Introduced Value Not Valid. Value must be between 1 and 100000. Utilizing default value = 10")
        if info.startswith("rs="):
            try:
                rs=int(info.split("=")[1]) 
               # rs in range(0:99999)
            except:
                print("Introduced Value Not Valid. Value must be between 0 and 99999. Utilizing default value = 0")
    
    return q, email, rm, rs