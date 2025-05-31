import pygame
from tabuleiro import Tabuleiro

class Jogo():

    def __init__(self):
        self.tabuleiro = Tabuleiro(50, 40)  # Inicializa o tabuleiro com a posição (50, 40)
        pass

    def tick(self):
        """Atualiza o estado do jogo."""
        pass

    def render(self, screen):
        """Renderiza o jogo na tela."""
        
        margem = 10
        
        # Montar barra de progresso no topo da tela
        screen.fill((255, 255, 255))
        
        # desenhar um retângulo no topo da tela
        pygame.draw.rect(screen, (0, 0, 100), (100, 10, 800, 15))
        
        # localização do tabuleiro
        #pygame.draw.rect(screen, (0, 100, 0), (50, 40, 640, 640))
        self.tabuleiro.desenhar(screen)
        
        
        # localização da caixa de seleção
        pygame.draw.rect(screen, (100, 0, 0), (700, 40, 192+2*margem, 2*margem+192))
        
        # locação da peça escolhida
        pygame.draw.rect(screen, (0, 0, 100), (700, 40 + 64*3*2+20, 192+2*margem, 2*margem+192))
        
        pass

    def input(self, event):
        """Processa a entrada do usuário."""
        # fechar a tela do jogo
        if event.type == "QUIT":
            print("Jogo fechado.")
            exit(0)
        pass