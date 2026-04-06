import numpy as np
import math
import random
from numbers import Number
from pdf_generator import generate_pdf
import os
import tkinter as tk
from tkinter import messagebox

print("Xenakizator 1.0")

#----------------------- General limits -----------------------#
r=6                         #Max density exponent
dens_min=0.11*math.exp(0)   #Max section density
dens_max=0.11*math.exp(r)   #Min section density 
a_max=100                   #Max section lenght
na_max=200                  #Max section number of sounds

#----------------- Timbre classes parameters -----------------#
#Instruments distribution
orchestra=[
    [1],
    [1],
    [1],
    [1/2,1],
    [1/3,2/3,1],
    [1/3,2/3,1],
    [1/3,2/3,1],
    [1/3,2/3,1]
]

#Timbre class distribution
e=[
[0.05,0.10,0.10,0.30,0.20,0.05,0.10,0.10],
[0.05,0.25,0.08,0.09,0.08,0.13,0.22,0.10],
[0.10,0.10,0.05,0.15,0.10,0.10,0.20,0.20],
[0.05,0.15,0.15,0.15,0.15,0.10,0.15,0.10],
[0.15,0.05,0.05,0.18,0.05,0.17,0.17,0.18],
[0.09,0.13,0.03,0.20,0.05,0.20,0.19,0.11],
[0.16,0.18,0.02,0.26,0.03,0.11,0.12,0.12]
]

#---------------------- Pitch parameters ----------------------#
#Instruments extention
hinf=[
    [0],
    [15],
    [3],
    [31,15],
    [34,15,15],
    [34,15,15],
    [34,15,15],
    [34,15,15]
]
hsup=[
    [12],
    [51],
    [71],
    [72,53],
    [86,60,55],
    [86,60,55],
    [86,60,55],
    [86,60,55]
]

#-------------------- Duration parameters --------------------#
#Min values of array e
amax=[20,20,50,11.1111,33.3333,20,10,10]
#Physical limits (e.g. breath)
gn=[
    [15],
    [7],
    [15],
    [7,7],
    [15,15,15],
    [15,15,15],
    [15,15,15],
    [15,15,15]
]

#-------------- Normal distribution parameters --------------#
#Teta function
N = 256

teta = []
for k in range(N):
    z = k*0.01
    #erf function
    phi = math.erf(z)
    #Saves the value rounded to four digits
    teta.append(round(phi,4))

z1=[2.55,2.63,2.75,3.13,3.46,3.77,4.06,1*10^30]
z2=[0.9997,0.9998,0.9999,0.99999,0.999999,0.9999999,0.99999999,1]
modi=[64,32,16,8,4,2,1]

#-------------------- Glissandi parameters -------------------#
alfa=[[0],[0],[0]]  #Alpha values
vitlim=71           #Max glissando velocity [semitoni/sec]
vigl=[0,0,0]        #Array for the storage of the glissando velocity

#Constants
a10=10*math.sqrt(math.pi)
a30=30*math.sqrt(math.pi)
a17=17.7
a20=20*math.sqrt(math.pi)/r
a35=35

#-------------------------- Intensity -------------------------#
#Constants  
bf=44       #Number of intensity options

#--------------------- Initial conditions ---------------------#
sina=0
kte=6
ktr=8
q=[0]*ktr
s=[0]*ktr
alfx=[0]*ktr
beta=[0]*ktr
sect=0

point = [[]]

def macro():
    #Part 1 and 2 - Definition of lenght, density and number of events of a section
    global sect
    global upr
    ind=1
    jnd=1
    a=a_max+1       #Used for the 'while not' cycle
    while True:
        if(jnd>=15):
            a=delta

        while not (a<=a_max or ind>=15):
            x1=random.random()
            a=-delta*math.log(x1)
            if(ind==15):
                a=a_max/2.0
                break
            ind+=1
    
        while True:
            x2=random.random()
            if(sect==0 or ind>=15):
                ux=r*x2
                u=ux
                break
            else:
                if(random.random()>=0.5):
                    ux=upr-r*(1-math.sqrt(x2))
                else:
                    ux=upr+r*(1-math.sqrt(x2))
            if(ux>=0 and ux<=r):
                u=ux
                break

            ind+=1
        dens=dens_min*math.exp(u)
        na=(int(a*dens+0.5))+1

        if(na<na_max):
            break

        jnd=+1

    upr=u

    #Part 3 - Definition of instrumental classes table
    global sina
    global xalog
    sina=sina+float(na)
    xlogda=u
    xalog=a20*xlogda
    m=int(xlogda)

    if((m+2)>=kte):
        m=kte-2

    sr=0.0
    m1=m+1
    m2=m+2
    for i in range(0,ktr):
        alfx=e[m1][i]
        beta=e[m2][i]
        xm=m
        qr=(xlogda-xm)*(beta-alfx)+alfx
        q[i]=qr
        sr=sr+qr
        s[i]=sr
    
    #Generation of section points (aka microcomposition)
    micro(sect, dens, na)
    sect+=1

def micro(sect, da, na):
    t=0
    p_ta=0
    for n in range(na):
        #Part 4 - Definition of instant of attack of the point
        if n!=0:
            t=-math.log(random.random())/da
            p_ta=p_ta+t

        #Part 5 - Definition of timbre class and instrument of the point
        x1=random.random()

        for timb in range(len(orchestra)):
            if(x1<=s[timb]):
                x2=random.random()
                for strum in range(len(orchestra[timb])):
                    if(x2<=orchestra[timb][strum]):
                        p_instr=orchestra[timb][strum]
                        pien=p_instr
                        p_i=timb
                        p_j=strum
                        break
                break

        #Part 6 - Definition of pitch of the point
        hm=hsup[timb][strum]-hinf[timb][strum]
        c=0
        while True:
            x=random.random()

            if(n==0 or c>=15):
                p_hx=round(hinf[timb][strum]+hm*x)      #added round, original code didn't do it
                
            else:
                hpr=point[sect][n-1][1]
                if(random.random()>=0.5):
                    p_hx=round(hpr-hm*(1-math.sqrt(x))) #added round, original code didn't do it
                else:
                    p_hx=round(hpr+hm*(1-math.sqrt(x))) #added round, original code didn't do it

            if(p_hx>=hinf[timb][strum] and p_hx<=hsup[timb][strum]):
                break

            c+=1

        #Part 7 - Definition glissando values of the point
        if(timb!=5):
            vigl[0]=0
            vigl[1]=0
            vigl[2]=0
            x1=0
            x2=0
            xlambda=0
        elif(timb==5):
            kx=1 
            x1=random.random()
            if(x1-0.9946<0):
                i=127
                for ix in range(7):
                    if(teta[i]-x1<0):
                        i=i+modi[ix]
                    elif(teta[i]-x1>0):
                        i=i-modi[ix]

                if(teta[i]-x1<0):
                    tx1=teta[i]
                    xlambda=((i)+(x1-tx1)/(teta[i+1]-tx1))/100
                elif(teta[i]-x1==0):
                    xlambda=(i)/100
                elif(teta[i]-x1>0):
                    i=i-1
                    tx1=teta[i]
                    xlambda=((i)+(x1-tx1)/(teta[i+1]-tx1))/100
            elif(x1-0.9946==0):
                xlambda=2.55
            elif(x1-0.9946>0):
                for i in range(1,7):
                    tx1=z2[i]
                    if(x1-tx1<0):
                        tx2=z1[i]
                        xlambda=tx2-((tx1-x1)/(tx1-z2[i-1]))*(tx2-z1[i-1])
                        break
                    elif(x1-tx1==0):
                        xlambda=z1[i]
                        break

                    if(i==6):
                        i=7
                        tx1=1
                        tx2=z1[i]
                        xlambda=tx2-((tx1-x1)/(tx1-z2[i-1]))*(tx2-z1[i-1])
                        break
            alfa[0]=a10+xalog
            alfa[1]=a30-xalog
            x2=random.random()
            alfa[2]=a17+a35*x2
            for i in range(3):
                vigl[i]=int(alfa[i]*xlambda+0.5)
                if(vigl[i]<0):
                    vigl[i]=-vigl[i]
                if(vigl[i]>vitlim):
                    vigl[i]=vitlim
                if(random.random()<0.5):
                    vigl[i]=-vigl[i]


        #Parte 8 - Definizione durata del punto
        if(timb==6 or timb==7):
            p_dur=0
        else:
            zmax=amax[timb]/(dens_min*pien)
            g=gn[timb][strum]
            ro=g/math.log(zmax)
            qpnda=1/(q[timb]*pien*da)
            ge=abs(ro*math.log(qpnda))
            xmu=ge/2
            sigma=ge/4
            x1=random.random()
            if(x1-0.9946<0):
                i=127   #Used 127 instead of 128 because in Python the array starts at 0 differently from Fortran IV
                for ix in range(7):
                    if(teta[i]-x1<0):
                        i=i+modi[ix]
                    elif(teta[i]-x1>0):
                        i=i-modi[ix]

                if(teta[i]-x1<0):
                    tx1=teta[i]
                    xlambda=((i)+(x1-tx1)/(teta[i+1]-tx1))/100
                elif(teta[i]-x1==0):
                    xlambda=(i)/100
                elif(teta[i]-x1>0):
                    tx1=teta[i-1]
                    xlambda=((i)+(x1-tx1)/(teta[i+1]-tx1))/100
            elif(x1-0.9946==0):
                xlambda=2.55
            elif(x1-0.9946>0):
                for i in range(1,7):
                    tx1=z2[i]
                    if(x1-tx1<0):
                        tx2=z1[i]
                        xlambda=tx2-((tx1-x1)/(tx1-z2[i-1]))*(tx2-z1[i-1])
                        break
                    elif(x1-tx1==0):
                        xlambda=z1[i]
                        break

                    if(i==6 or x1-tx1>0):
                        i=7
                        tx1=1
                        tx2=z1[i]
                        xlambda=tx2-((tx1-x1)/(tx1-z2[i-1]))*(tx2-z1[i-1])
                        break
            tau=sigma*xlambda*1.4142
            x2=random.random()
            if(x2>=0.5):
                p_dur=xmu-tau
                if(p_dur<0):
                    p_dur=0
            else:
                p_dur=xmu+tau

        #Part 9 - Definition intensity of the point
        p_int=int(random.random()*bf+0.5)

        #Used for the visualization in the table
        if(timb==5):
            tab_gliss=vigl.copy()
        else:
            tab_gliss="\\"

        #Sound event
        point[sect].append([p_ta, p_i, p_j, p_hx, p_dur, p_int, tab_gliss])


        


################################    MAIN    ################################
sect=0
print("Starting generation")
def run(val1, val2, output_path):
    if os.path.exists(output_path):
        root = tk.Tk()
        root.withdraw()
        overwrite = messagebox.askyesno(
            title="File already exists",
            message=f"'{os.path.basename(output_path)}' already exists.\nDo you want to overwrite it?"
        )
        if not overwrite:
            return

    global delta
    delta=val1
    global sect_tot
    sect_tot=int(val2)
    for l in range(sect_tot):
        if(l<sect_tot-1):
            point.append([])
        macro()

    generate_pdf(point, sect_tot, output_path)

    messagebox.showinfo(
        title="Success",
        message=f"File generated successfully!\n\n{output_path}"
    )
