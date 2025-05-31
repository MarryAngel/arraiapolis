import pygame

class Caixa_Selecao:
    
    def __init__(self, pos_x, pos_y, largura, altura):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.largura = largura
        self.altura = altura
        self.margem = 10
        
        # Cores
        self.cor_fundo = (100, 0, 0)
        self.cor_borda = (0, 0, 100)
        
    def desenhar(self, screen):
        pygame.draw.rect(screen, self.cor_fundo, (self.pos_x, self.pos_y, self.largura + 2 * self.margem, self.altura + 4 * self.margem))
        pygame.draw.rect(screen, self.cor_borda, (self.pos_x, self.pos_y, self.largura + 2 * self.margem, self.altura + 4 * self.margem), 1)