import pygame
from src.peca import Peca_Fantasma

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
        
    def encontrar_vizinhos_pai_unicos(self, peca):
        """Encontra vizinhos únicos da peça, considerando apenas as peças originais (pais)."""
        vizinhos = set()
        
        todas_pos = peca.dic_fantasmas[peca.formato].copy()  # Copia as posições dos fantasmas
        todas_pos.append(peca.ancora)  # Adiciona a âncora para verificar a posição original da peça

        for pos in todas_pos:
            pos_linha = peca.pos[0] + pos[0] - peca.ancora[0]
            pos_coluna = peca.pos[1] + pos[1] - peca.ancora[1]

            for i in range(-1, 2):  # Verifica as posições adjacentes
                for j in range(-1, 2):
                    if abs(i+j) != 1:  # Verifica apenas vizinhanca 4
                        continue
                    pos_linha_adj = pos_linha + i
                    pos_coluna_adj = pos_coluna + j
                    # print("ver", pos_linha_adj, pos_coluna_adj, end=" ")
                    if (0 <= pos_linha_adj < self.linhas and 0 <= pos_coluna_adj < self.colunas):
                        vizinho = self.estado_tabuleiro[pos_linha_adj][pos_coluna_adj]
                        if vizinho is not None:
                            vizinhos.add(vizinho.peca_pai)
        
        # # Remove a própria peça para evitar que ela seja considerada como vizinha
        if peca in vizinhos:
            vizinhos.remove(peca)

        return list(vizinhos)

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
            if self.estado_tabuleiro[linha][coluna] is not None and peca.tipo != "bomba":
                return False

            # Verifica se as peças fantasma da peça dic_fantasmas se encaixam na posição
            for pos in peca.dic_fantasmas[peca.formato]:
                pos_linha = linha + pos[0] - peca.ancora[0]
                pos_coluna = coluna + pos[1] - peca.ancora[1]
                if (pos_linha < 0 or pos_linha >= self.linhas or
                    pos_coluna < 0 or pos_coluna >= self.colunas or
                    self.estado_tabuleiro[pos_linha][pos_coluna] is not None):
                    if peca.tipo != "bomba":
                        return False
            
            if peca.tipo == "bomba":
                if self.estado_tabuleiro[linha][coluna] is not None:
                    alvo = self.estado_tabuleiro[linha][coluna].peca_pai
                    for fantasma in alvo.fantasmas:
                        self.estado_tabuleiro[fantasma.pos[0]][fantasma.pos[1]] = None
                    self.estado_tabuleiro[alvo.pos[0]][alvo.pos[1]] = None

                    self.estado_tabuleiro[linha][coluna] = None
            else:
                # Coloca a peça original no tabuleiro
                self.estado_tabuleiro[linha][coluna] = peca
                peca.set_posicao((linha, coluna))
            
            # Coloca as peças fantasma no tabuleiro
            for pos in peca.dic_fantasmas[peca.formato]:
                pos_linha = linha + pos[0] - peca.ancora[0]
                pos_coluna = coluna + pos[1] - peca.ancora[1]
                if peca.tipo == "bomba":
                    if not (0 <= pos_linha < self.linhas and 0 <= pos_coluna < self.colunas):
                        continue
                    alvo = self.estado_tabuleiro[pos_linha][pos_coluna]
                    if alvo is None:
                        continue
                    alvo_pai = alvo.peca_pai
                    for fantasma in alvo_pai.fantasmas:
                        self.estado_tabuleiro[fantasma.pos[0]][fantasma.pos[1]] = None
                    self.estado_tabuleiro[alvo_pai.pos[0]][alvo_pai.pos[1]] = None
                else:
                    self.estado_tabuleiro[pos_linha][pos_coluna] = Peca_Fantasma(peca, (pos_linha, pos_coluna))
            
            
            return True
        return False
    
    def remover_peca(self, linha, coluna):
        """Remove a peça (e seus fantasmas) da posição especificada."""
        peca = self.estado_tabuleiro[linha][coluna]
        
        if peca is None:
            return False

        # Se clicou num fantasma, encontrar a peça original
        if hasattr(peca, "original"):
            peca = peca.original

        # Verifica se é uma peça do tipo Peca
        if not hasattr(peca, "dic_fantasmas") or not hasattr(peca, "formato"):
            return False

        # Remover a peça e seus fantasmas do tabuleiro
        for pos in peca.dic_fantasmas[peca.formato]:
            pos_linha = peca.pos_linha + pos[0] - peca.ancora[0]
            pos_coluna = peca.pos_coluna + pos[1] - peca.ancora[1]
            if (0 <= pos_linha < self.linhas and 0 <= pos_coluna < self.colunas):
                self.estado_tabuleiro[pos_linha][pos_coluna] = None

        return True
