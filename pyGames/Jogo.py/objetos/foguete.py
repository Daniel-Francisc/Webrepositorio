class Foguete:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.largura = 50
        self.altura = 50

        self.velocidade_x = 0
        self.velocidade_y = 0

        self.massa = 1
        self.energia = 0

    def atualizar(self, largura_tela, altura_tela):
        self.x += self.velocidade_x
        self.y += self.velocidade_y

        # Saiu pela esquerda
        if self.x + self.largura < 0:
            self.x = largura_tela

        # Saiu pela direita
        elif self.x > largura_tela:
            self.x = -self.largura

        # Saiu pelo topo
        if self.y + self.altura < 0:
            self.y = altura_tela

        # Saiu pela parte inferior
        elif self.y > altura_tela:
            self.y = -self.altura