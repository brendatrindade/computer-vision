import math
import random

# deteccao de gestos com base nos landmarks
def distancia(p1, p2): # entre dois pontos
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def angulo(a, b, c): # entre tres pontos (A-B-C)
    ab = (a[0] - b[0], a[1] - b[1])
    cb = (c[0] - b[0], c[1] - b[1])
    dot = ab[0] * cb[0] + ab[1] * cb[1]
    mag_ab = math.sqrt(ab[0]**2 + ab[1]**2)
    mag_cb = math.sqrt(cb[0]**2 + cb[1]**2)
    if mag_ab * mag_cb == 0:
        return 0
    cos_angle = dot / (mag_ab * mag_cb)
    return math.degrees(math.acos(min(1, max(-1, cos_angle))))

def posicao_inicial(x, y):
    x_inicial = random.randint(0,x)
    y_inicial = random.randint(0,y)
    return x_inicial, y_inicial

def direcao_obstaculo(direcoes):
    direcao = random.choice(direcoes)
    return direcao
