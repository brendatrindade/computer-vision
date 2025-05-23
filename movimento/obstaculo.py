import pygame
import time
import random
from utils import utils

class Obstaculo:
    def __init__(self, caminho_img='./assets/lamina.png', x=-1, y=-1, l_q=48, a_q=48):
        if x == -1 and y == -1:
            self.x, self.y = utils.posicao_inicial(640-40, 480-40)
        else:
             self.x, self.y = x, y
        self.velocidade = 5
        self.direcao = utils.direcao_obstaculo([6,4])
        self.frame = 0
        self.velocidade_animacao = 0.2
        
        self.sprite_sheet = pygame.image.load(caminho_img).convert_alpha()
        self.largura_folha, self.altura_folha = self.sprite_sheet.get_size()
        self.largura_quadro = l_q 
        self.altura_quadro = a_q  
        self.colunas = self.largura_folha // self.largura_quadro
        self.linhas = self.altura_folha // self.altura_quadro
        
        self.quadros = self.carregar_quadros()
    
    def carregar_quadros(self):
        quadros = []
        for linha in range(self.linhas):
            linha_quadros = []
            for coluna in range(self.colunas):
                x = coluna * self.largura_quadro
                y = linha * self.altura_quadro
                if (x + self.largura_quadro <= self.largura_folha and 
                    y + self.altura_quadro <= self.altura_folha):
                    quadro = self.sprite_sheet.subsurface(pygame.Rect(x, y, self.largura_quadro, self.altura_quadro))
                    linha_quadros.append(quadro)
            quadros.append(linha_quadros)
        return quadros
    
    def mover(self):
        if self.direcao == 8: 
            self.y -= self.velocidade
        elif self.direcao == 2:  
            self.y += self.velocidade
        elif self.direcao == 6:  
            self.x += self.velocidade
        elif self.direcao == 4:
            self.x -= self.velocidade

        self.frame += self.velocidade_animacao
        if self.frame >= self.colunas:
            self.frame = 0

        # Sorteia se muda para nova direcao
        mudou = random.randint(0,50)
        i = random.randint(0,20)
        if mudou == i:
            direcoes = [8, 2, 6, 4]
            direcoes.remove(self.direcao)
            self.direcao = random.choice(direcoes)

        bateu = False
        if self.x <= 0:
            bateu = True
        elif self.x >= 640 - self.largura_quadro:
            self.x = 640 - self.largura_quadro
            bateu = True
        if self.y <= 0:
            bateu = True
        elif self.y >= 480 - self.altura_quadro:
            self.y = 480 - self.altura_quadro
            bateu = True
        if bateu:
            direcoes = [8, 2, 6, 4]
            direcoes.remove(self.direcao)
            self.direcao = random.choice(direcoes)
            
        self.x = max(0, min(self.x, 640 - self.largura_quadro))
        self.y = max(0, min(self.y, 480 - self.altura_quadro))
    
    def mover_horizontal(self):
        self.velocidade_animacao = random.choice([0.2, 0.3, 0.4, 0.5])
        self.velocidade = random.randint(3,12)

        if self.direcao == 6:  
            self.x += self.velocidade
        elif self.direcao == 4:
            self.x -= self.velocidade

        self.frame += self.velocidade_animacao
        if self.frame >= self.colunas:
            self.frame = 0

        if self.x <= 0:
            self.direcao = 6
            _, self.y = utils.posicao_inicial(600, 400)
        elif self.x >= 640 - self.largura_quadro:
            self.direcao = 4
            _, self.y = utils.posicao_inicial(600, 400)

        self.x = max(0, min(self.x, 640 - self.largura_quadro))
        self.y = max(0, min(self.y, 480 - self.altura_quadro))
            
    def desenhar(self, tela):
        linha = 0  # animacao para baixo

        if self.direcao == 8:
            linha = 0
        elif self.direcao == 6:
            linha = 1
        elif self.direcao == 2:
            linha = 2
        elif self.direcao == 4:
            linha = 3
        
        linha = min(linha, self.linhas - 1)
        quadro = int(self.frame) % self.colunas
        tela.blit(self.quadros[linha][quadro], (self.x, self.y))