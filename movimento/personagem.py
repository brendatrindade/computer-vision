import pygame
from utils import utils
from movimento import controle

class Personagem:
    def __init__(self):
        self.x, self.y = utils.posicao_inicial(640-40, 480-40)
        self.velocidade = 8
        self.direcao = 0
        self.frame = 0
        self.velocidade_animacao = 0.3
        
        self.sprite_sheet = pygame.image.load('./assets/movendo.png').convert_alpha()
        self.largura_folha, self.altura_folha = self.sprite_sheet.get_size()
        self.largura_quadro = 32  
        self.altura_quadro = 32  
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
        direcao_movimento = controle.controle()
        if direcao_movimento == 8: 
            self.y -= self.velocidade
            self.direcao = direcao_movimento
        elif direcao_movimento == 2: 
            self.y += self.velocidade
            self.direcao = direcao_movimento
        elif direcao_movimento == 6: 
            self.x += self.velocidade
            self.direcao = direcao_movimento
        elif direcao_movimento == 4:  
            self.x -= self.velocidade
            self.direcao = direcao_movimento
        
        if direcao_movimento is not None:
            self.frame += self.velocidade_animacao
            if self.frame >= self.colunas:
                self.frame = 0
        
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