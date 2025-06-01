import pygame
from tabuleiro import Tabuleiro
from peca import Peca
from caixa_selecao import Caixa_Selecao

class Jogo():

    def __init__(self):
        self.reset_partida()  # Inicializa o jogo com uma nova partida
        
    def reset_partida(self):
        self.tabuleiro = Tabuleiro(50, 40)                        # Inicializa o tabuleiro com a posição (50, 40)
        self.caixa_selecao = Caixa_Selecao(700, 40, 192, 192*3)   # Inicializa a caixa de seleção
        self.peca_selecionada = None
        self.max_score = 100
        self.score = 0                                            # Reseta o score
        self.vitoria = False

    def computar_pontos(self):
        """Ver todas as peças do tabuleiro e se for do tipo peca, soma os pontos."""
        pontos = 0
        for linha in self.tabuleiro.estado_tabuleiro:
            for peca in linha:
                if isinstance(peca, Peca):
                    pontos += peca.pontos
        return pontos

    def tick(self):
        """Atualiza o estado do jogo."""
        #if self.peca_selecionada != None:
        self.score = self.computar_pontos()  # Atualiza o score a cada tick
        # Verifica se o score atingiu o máximo
        if self.score >= self.max_score:
            self.vitoria = True
        
    def tela_vitoria(self, screen):
        """Mostra a tela de vitória dentro de um retângulo no centro do jogo e embaixo o botão de reiniciar."""
        largura = 400
        altura = 200
        x = (800 - largura) // 2
        y = (600 - altura) // 2

        # Desenhar fundo da tela de vitória
        pygame.draw.rect(screen, (255, 255, 255), (x, y, largura, altura))
        pygame.draw.rect(screen, (0, 0, 0), (x, y, largura, altura), 2)

        # Texto de vitória
        font = pygame.font.Font(None, 74)
        texto = font.render("Vitória!", True, (0, 255, 0))
        screen.blit(texto, (x + 100, y + 50))
    
    def barra_progresso(self, screen):
        # Configurações da barra de progresso
        barra_x = 100
        barra_y = 10
        barra_largura = 800
        barra_altura = 20

        # Calcula a largura da barra preenchida
        progresso = min(self.score / self.max_score, 1.0)  # impede ultrapassar 100%
        largura_preenchida = int(barra_largura * progresso)

        # Desenhar fundo da barra
        pygame.draw.rect(screen, (200, 200, 200), (barra_x, barra_y, barra_largura, barra_altura))

        # Desenhar parte preenchida
        pygame.draw.rect(screen, (0, 150, 0), (barra_x, barra_y, largura_preenchida, barra_altura))

        # Borda da barra
        pygame.draw.rect(screen, (0, 0, 0), (barra_x, barra_y, barra_largura, barra_altura), 2)

        # Texto centralizado
        font = pygame.font.Font(None, 24)
        texto_score = font.render(f"Score: {self.score}/{self.max_score}", True, (0, 0, 0))
        text_rect = texto_score.get_rect(center=(barra_x + barra_largura // 2, barra_y + barra_altura // 2))
        screen.blit(texto_score, text_rect)

    def render(self, screen):
        """Renderiza o jogo na tela."""
        
        # Fundo da tela
        screen.fill((255, 255, 255))
        
        if self.vitoria:
            self.tela_vitoria(screen)
            return
    
        self.barra_progresso(screen)
        
        # desenhar o tabuleiro
        self.tabuleiro.desenhar(screen)
        
        # localização da caixa de seleção
        self.caixa_selecao.desenhar(screen)
        
        # botão de reiniciar
        pygame.draw.rect(screen, (100, 0, 0), (10, 10, 80, 20))
        pygame.draw.rect(screen, (0, 0, 100), (10, 10, 80, 20), 1)
        # escrever "Reiniciar" no botão
        font = pygame.font.Font(None, 24)
        text = font.render("Reiniciar", True, (255, 255, 255))
        screen.blit(text, (15, 12))
        
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
            exit(0)
        
        # Detectar letra 'r' pressionada para reiniciar
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if self.peca_selecionada:
                    self.peca_selecionada.rotacionar()


        # capturar o clique esquerdo do mouse 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                
                pos_x, pos_y = event.pos
                
                # Verifica se o botão de reiniciar foi clicado
                if 10 <= pos_x <= 90 and 10 <= pos_y <= 30:
                    self.reset_partida()
                    return
                
                if self.peca_selecionada is None:
                    input_peca = self.caixa_selecao.input(pos_x, pos_y)

                    if input_peca:
                        self.peca_selecionada = input_peca
                    
                if self.peca_selecionada:
                    coord_tabuleiro= self.tabuleiro.get_coord_tabuleiro(pos_x, pos_y)
                    if coord_tabuleiro:
                        linha, coluna = coord_tabuleiro
                        if self.tabuleiro.colocar_peca(linha, coluna, self.peca_selecionada):
                            self.peca_selecionada = None
                            self.caixa_selecao.reset()