import os
Texto= open("PruebaLab4.s")
with open("resultMedio","w") as file:
    count=0
    for line in Texto:

        if(line!='\n'):
            if(line.split("#")[0]!=''):
                count=count+1
                file.write(line.split("#")[0].strip("\t")+'\n')

Texto= open("resultMedio")
dictionary={}
count=0
for line in Texto:
    if(line!='\n'):
        if(':'in line):
            dictionary[line.split(":")[0].strip(" ")]=count
        else:
            count=count+1

with open("result","w") as file:
    Texto= open("resultMedio")
    count=-1
    for line in Texto:
        if(line!='\n'):
            if(not ':'in line):
                line=line.replace('\t',' ')
                count=count+1
                for head in dictionary:
                    if (head in line):
                        line=line.replace(head,str((dictionary[head]-count)*4))

                file.write(line)
Texto=''
os.remove('resultMedio')
