import time
import yaml
from core.actions import execute_action
from core import detector

class GestureEngine:
    def __init__(self, config_path='config.yaml'):
        self.config = self._load_config(config_path)
        camera_config = self.config['hardware']['camera']
        self.resolucao = tuple(camera_config['resolution'])
        self.fps = camera_config['fps']
        self.flip_horizontal = camera_config['flip_horizontal']
        self.auto_exposure = camera_config['auto_exposure']
        aceleracao_config = self.config['hardware']['acceleration']
        self.use_gpu = aceleracao_config['use_gpu']
        self.num_threads = aceleracao_config['num_threads']
        self.gestures = self.config.get('gestures', {})
        self.cooldowns = {}
        self.last_activations = {}

    def _load_config(self, path):
        try:
            with open(path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            print(f"Erro ao carregar configuracao: {e}")
            return {}

    def update(self, landmarks):
        for name, gesture in self.gestures.items():
            detection = gesture.get('detection', {}) 
            cooldown = self.config.get('settings', {}).get('gesture', {}).get('cooldown', 0.5)

            if self._is_in_cooldown(name, cooldown):
                continue

            if self._detect_gesture(landmarks, detection):
                self._activate(name, gesture)

    def _is_in_cooldown(self, gesture_name, cooldown):
        now = time.time()
        last_time = self.last_activations.get(gesture_name, 0)
        return (now - last_time) < cooldown

    def _activate(self, name, gesture):
        self.last_activations[name] = time.time()
        action = gesture.get('action')
        key_combo = gesture.get('key_combo')
        execute_action(action, key_combo, self.config)

    def _detect_gesture(self, landmarks, detection):
        tipo = detection.get('type')
        if tipo == 'fingers_closed':
            return detector.detect_fingers_closed(landmarks)
        if tipo == 'fingers_open':
            return detector.detect_fingers_open(landmarks)
        if tipo == 'two_fingers_up':
            return detector.detect_two_fingers_up(landmarks)
        if tipo == 'pinch':
            return detector.detect_pinch(landmarks)
        if tipo == 'thumb_up':
            return detector.detect_thumb_up(landmarks)
        if tipo == 'thumbs_and_pinky_up':
            return detector.detect_thumbs_and_pinky_up(landmarks)
        if tipo == 'thumb_down':
            return detector.detect_thumb_down(landmarks)
        if tipo == 'index_and_middle_up':
            return detector.detect_index_and_middle_up(landmarks)
        if tipo == 'index_and_middle_down':
            return detector.detect_index_and_middle_down(landmarks)
        if tipo == 'finger_left':
            return detector.detect_finger_left(landmarks)
        if tipo == 'finger_right':
            return detector.detect_finger_right(landmarks)
        if tipo == 'finger_up':
            return detector.detect_finger_up(landmarks)
        if tipo == 'finger_down':
            return detector.detect_finger_down(landmarks)
        return False