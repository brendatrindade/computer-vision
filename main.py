import cv2
import mediapipe as mp
import time
from core_auto import captura
from core_auto.configuracao_yaml import Configuracao_yaml

def main():
    # Carrega a configuração do arquivo YAML
    yaml = Configuracao_yaml()
    if not yaml.config:
        return
    
    # Captura video da webcam
    captura_video = cv2.VideoCapture(0)  # 0 para a webcam padrao
    captura_video.set(cv2.CAP_PROP_FRAME_WIDTH, yaml.resolucao[0]) #largura - x
    captura_video.set(cv2.CAP_PROP_FRAME_HEIGHT, yaml.resolucao[1]) #altura - y
    captura_video.set(cv2.CAP_PROP_FPS, yaml.fps) 

    print("Sistema iniciado. Aguardando leitura das maos...")

    with mp.solutions.hands.Hands(min_detection_confidence=0.9, min_tracking_confidence=0.9,  max_num_hands=2, model_complexity=1) as maos:
        try:
            while captura_video.isOpened():
                # Le um frame da webcam
                sucesso_captura, frame = captura_video.read()
                if not sucesso_captura:
                    continue
                if yaml.flip_horizontal:
                    frame = cv2.flip(frame, 1) #espelha 

                movimento, parametros_detectados = captura.captura_mao(frame, maos)
                if movimento and parametros_detectados:
                    n_dedos = len(movimento)
                    cor_texto = (0,0,0) # BGR
                    if n_dedos >= 1:
                        cv2.putText(
                            frame, 
                            movimento[0],
                            (10, 30), # posicao
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            0.75, # escala da fonte
                            cor_texto, # cor 
                            1, # espessura da linha
                            cv2.LINE_AA
                        )
                    if n_dedos >= 2:
                        cv2.putText(
                            frame, 
                            movimento[1],
                            (10, 60), # posicao 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            0.75, # escala da fonte
                            cor_texto, # cor 
                            1, # espessura da linha
                            cv2.LINE_AA
                        )
                    if n_dedos >= 3:
                        cv2.putText(
                            frame, 
                            movimento[2],
                            (10, 90), # posicao 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            0.75, # escala da fonte
                            cor_texto, # cor 
                            1, # espessura da linha
                            cv2.LINE_AA
                        )
                    if n_dedos >= 4:
                        cv2.putText(
                            frame, 
                            movimento[3],
                            (10, 120), # posicao
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            0.75, # escala da fonte
                            cor_texto, # cor 
                            1, # espessura da linha
                            cv2.LINE_AA
                        )
                    if n_dedos == 5:
                        cv2.putText(
                            frame, 
                            movimento[4],
                            (10, 150), # posicao
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            0.75, # escala da fonte
                            cor_texto, # cor 
                            1, # espessura da linha
                            cv2.LINE_AA
                        )
                    print("Dedos detectados:", " - ".join(movimento))
                else:
                    cv2.putText(
                        frame, 
                        "Por favor, deixe uma mao visivel para iniciar",
                        (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.75,
                        (0, 0, 0), 
                        1, 
                        cv2.LINE_AA
                    )

                # Exibe o frame com os parametros de deteccao desenhados
                cv2.imshow(
                    "Captura movimento da mao", 
                    frame
                )
                
                if cv2.waitKey(1) & 0xFF == ord('f'):
                    print("Sistema encerrado pelo usuario")
                    break #se a tecla f for pressionada

                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Sistema encerrado pelo usuario")
        finally:
            captura_video.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    main()