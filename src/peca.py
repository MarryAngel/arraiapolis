import pygame

class Peca():
    
    todas_pecas = ["+", "0", "c", "i", "l", "lzao", "o", "s", "t"]
    dic_ancora = {
        "+":    [1, 1],
        "0":    [1, 1],
        "c":    [1, 1],
        "i":    [1, 0],
        "l":    [0, 0],
        "lzao": [1, 1],
        "o":    [0, 0],
        "s":    [1, 1],
        "t":    [1, 1]
    }
    
    def __init__(self, formato, tipo):
        self.tipo = tipo
        self.formato = formato
        self.image = None
        self.ancora = self.dic_ancora[self.formato]
        self.carregar_imagem()
        
    def carregar_imagem(self):
        """Carrega a imagem da peça com base no tipo."""
        try:
            self.image = pygame.image.load(f"../images/{self.formato}/{self.tipo}.png").convert_alpha()
        except pygame.error as e:
            print(f"Erro ao carregar a imagem da peça {self.formato}/{self.tipo}.png: {e}")
            self.image = None
            
    def desenhar(self, screen, pos_x, pos_y):
        """Desenha a peça na tela."""
        if self.image:
            screen.blit(self.image, (pos_x-self.ancora[1]*64, pos_y-self.ancora[0]*64))
            
    def desenhar_bruto(self, screen, pos_x, pos_y):
        """Desenha a peça na tela."""
        if self.image:
            screen.blit(self.image, (pos_x, pos_y))