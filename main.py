# Bibliotecas e Importações
from src.motor import Coracao
import asyncio

# Inicialização do jogo
if __name__ == "__main__":
    game = Coracao()
    asyncio.run(game.run())