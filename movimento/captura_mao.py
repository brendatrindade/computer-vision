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
    # Processa o frame e detecta as maos
    if frame is not None:
        # Converte a imagem para RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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

                buffer_direcao = []
                for i in range(0, 5):
                    movimento_dedo8, direcao = mao.movimento_dedo_n(dic_parametros_detectados, 8)
                    buffer_direcao.append(direcao)
                todos_iguais = all(n == buffer_direcao[0] for n in buffer_direcao)
                if todos_iguais:
                    return movimento_dedo8, dic_parametros_detectados, buffer_direcao[0]
            return movimento_dedo8, dic_parametros_detectados, 0
    return None, None, None