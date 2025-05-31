import pygame

class Peca():
    
    def __init__(self, formato, tipo):
        self.tipo = tipo
        self.formato = formato
        self.image = None
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
            screen.blit(self.image, (pos_x, pos_y))