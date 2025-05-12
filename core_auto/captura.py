import cv2
import mediapipe as mp
from core_auto import mao

# Inicializa o modelo de deteccao de maos do MediaPipe
mp_maos = mp.solutions.hands
mp_desenho = mp.solutions.drawing_utils

cor_pontos_detectados = (100,0,0) # BGR
cor_linhas = (100,100,100)
espec_desenho_parametros = mp_desenho.DrawingSpec(color=cor_pontos_detectados, circle_radius=3)
espec_desenho_linhas = mp_desenho.DrawingSpec(color=cor_linhas, thickness=3)

def captura_mao(frame, maos):    
    # Converte a imagem para RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Processa o frame e detecta as maos
    maos_detectadas = maos.process(frame_rgb)

    if maos_detectadas.multi_hand_landmarks:
        for parametros_detectados in maos_detectadas.multi_hand_landmarks:
            # Desenha os parametros de deteccao da mao
            mp_desenho.draw_landmarks(
                frame,
                parametros_detectados,
                mp_maos.HAND_CONNECTIONS,
                espec_desenho_parametros,
                espec_desenho_linhas
            )
            # Escreve as coordenadas (x,y) dos pontos detectados da mao
            dic_parametros_detectados = {
                i: (parametro.x, parametro.y)
                for i, parametro in enumerate(parametros_detectados.landmark)
            }

            movimento_dedos = mao.movimento_todos_dedos(dic_parametros_detectados)
            #movimento_dedo8 = mao.movimento_dedo_n(dic_parametros_detectados, 8)

            return movimento_dedos, dic_parametros_detectados
    return None, None