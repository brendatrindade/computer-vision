from core import detector

def identificar_gesto(landmarks_dict):
    if detector.detect_fingers_closed(landmarks_dict):
        return 'fingers_closed'
    
    if detector.detect_fingers_open(landmarks_dict):
        return 'fingers_open'
    
    if detector.detect_closed_hand(landmarks_dict):
        return 'close_hand'
    
    if detector.detect_open_hand(landmarks_dict):
        return 'open_hand'

    # Dois dedos para cima
    if detector.detect_two_fingers_up(landmarks_dict):
        return 'two_fingers_up'
    
    # Pinça: indicador e polegar próximos
    if detector.detect_pinch(landmarks_dict):
        return 'pinch'

    # Polegar para cima
    if detector.detect_thumb_up(landmarks_dict):
        return 'thumb_up'

    # Polegar para baixo
    if detector.detect_thumb_down(landmarks_dict):
        return 'thumb_down'
    
    if detector.detect_finger_up(landmarks_dict):
        return 'finger_up'
    
    if detector.detect_finger_down(landmarks_dict):
        return 'finger_down'
    
    if detector.detect_finger_left(landmarks_dict):
        return 'finger_left'
    
    if detector.detect_finger_right(landmarks_dict):
        return 'finger_right'

    if detector.detect_thumb_and_index_up(landmarks_dict):
        return 'thumb_index_up'

    if detector.detect_thumb_and_index_together(landmarks_dict):
        return 'thumb_index_together'

    if detector.detect_index_and_middle_up(landmarks_dict):
        return 'index_middle_up'

    if detector.detect_index_and_middle_down(landmarks_dict):
        return 'index_middle_down'

    return 'unknown'