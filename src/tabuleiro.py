import pygame

class Tabuleiro:
    def __init__(self, pos_x, pos_y):
        self.linhas = 10
        self.colunas = 10
        self.tamanho_celula = 64
        self.offset_x =  pos_x
        self.offset_y = pos_y
        
        # Cores
        self.cor_celula = (192, 192, 192)  # Um tom de cinza (Silver)
        self.cor_borda = (128, 128, 128)   # Um cinza mais escuro para as bordas
        
        self.estado_tabuleiro = [[None for _ in range(self.colunas)] for _ in range(self.linhas)]
        
    def desenhar(self, screen):
        """Desenha a grade do tabuleiro na tela."""
        
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                # Calcular a posição da célula
                x_celula = self.offset_x + (coluna * self.tamanho_celula)
                y_celula = self.offset_y + (linha * self.tamanho_celula)
        
                rect_celula =  rect_celula = pygame.Rect(x_celula, y_celula, self.tamanho_celula, self.tamanho_celula)

               # Desenha o interior da célula com a cor cinza
                pygame.draw.rect(screen, self.cor_celula, rect_celula)

                # Desenha a borda da célula
                pygame.draw.rect(screen, self.cor_borda, rect_celula, 1)  # O '1' define a espessura da borda
                
        # desenhar a peca
        
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                peca = self.estado_tabuleiro[linha][coluna]
                if peca != None:
                    # Desenhar a peça na célula
                    peca.desenhar(screen, self.offset_x + (coluna * self.tamanho_celula), self.offset_y + (linha * self.tamanho_celula)) 
        
    