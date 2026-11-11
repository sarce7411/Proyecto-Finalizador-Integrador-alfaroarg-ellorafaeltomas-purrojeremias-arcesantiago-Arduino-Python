import random

def generar(): 
    secuencia = []
    for i in range(4):
        r = random.randint(1, 4)
        secuencia.append(r)
    return secuencia

def potenciometro():
    r = random.randint(0, 1023)
    return r