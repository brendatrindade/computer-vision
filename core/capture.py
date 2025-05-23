import cv2
import mediapipe as mp
from core.identify import identificar_gesto

# Inicializa o modelo de deteccao de maos do MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def captura_gestos(frame, hands):    
    # Converte a imagem para RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Processa o frame e detecta as maos
    results = hands.process(rgb_frame)

    # Se maos forem detectadas
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Desenha as landmarks das maos
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Pega as coordenadas das landmarks das maos
            landmarks_dict = {
                i: (landmark.x, landmark.y)
                for i, landmark in enumerate(landmarks.landmark)
            }
        
            gesto = identificar_gesto(landmarks_dict)
            return gesto, landmarks_dict
    return None, None