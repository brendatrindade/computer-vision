from utils import utils

def get_threshold(landmarks, fator=0.25):
    return utils.distancia(landmarks[0], landmarks[12]) * fator

def detect_fingers_closed(landmarks):
    fingers = [8, 12, 16, 20]
    bases = [5, 9, 13, 17]
    required_fingers = 4
    threshold = get_threshold(landmarks)
    
    count = 0
    for f, b in zip(fingers, bases):
        d = utils.distancia(landmarks[f], landmarks[b])
        if d < threshold:
            count += 1
    return count >= required_fingers

# se os dedos especificados estao abertos (distantes da base)
def detect_fingers_open(landmarks):
    fingers = [8, 12, 16, 20]
    bases = [5, 9, 13, 17]
    required_fingers = 4
    threshold = get_threshold(landmarks)

    count = 0
    for f, b in zip(fingers, bases):
        d = utils.distancia(landmarks[f], landmarks[b])
        if d > threshold:
            count += 1
    return count >= required_fingers

def detect_closed_hand(landmarks):
    threshold = get_threshold(landmarks)
    return all((landmarks[i-1][1] - landmarks[i][1]) > threshold for i in range(5, 20, 4))

def detect_open_hand(landmarks):
    threshold = get_threshold(landmarks)
    return all((landmarks[i-1][1] - landmarks[i][1]) > threshold for i in range(5, 21, 4))

# se dois dedos estao para cima em relacao aos seus respectivos pontos base
def detect_two_fingers_up(landmarks):
    fingers = [8, 12]
    references = [6, 10]
    threshold = get_threshold(landmarks)

    for f, r in zip(fingers, references):
        if f not in landmarks or r not in landmarks:
            return False

        fx, fy = landmarks[f]
        rx, ry = landmarks[r]

        if fy >= (ry - threshold):
            return False

    return True

# indicador e polegar proximos
def detect_pinch(landmarks):
    finger1 = 4
    finger2 = 8
    threshold = get_threshold(landmarks)

    d = utils.distancia(landmarks[finger1], landmarks[finger2])
    
    return d < threshold

# polegar para cima
def detect_thumb_up(landmarks):
    thumb = 4
    base = 3
    threshold = get_threshold(landmarks)

    tx, ty = landmarks[thumb]  # Coordenadas do polegar
    bx, by = landmarks[base] # Coordenadas da base do polegar

    return (by - ty) > threshold # a coordenada Y do polegar deve ser menor (mais alto na imagem)

# polegar para baixo
def detect_thumb_down(landmarks):
    thumb = 4
    base = 3
    threshold = get_threshold(landmarks)

    tx, ty = landmarks[thumb]
    bx, by = landmarks[base]

    return ty > (by + threshold)

# apontar com um dedo (um dedo acima, os outros abaixo)
def detect_finger_up(landmarks):
    threshold = get_threshold(landmarks)
    ref_y = landmarks[6][1]
    return (ref_y - landmarks[8][1]) > threshold

def detect_finger_down(landmarks):
    threshold = get_threshold(landmarks)
    ref_y = landmarks[6][1]
    return (landmarks[8][1] - ref_y) > threshold

def detect_finger_left(landmarks):
    threshold = get_threshold(landmarks)
    ref_x = landmarks[5][0]
    return (ref_x - landmarks[8][0]) > threshold

def detect_finger_right(landmarks):
    threshold = get_threshold(landmarks)
    ref_x = landmarks[5][0]
    return (landmarks[8][0] - ref_x) > threshold

def detect_thumbs_and_pinky_up(landmarks):
    threshold = get_threshold(landmarks)
    
    thumb_up = landmarks[3][1] - landmarks[4][1] > threshold
    pinky_up = landmarks[19][1] - landmarks[20][1] > threshold
    return thumb_up and pinky_up

def detect_thumb_and_index_up(landmarks):
    threshold = get_threshold(landmarks)
    
    return (landmarks[3][1] - landmarks[4][1] > threshold and landmarks[7][1] - landmarks[8][1] > threshold)

def detect_thumb_and_index_together(landmarks):
    threshold = get_threshold(landmarks)
   
    distance = abs(landmarks[4][0] - landmarks[8][0])
    return distance < threshold  

def detect_index_and_middle_up(landmarks):
    threshold = get_threshold(landmarks)    
    
    return (landmarks[7][1] - landmarks[8][1] > threshold and landmarks[11][1] - landmarks[12][1] > threshold)

def detect_index_and_middle_down(landmarks):
    threshold = get_threshold(landmarks)
    
    return (landmarks[8][1] - landmarks[7][1] > threshold and landmarks[12][1] - landmarks[11][1] > threshold)