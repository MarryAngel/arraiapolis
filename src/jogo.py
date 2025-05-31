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
        #if self.peca_selecionada != None:
            
        pass

    def render(self, screen):
        """Renderiza o jogo na tela."""
        
        # Fundo da tela
        screen.fill((255, 255, 255))
        
        # desenhar um retângulo no topo da tela
        pygame.draw.rect(screen, (0, 0, 100), (100, 10, 800, 15))
        
        # desenhar o tabuleiro
        self.tabuleiro.desenhar(screen)
        
        # localização da caixa de seleção
        self.caixa_selecao = Caixa_Selecao(700, 40, 192, 192*3)
        self.caixa_selecao.desenhar(screen)
        
        # desenhar a peça selecionada
        if self.peca_selecionada:
            
            pos_x = pygame.mouse.get_pos()[0] # Centraliza a peça no mouse
            pos_y = pygame.mouse.get_pos()[1] # Centraliza a peça no mouse
            self.peca_selecionada.desenhar(screen, pos_x-32, pos_y-32)
        
        pass

    def input(self, event):
        """Processa a entrada do usuário."""
        # fechar a tela do jogo
        if event.type == "QUIT":
            print("Jogo fechado.")
            exit(0)
            
        # # ao pressionar a tecla L
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_l:
        #         print("Tecla L pressionada.")
        #         # Aqui você pode adicionar a lógica para lidar com a tecla L
        #         # Por exemplo, carregar um nível ou reiniciar o jogo
        #         self.tabuleiro.estado_tabuleiro[0][0] = Peca("l", "cinza")
            
        # capturar o clique esquerdo do mouse 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos_x, pos_y = event.pos
                input_peca = self.caixa_selecao.input(pos_x, pos_y)
                
                if input_peca:
                    self.peca_selecionada = input_peca
                    # self.caixa_selecao.reset()
               
                if self.peca_selecionada:
                    coord_tabuleiro= self.tabuleiro.get_coord_tabuleiro(pos_x, pos_y)
                    if coord_tabuleiro:
                        linha, coluna = coord_tabuleiro
                        if self.tabuleiro.colocar_peca(linha, coluna, self.peca_selecionada):
                            print(f"Peca {self.peca_selecionada.tipo} {self.peca_selecionada.formato} colocada na posição ({linha}, {coluna})")
                            self.peca_selecionada = None
                            self.caixa_selecao.reset()
                                
        pass