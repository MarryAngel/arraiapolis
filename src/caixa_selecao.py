import pygame
from peca import Peca
import random

class Caixa_Selecao:
    
    def __init__(self, pos_x, pos_y, largura, altura):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.largura = largura
        self.altura = altura
        self.margem = 10
        
        self.tamanho_peca = largura  # Tamanho da peça (assumindo que todas as peças têm o mesmo tamanho)
        
        # Cores
        self.cor_fundo = (100, 0, 0)
        self.cor_borda = (0, 0, 100)
        
        self.reset()
        
    def reset(self):
        """Selecionar três peças aleatórias."""
        
        #Selecionar três peças aleatórias do conjunto de peças disponíveis
        self.pecas_disponiveis = random.sample(Peca.todas_pecas, 3)
        self.pecas_disponiveis = [Peca(peca, "cinza") for peca in self.pecas_disponiveis]
        
    def input(self, mouse_x, mouse_y):
        """Detecta se o mouse clicou em uma das peças disponíveis."""
        
        # Verifica se o clique está dentro em umas das pecas disponíveis
        for i, peca in enumerate(self.pecas_disponiveis):
            pos_x = self.pos_x + self.margem
            pos_y = self.pos_y + self.margem * i * 2 + i * (self.tamanho_peca) + (self.margem)
            
            if (mouse_x >= pos_x and mouse_x <= pos_x + self.tamanho_peca and
                mouse_y >= pos_y and mouse_y <= pos_y + self.tamanho_peca):
                self.pecas_disponiveis[i] = None
                return peca

        return None

    def desenhar(self, screen):
        pygame.draw.rect(screen, self.cor_fundo, (self.pos_x, self.pos_y, self.largura + 2 * self.margem, self.altura + 2 * self.margem + self.margem*4))
        pygame.draw.rect(screen, self.cor_borda, (self.pos_x, self.pos_y, self.largura + 2 * self.margem, self.altura + 2 * self.margem + self.margem*4), 1)
        
        # Desenhar as peças disponíveis
        for i, peca in enumerate(self.pecas_disponiveis):
            pos_x = self.pos_x + self.margem
            pos_y = self.pos_y + self.margem *i*2 + i * (self.tamanho_peca) + (self.margem)
            
            if peca is not None:
                peca.desenhar_bruto(screen, pos_x, pos_y)
    