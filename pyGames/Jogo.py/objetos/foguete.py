from lib.Colisao import place_meeting


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

        self.colidindo = False

    def atualizar(self, input, dT, largura_tela, altura_tela, objeto_colisao=None):

        if input.pressionada("Left"):
            self.x -= 200 * dT

        if input.pressionada("Right"):
            self.x += 200 * dT

        if input.pressionada("Up"):
            self.y -= 200 * dT

        if input.pressionada("Down"):
            self.y += 200 * dT

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

        # Verifica colisão com o objeto informado
        if objeto_colisao is not None:
            self.colidindo = place_meeting(
                self,
                self.x,
                self.y,
                objeto_colisao
            )

            if self.colidindo:
                self.y = objeto_colisao.y - self.altura
                self.velocidade_y = 0
        else:
            self.colidindo = False
