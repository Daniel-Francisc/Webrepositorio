import random


class LocalPouso:
    def __init__(self, x, y, largura=400, altura=25):
        self.x = x
        self.y = y

        self.largura = largura
        self.altura = altura

    @staticmethod
    def posicao_aleatoria(largura_tela, largura_plataforma=400):
        limite_x = largura_tela - largura_plataforma

        if limite_x < 0:
            raise ValueError(
                "A plataforma é maior que a largura disponível da tela."
            )

        return random.randint(0, limite_x)
