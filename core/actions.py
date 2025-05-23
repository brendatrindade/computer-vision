import subprocess
import platform
import keyboard
from core import detector

def execute_action(gesto, landmarks, config):
    # mapeamento dos gestos do arquivo config.yaml
    acao = config['gestures'].get(gesto)

    if not acao:
        #print(f"Gesto '{gesto}' nao identificado.")
        return False
    
    # Executa a acao apenas se a confianca for suficiente
    confianca = acao['detection'].get('min_confidence', 0.9)
    if confianca < 0.9:
        print(f"Confianca insuficiente para o gesto '{gesto}'. Confianca de {confianca}.")
        return False

    # Detecta o gesto de acordo com o tipo de deteccao
    if acao['detection']['type'] == 'finger_position':
        if not detector.detect_finger_position(landmarks, acao['detection']):
            return False
    elif acao['detection']['type'] == 'fingers_closed':
        if not detector.detect_fingers_closed(landmarks, acao['detection']):
            return False
    elif acao['detection']['type'] == 'pointing':
        if not detector.detect_pointing(landmarks, acao['detection']):
            return False
    elif acao['detection']['type'] == 'two_fingers_up':
        if not detector.detect_two_fingers_up(landmarks, acao['detection']):
            return False
    elif acao['detection']['type'] == 'pinch':
        if not detector.detect_pinch(landmarks, acao['detection']):
            return False
    elif acao['detection']['type'] == 'thumb_up':
        if not detector.detect_thumb_up(landmarks, acao['detection']):
            return False
    elif acao['detection']['type'] == 'thumb_down':
        if not detector.detect_thumb_down(landmarks, acao['detection']):
            return False
    
    # Se a acao foi detectada, executa de acordo com o sistema operacional
    sistema = platform.system()

    if sistema == "Windows":
        try:
            keyboard.press_and_release(acao['key_combo'])
            print(f"Acao '{acao['action']}' executada: {acao['key_combo']}")
        except ImportError:
            print("Biblioteca 'keyboard' nao instalada")
    
    elif sistema == "Linux":
        subprocess.run(["xdotool", "key", acao['key_combo']])
        print(f"Acao '{acao['action']}' executada: {acao['key_combo']}")

    elif sistema == "Darwin":
        print("macOS nao suportado")

    else:
        print(f"Sistema {sistema} nao reconhecido")
    
    if acao['feedback']['visual']:
        print(f"Feedback visual do gesto {gesto}: cor {acao['feedback']['color']}")
    return True