from utils import utils

nome_dedo = {
    4: "polegar",
    8: "indicador",
    12: "dedo medio",
    16: "anelar",
    20: "mindinho"
}
base_por_ponta = {
    4: 3,
    8: 6,
    12: 10,
    16: 14,
    20: 18
}

def get_limiar_deteccao(parametros_detectados, fator=0.3):
    tam_palma_mao = utils.distancia(parametros_detectados[0], parametros_detectados[9])
    limiar_deteccao = tam_palma_mao * fator #30% por padrao
    return  limiar_deteccao #ajusta a verificacao de acordo a distancia da mao ate a camera

def movimento_polegar(parametros_detectados):
    limiar_deteccao = get_limiar_deteccao(parametros_detectados, fator=0.15)

    deteccao_x = parametros_detectados[4][0] - parametros_detectados[3][0]
    deteccao_y = parametros_detectados[3][1] - parametros_detectados[4][1] 

    if deteccao_y > limiar_deteccao and abs(deteccao_x) < limiar_deteccao: #abs - sem sinal
        return f"{nome_dedo[4]} cima"
    elif deteccao_y < -limiar_deteccao and abs(deteccao_x) < limiar_deteccao:
        return f"{nome_dedo[4]} baixo"
    elif deteccao_x > limiar_deteccao:
        return f"{nome_dedo[4]} direita"
    elif deteccao_x < -limiar_deteccao:
        return f"{nome_dedo[4]} esquerda"

def movimento_dedo_n(parametros_detectados, ponta_dedo):
    limiar_deteccao = get_limiar_deteccao(parametros_detectados)
    base_dedo = base_por_ponta[ponta_dedo]
    deteccao_y = parametros_detectados[base_dedo][1] - parametros_detectados[ponta_dedo][1]
    deteccao_x = parametros_detectados[ponta_dedo][0] - parametros_detectados[base_dedo][0]

    if deteccao_y > limiar_deteccao:
        return f"{nome_dedo[ponta_dedo]} cima", 8
    elif deteccao_y < -limiar_deteccao:
        return f"{nome_dedo[ponta_dedo]} baixo", 2
    elif deteccao_x > limiar_deteccao:
        return f"{nome_dedo[ponta_dedo]} direita", 6
    elif deteccao_x < -limiar_deteccao:
        return f"{nome_dedo[ponta_dedo]} esquerda", 4
    return None, None

def movimento_todos_dedos(parametros_detectados):
    estado_atual = []
    limiar_deteccao = get_limiar_deteccao(parametros_detectados)
    estado_polegar= movimento_polegar(parametros_detectados)

    if estado_polegar:
        estado_atual.append(estado_polegar)

    for ponta, base in base_por_ponta.items():
        if ponta not in parametros_detectados or base not in parametros_detectados:
            continue

        deteccao_y = parametros_detectados[base][1] - parametros_detectados[ponta][1]
        deteccao_x = parametros_detectados[ponta][0] - parametros_detectados[base][0]
        
        if deteccao_y > limiar_deteccao:
            estado_atual.append(f"{nome_dedo[ponta]} cima")
        if deteccao_y < -limiar_deteccao:
            estado_atual.append(f"{nome_dedo[ponta]} baixo")
        if deteccao_x > limiar_deteccao:
            estado_atual.append(f"{nome_dedo[ponta]} direita")
        if deteccao_x < -limiar_deteccao:
            estado_atual.append(f"{nome_dedo[ponta]} esquerda")

    return estado_atual