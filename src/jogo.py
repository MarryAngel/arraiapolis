import pygame
from src.tabuleiro import Tabuleiro
from src.peca import Peca, Peca_Fantasma
from src.caixa_selecao import Caixa_Selecao
import threading
import random

class Jogo():

    def __init__(self):
        self.reset_partida()  # Inicializa o jogo com uma nova partida
        
    def tocar(self, tipo, nome = None, pararFundo=False):
        if tipo == "background":
            if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()

            def tocar_musica():
                pygame.mixer.init()
                pygame.mixer.music.load("audio/musica.mp3")
                pygame.mixer.music.set_volume(0.05)  # Define o volume para 5%
                pygame.mixer.music.play(-1)  # Loop infinito
            self.musica_thread = threading.Thread(target=tocar_musica, daemon=True)
            self.musica_thread.start()
        elif tipo == "peca":
            if pararFundo and pygame.mixer.get_init() and pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()

            if pygame.mixer.get_init():
                    pygame.mixer.Sound(f"audio/{nome}.mp3").play()

        elif tipo == "nada":
            if pararFundo:
                # Para toda música de fundo e efeitos sonoros em andamento
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                # Para todos os canais de efeitos sonoros
                for i in range(pygame.mixer.get_num_channels()):
                    pygame.mixer.Channel(i).stop()

    def reset_partida(self):
        self.tocar("nada", pararFundo=True)  # Para a música de fundo antes de reiniciar

        self.tabuleiro = Tabuleiro(50, 40)                        # Inicializa o tabuleiro com a posição (50, 40)
        self.caixa_selecao = Caixa_Selecao(700, 40, 192, 192*3)   # Inicializa a caixa de seleção
        self.peca_selecionada = None
        self.max_score_easy = 90
        self.max_score_hard = 180
        self.score = 0                                            # Reseta o score
        self.vitoria = False
        self.tocar("background")                                 # Toca a música de fundo
        self.hard = False                                        # Reseta o modo hard
        

    def computar_pontos(self):
        """Ver todas as peças do tabuleiro e se for do tipo peca, soma os pontos."""
        pontos = 0
        for linha in self.tabuleiro.estado_tabuleiro:
            for peca in linha:
                if peca is None or isinstance(peca, Peca_Fantasma):
                    continue
                if isinstance(peca, Peca):
                    pontos += peca.pontos

                if peca.tipo == "cobra":
                    continue
                vizinhos_pai = self.tabuleiro.encontrar_vizinhos_pai_unicos(peca)
                

                for vizinho in vizinhos_pai:
                    if vizinho.tipo == "cobra":
                        pontos -=1
                    elif vizinho.tipo in peca.dic_bem_com[peca.tipo]:
                        pontos += 1

        return pontos

    def tick(self):
        """Atualiza o estado do jogo."""
        #if self.peca_selecionada != None:
        self.score = self.computar_pontos()  # Atualiza o score a cada tick
        # Verifica se o score atingiu o máximo
        maximo = self.max_score_hard if self.hard else self.max_score_easy
        if self.score >= maximo:
            if not self.vitoria:
                self.tocar("peca", "vitoria", pararFundo=True)
            self.vitoria = True
        
    def tela_vitoria(self, screen):
        """Mostra a tela de vitória dentro de um retângulo no centro do jogo e embaixo o botão de reiniciar."""
        largura = 400
        altura = 200
        x = (800 - largura) // 2
        y = (600 - altura) // 2


        # Texto de vitória
        font = pygame.font.Font(None, 274)
        texto = font.render("Vitória!", True, (0, 255, 0))
        screen.blit(texto, (x- 100, y + 50))
    
    def barra_progresso(self, screen):
        # Configurações da barra de progresso
        barra_x = 100
        barra_y = 10
        barra_largura = 800
        barra_altura = 20

        maximo = self.max_score_hard if self.hard else self.max_score_easy
        # Calcula a largura da barra preenchida
        progresso = min(self.score / maximo, 1.0)  # impede ultrapassar 100%
        largura_preenchida = int(barra_largura * progresso)

        # Desenhar fundo da barra
        pygame.draw.rect(screen, (200, 200, 200), (barra_x, barra_y, barra_largura, barra_altura))

        # Desenhar parte preenchida
        pygame.draw.rect(screen, (0, 150, 0), (barra_x, barra_y, largura_preenchida, barra_altura))

        # Borda da barra
        pygame.draw.rect(screen, (0, 0, 0), (barra_x, barra_y, barra_largura, barra_altura), 2)

        # Texto centralizado
        font = pygame.font.Font(None, 24)
        texto_score = font.render(f"Score: {self.score}/{maximo}", True, (0, 0, 0))
        text_rect = texto_score.get_rect(center=(barra_x + barra_largura // 2, barra_y + barra_altura // 2))
        screen.blit(texto_score, text_rect)


    def desenhar_hard(self, screen):
        # Botão estilo interruptor "difici dimais" (vertical)
        interruptor_x = 920
        interruptor_y = 40
        interruptor_largura = 56   # largura do interruptor vertical
        interruptor_altura = 140   # altura aumentada para vertical

        # Cor do interruptor dependendo do estado
        cor_interruptor = (180, 0, 0) if self.hard else (0, 180, 0)
        pygame.draw.rect(screen, cor_interruptor, (interruptor_x, interruptor_y, interruptor_largura, interruptor_altura), border_radius=20)
        pygame.draw.rect(screen, (0, 0, 0), (interruptor_x, interruptor_y, interruptor_largura, interruptor_altura), 2, border_radius=20)

        # Círculo deslizante do interruptor (centralizado horizontalmente)
        circulo_x = interruptor_x + (interruptor_largura - 40) // 2
        circulo_y = interruptor_y + (8 if self.hard else interruptor_altura - 50)
        pygame.draw.ellipse(screen, (255, 255, 255), (circulo_x, circulo_y, 40, 40))

        # Texto do botão (centralizado horizontalmente)
        font = pygame.font.Font(None, 28)
        texto1 = font.render("Danado", True, (255, 0, 0))
        texto2 = font.render("Diboa", True, (10, 180, 30))
        
        # Centraliza os textos na largura do interruptor
        text1_rect = texto1.get_rect(center=(interruptor_x + interruptor_largura // 2, interruptor_y + -10))
        text2_rect = texto1.get_rect(center=(interruptor_x + interruptor_largura // 2+10, interruptor_y + +150))
        screen.blit(texto1, text1_rect)
        screen.blit(texto2, text2_rect)

    def render(self, screen):
        """Renderiza o jogo na tela."""
        
        # Fundo da tela
        screen.fill((255, 255, 255))
        
    
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
        
        self.desenhar_hard(screen)  # Desenha o botão de dificuldade

        # desenhar a peça selecionada
        if self.peca_selecionada:
            pos_x = pygame.mouse.get_pos()[0] # Centraliza a peça no mouse
            pos_y = pygame.mouse.get_pos()[1] # Centraliza a peça no mouse
            self.peca_selecionada.desenhar(screen, pos_x-32, pos_y-32)
        
        if self.vitoria:
            self.tela_vitoria(screen)

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
                    venceu = self.vitoria
                    self.reset_partida()
                    if not venceu:
                        self.tocar("peca", "reset", pararFundo=True)
                    return
                
                # Verifica se o botão de dificuldade foi clicado
                if 920 <= pos_x <= 976 and 40 <= pos_y <= 180:
                    self.hard = not self.hard
                    self.tocar("peca", "colocar")

                if self.vitoria:
                    return
                
                if self.peca_selecionada is None:
                    input_peca = self.caixa_selecao.input(pos_x, pos_y)

                    if input_peca:
                        self.peca_selecionada = input_peca

                        input_peca.definir_tipo(random.choice(input_peca.dic_tipos[input_peca.formato]))

                        if input_peca.tipo != "cinza":
                            self.tocar("peca", input_peca.tipo)
                    
                if self.peca_selecionada:
                    coord_tabuleiro= self.tabuleiro.get_coord_tabuleiro(pos_x, pos_y)
                    if coord_tabuleiro:
                        linha, coluna = coord_tabuleiro
                        if self.tabuleiro.colocar_peca(linha, coluna, self.peca_selecionada):
                            if self.peca_selecionada.tipo != "bomba":
                                self.tocar("peca", "colocar")
                            else:
                                self.tocar("peca", "estalinho")
                            self.peca_selecionada = None
                            self.caixa_selecao.reset()