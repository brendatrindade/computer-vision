import cv2
import mediapipe as mp
import time
from core.capture import captura_gestos
from core.engine import GestureEngine

def main():
    # Carregar a configuração do arquivo YAML
    engine = GestureEngine()
    if not engine.config:
        return
    print("Sistema iniciado. Aguardando gestos...")

    # Captura video da webcam
    cap = cv2.VideoCapture(0)  # 0 para a webcam padrao
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, engine.resolucao[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, engine.resolucao[1])
    cap.set(cv2.CAP_PROP_FPS, engine.fps) 

    
    with mp.solutions.hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8,  max_num_hands=2, model_complexity=1) as hands:
        try:
            while cap.isOpened():
                # Le um frame da webcam
                ret, frame = cap.read()
                if not ret:
                    continue
                if engine.flip_horizontal:
                    frame = cv2.flip(frame, 1)

                gesto, landmarks = captura_gestos(frame, hands)

                if gesto and landmarks:
                    print(f"Gesto detectado: {gesto}")
                    engine.update(landmarks)
                
                # Exibe o frame com as landmarks desenhadas
                cv2.imshow("Gesto", frame)
                
                # Encerra o loop se a tecla 'q' for pressionada
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                time.sleep(0.1)
        except KeyboardInterrupt:
            print("Sistema encerrado pelo usuário.")
        finally:
            cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    main()