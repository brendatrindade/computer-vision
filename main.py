import pygame
import time
from movimento.personagem import Personagem
from movimento.obstaculo import Obstaculo
import random

def colisao(personagem, obstaculos, tela):
    # linhas x colunas no quadro de sprites do personagem
    n_linha_personagem = min(personagem.direcao, len(personagem.quadros) - 1)
    n_coluna_personagem = int(personagem.frame) % len(personagem.quadros[n_linha_personagem])
    #quadro atual
    quadro_personagem = personagem.quadros[n_linha_personagem][n_coluna_personagem]
    mascara_personagem = pygame.mask.from_surface(quadro_personagem)
    for obstaculo in obstaculos:
        linha_obstaculo = min(obstaculo.direcao, len(obstaculo.quadros) - 1)
        coluna_obstaculo = int(obstaculo.frame) % len(obstaculo.quadros[linha_obstaculo])
        quadro_obstaculo = obstaculo.quadros[linha_obstaculo][coluna_obstaculo]
        mascara_obstaculo = pygame.mask.from_surface(quadro_obstaculo)
        offset = (int(obstaculo.x - personagem.x), int(obstaculo.y - personagem.y))
        
        #pygame.draw.rect(tela, (255, 0, 0), quadro_personagem.get_rect(topleft=(personagem.x, personagem.y)), 2)
        #pygame.draw.rect(tela, (0, 0, 255), quadro_obstaculo.get_rect(topleft=(obstaculo.x, obstaculo.y)), 2)
        if mascara_personagem.overlap(mascara_obstaculo, offset):
            return True

def criar_jogo():
    personagem = Personagem()
    assets = ['./assets/boneco.png', './assets/barril.png', './assets/cacto.png', './assets/muralha.png', './assets/pc.png',]
    
    obstaculo1 = Obstaculo(caminho_img=random.choice(assets), x=0, y=0)
    obstaculo2 = Obstaculo(caminho_img=random.choice(assets), x=600, y=440)
    obstaculo3 = Obstaculo(caminho_img='./assets/sapo.png', l_q=71, a_q=48)
    obstaculo4 = Obstaculo(caminho_img=random.choice(assets))
    #obstaculo5 = Obstaculo(caminho_img=random.choice(assets))
    #obstaculo6 = Obstaculo(caminho_img=random.choice(assets))
    
    return personagem, [obstaculo1, obstaculo2, obstaculo3, obstaculo4]

def main():
    pygame.init()
    tela = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Robozinho")
        
    clock = pygame.time.Clock()
    running = True
    personagem, obstaculos = criar_jogo()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        tela.fill((250, 250, 250)) # Cor do fundo
        personagem.mover()
        personagem.desenhar(tela)
        for obstaculo in obstaculos:
            obstaculo.mover_horizontal()
            obstaculo.desenhar(tela)

        if colisao(personagem, obstaculos, tela):
            pygame.display.flip()
            esperando = True
            piscar = True
            tempo_pisca = 0
            while esperando:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        esperando = False
                        running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        personagem, obstaculos = criar_jogo()
                        esperando = False
                tela.fill((250, 250, 250))
                # Pisca a cada 10 frames
                if piscar:
                    personagem.desenhar(tela)
                for obstaculo in obstaculos:
                    obstaculo.desenhar(tela)
                pygame.display.flip()
                tempo_pisca += 1
                if tempo_pisca % 10 == 0:
                    piscar = not piscar
                clock.tick(30)

        pygame.display.flip()
        clock.tick(30)  # Limita a 30 FPS

    pygame.quit()
if __name__ == "__main__":
    main()