import pygame
from peca import Peca_Fantasma

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
                        
        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                peca = self.estado_tabuleiro[linha][coluna]
                if peca != None:
                    # Desenhar a peça na célula
                    peca.desenhar(screen, self.offset_x + (coluna * self.tamanho_celula), self.offset_y + (linha * self.tamanho_celula)) 
        
    def get_coord_tabuleiro(self, pos_x, pos_y):
        """Converte as coordenadas da tela para as coordenadas do tabuleiro."""
        if (pos_x < self.offset_x or pos_x > self.offset_x + self.colunas * self.tamanho_celula or
            pos_y < self.offset_y or pos_y > self.offset_y + self.linhas * self.tamanho_celula):
            return None
        
        coluna = (pos_x - self.offset_x) // self.tamanho_celula
        linha = (pos_y - self.offset_y) // self.tamanho_celula
        
        return (linha, coluna)
    
    def colocar_peca(self, linha, coluna, peca):
        """Coloca uma peça no tabuleiro na posição especificada."""
        
        # Verifica se a posição está dentro dos limites do tabuleiro
        if 0 <= linha < self.linhas and 0 <= coluna < self.colunas:
            # Verifica se já tem a peça nessa posição
            if self.estado_tabuleiro[linha][coluna] is not None:
                return False

            # Verifica se as peças fantasma da peça dic_fantasmas se encaixam na posição
            for pos in peca.dic_fantasmas[peca.formato]:
                pos_linha = linha + pos[0] - peca.ancora[0]
                pos_coluna = coluna + pos[1] - peca.ancora[1]
                print(f"Verificando posição fantasma ({pos_linha}, {pos_coluna})")
                if (pos_linha < 0 or pos_linha >= self.linhas or
                    pos_coluna < 0 or pos_coluna >= self.colunas or
                    self.estado_tabuleiro[pos_linha][pos_coluna] is not None):
                    return False
            
            
            print(f"Colocando peça {peca.tipo} {peca.formato} na posição ({linha}, {coluna})")
            self.estado_tabuleiro[linha][coluna] = peca
            
            # Coloca as peças fantasma no tabuleiro
            for pos in peca.dic_fantasmas[peca.formato]:
                pos_linha = linha + pos[0] - peca.ancora[0]
                pos_coluna = coluna + pos[1] - peca.ancora[1]
                self.estado_tabuleiro[pos_linha][pos_coluna] = Peca_Fantasma(peca)
            
            
            return True
        return False