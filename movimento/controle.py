import cv2
import mediapipe as mp
import time
from movimento import captura_mao
from core_auto.configuracao_yaml import Configuracao_yaml

class ControladorMao:
    def __init__(self):
        # Carrega a configuração do arquivo YAML
        self.yaml = Configuracao_yaml()
        if not self.yaml.config:
            return
        
        # Captura video da webcam
        self.captura_video = cv2.VideoCapture(0)  # 0 para a webcam padrao
        self.captura_video.set(cv2.CAP_PROP_FRAME_WIDTH, self.yaml.resolucao[0]) #largura - x
        self.captura_video.set(cv2.CAP_PROP_FRAME_HEIGHT, self.yaml.resolucao[1]) #altura - y
        self.captura_video.set(cv2.CAP_PROP_FPS, self.yaml.fps) 

        self.maos = mp.solutions.hands.Hands(min_detection_confidence=0.9, min_tracking_confidence=0.9,  max_num_hands=1, model_complexity=0)

    print("Sistema iniciado. Aguardando leitura das maos...")

    def get_direcao(self):
        # Le um frame da webcam
        sucesso_captura, frame = self.captura_video.read()
        if not sucesso_captura:
            return None
            
        if self.yaml.flip_horizontal:
            frame = cv2.flip(frame, 1) #espelha 
            
        movimento_indicador, _, direcao = captura_mao.captura_mao(frame, self.maos)
        if direcao:
            print(f"Direcao movimento: {movimento_indicador}\n")
            return direcao
        # Exibe o frame com os parametros de deteccao desenhados
        '''cv2.imshow(
            "Captura movimento da mao", 
            frame
        )'''
        #time.sleep(0.1)
        
    def __del__(self):
        self.captura_video.release()
        cv2.destroyAllWindows()
        self.maos.close()

def controle():
    global controlador
    if 'controlador' not in globals():
        controlador = ControladorMao()
    return controlador.get_direcao()