import pygame

class Peca():
    
    todas_pecas = ["+", "0", "c", "i", "l", "lzao", "o", "s", "t", "b"]
    dic_ancora_padrao = {
        "+":    [1, 1],
        "0":    [1, 1],
        "c":    [1, 1],
        "i":    [1, 0],
        "l":    [0, 0],
        "lzao": [1, 1],
        "o":    [0, 0],
        "s":    [1, 1],
        "t":    [1, 1],
        "b":    [1, 1]
    }
    
    dic_fantasmas_padrao = {
        "+":    [[0,1], [1,0], [1,2], [2,1]],
        "0":    [[0,0], [0,1], [0,2], [1,0], [1,2], [2,0], [2,1], [2,2]],
        "c":    [[0,0], [0,1], [2,0], [2,1]],   
        "i":    [[0,0], [2,0]],
        "l":    [[0,1], [1,0]],
        "lzao": [[0,0], [0,1], [2,1]],
        "o":    [[0,1], [1,0], [1,1]],
        "s":    [[0,0], [1,0], [2,1]],
        "t":    [[0,0], [1,0], [2,0]],
        "b":    [[0,0], [0,1], [0,2], [1,0], [1,2], [2,0], [2,1], [2,2]] 
    }
    
    dic_tipos = {
        "+": ["fogueira", "igreja", "banda"],
        "0": ["quadrilha", "fogueira", "cobra"],
        "c": ["jogo", "comida", "banda", "cobra"],
        "i": ["comida", "sebo", "cobra"],
        "l": ["jogo", "comida", "correio"],
        "lzao": ["jogo", "comida", "cobra"],
        "o": ["quadrilha", "fogueira"],
        "s": ["jogo", "banda", "cobra"],
        "t": ["jogo", "comida", "correio", "cobra"],
        "b": ["bomba"]
    }
    

    dic_bem_com = {

        "quadrilha": ["fogueira"],
        "fogueira": ["fogueira"],
        "jogo": ["comida"],
        "comida": ["jogo"],
        "igreja": ["quadrilha"],
        "banda": ["quadrilha"],
        "correio": ["igreja"],
        "sebo": ["jogo"],
        "cinza": []
    }




    def negar(self, x):
        """Inverte as coordenadas de um fantasma."""
        if x == 0:
            return 2
        elif x == 1:
            return 1
        elif x == 2:
            return 0
        else:
            raise ValueError("Coordenada inválida. Deve ser 0, 1 ou 2.")

    def rotacionar(self):
        self.dic_fantasmas[self.formato] = [[y, self.negar(x)] for x, y in self.dic_fantasmas[self.formato]]
        self.ancora = [self.ancora[1], self.negar(self.ancora[0])]

        self.image = pygame.transform.rotate(self.image, - 90)
    
    def anti_rotacionar(self):
        self.dic_fantasmas[self.formato] = [[self.negar(y), x] for x, y in self.dic_fantasmas[self.formato]]
        self.ancora = [self.negar(self.ancora[1]), self.ancora[0]]
        self.image = pygame.transform.rotate(self.image, +90)

    def __init__(self, formato, tipo):
        self.tipo = tipo
        self.formato = formato
        if formato == "b":
            self.tipo = "bomba"
        self.dic_fantasmas = self.dic_fantasmas_padrao.copy()
        self.dic_ancora = self.dic_ancora_padrao.copy()
        self.image = None
        self.ancora = self.dic_ancora[self.formato]
        self.pontos = len(self.dic_fantasmas[self.formato])+1
        self.pos = None
        self.peca_pai = self
        self.carregar_imagem()

    def definir_tipo(self, tipo):
        """Define o tipo da peça e carrega a imagem correspondente."""
        if tipo not in self.dic_tipos[self.formato]:
            raise ValueError(f"Tipo '{tipo}' não é válido para o formato '{self.formato}'.")
        self.tipo = tipo
        if self.tipo == "cobra":
            self.pontos = abs(self.pontos) * -1
        self.carregar_imagem()

    def set_posicao(self, pos):
        """Define a posição da peça."""
        self.pos = pos
        
    def add_fantasma(self, fantasma):
        """Adiciona um fantasma à peça."""
        if not hasattr(self, 'fantasmas'):
            self.fantasmas = []
        self.fantasmas.append(fantasma)

    def carregar_imagem(self):
        """Carrega a imagem da peça com base no tipo."""
        try:
            self.image = pygame.image.load(f"images/{self.formato}/{self.tipo}.png")
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
    def __init__ (self, peca, pos):
        self.peca_pai = peca
        peca.add_fantasma(self)
        self.set_posicao(pos)
        
    def desenhar(self, screen, pos_x, pos_y):
        pass
    
    def tick(self):
        pass

    def set_posicao(self, pos):
        """Define a posição da peça."""
        self.pos = pos