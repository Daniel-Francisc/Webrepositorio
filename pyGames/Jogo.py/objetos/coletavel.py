import random


class Coletavel:
    def __init__(self, x, y, valor=10):
        self.x = x
        self.y = y

        self.largura = 25
        self.altura = 25

        self.valor = valor
        self.destruido = False

    @staticmethod
    def posicao_aleatoria(
        largura_tela,
        altura_tela,
        limite_inferior=None,
        margem=50
    ):
        limite_x = largura_tela - 25
        limite_y = (
            limite_inferior - margem - 25
            if limite_inferior is not None
            else altura_tela - 25
        )

        if limite_x < 0 or limite_y < 0:
            raise ValueError(
                "O objeto é maior que a área disponível para nascimento."
            )

        return (
            random.randint(0, limite_x),
            random.randint(0, limite_y)
        )
