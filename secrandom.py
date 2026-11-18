import random

def generar(): 
    secuencia = []
    for i in range(3):
        r = random.randint(1, 4)
        if r == 1:
            l = "A"
        elif r == 2:
            l = "B"
        elif r == 3:
            l = "C"
        elif r == 4:
            l = "D"
        secuencia.append(l)
    return secuencia