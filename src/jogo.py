import pygame
from tabuleiro import Tabuleiro
from peca import Peca
from caixa_selecao import Caixa_Selecao

class Jogo():

    def __init__(self):
        self.tabuleiro = Tabuleiro(50, 40)                      # Inicializa o tabuleiro com a posição (50, 40)
        self.caixa_selecao = Caixa_Selecao(700, 40, 192, 192)   # Inicializa a caixa de seleção
        self.peca_selecionada = None
        
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
        #pygame.draw.rect(screen, (100, 0, 0), (700, 40, 192+2*margem, 2*margem+192))
        caixa_selecao = Caixa_Selecao(700, 40, 192*0.75, 192*0.75*3)
        caixa_selecao.desenhar(screen)
        
        # locação da peça escolhida
        #pygame.draw.rect(screen, (0, 0, 100), (700, 40 + 64*3*2+20, 192+2*margem, 2*margem+192))
        
        pass

    def input(self, event):
        """Processa a entrada do usuário."""
        # fechar a tela do jogo
        if event.type == "QUIT":
            print("Jogo fechado.")
            exit(0)
            
        # ao pressionar a tecla L
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                print("Tecla L pressionada.")
                # Aqui você pode adicionar a lógica para lidar com a tecla L
                # Por exemplo, carregar um nível ou reiniciar o jogo
                self.tabuleiro.estado_tabuleiro[0][0] = Peca("l", "cinza")
            
        # capturar o clique esquerdo do mouse 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos_x, pos_y = event.pos
                print(f"Clique detectado na posição: ({pos_x}, {pos_y})")
        

        pass