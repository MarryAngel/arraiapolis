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
    
    dic_fantasmas = {
        "+":    [[0,1], [1,0], [1,2], [2,1]],
        "0":    [[0,0], [0,1], [0,2], [1,0], [1,2], [2,0], [2,1], [2,2]],
        "c":    [[0,0], [0,1], [2,0], [2,1]],   
        "i":    [[0,0], [2,0]],
        "l":    [[0,1], [1,0]],
        "lzao": [[0,0], [0,1], [2,1]],
        "o":    [[0,1], [1,0], [1,1]],
        "s":    [[0,0], [1,0], [2,1]],
        "t":    [[0,0], [1,0], [2,0]]
    }
    
    dic_tipos2 = {
        "+": ["fogueira", "igreja", "banda", "cobra"],
        "0": ["quadrilha", "fogueira", "cobra"],
        "c": ["jogo", "comida", "banda", "cobra"],
        "i": ["comida", "sebo", "cobra"],
        "l": ["jogo", "comida", "cobra", "correio"],
        "lzao": ["jogo", "comida", "cobra"],
        "o": ["quadrilha", "fogueira", "cobra"],
        "s": ["jogo", "banda", "cobra"],
        "t": ["jogo", "comida", "correio", "cobra"]
    }
    
    # dic_tipos com tudo cinza
    dic_tipos = {
        "+": ["cinza"],
        "0": ["quadrilha", "fogueira", "cobra"],
        "c": ["cinza"],
        "i": ["cinza"],
        "l": ["cinza"],
        "lzao": ["cinza"],
        "o": ["cinza"],
        "s": ["cinza"],
        "t": ["cinza"]
    }
    
    
    dic_formato = {
        "0": [],
        "c": [],
        "i": [],
        "l": [],
        "lzao": [],
        "o": [],
        "s": [],
        "t": []
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
            
class Peca_Fantasma():
    def __init__ (self, peca):
        self.peca_pai = peca
        
    def desenhar(self, screen, pos_x, pos_y):
        pass
    
    def tick(self):
        pass