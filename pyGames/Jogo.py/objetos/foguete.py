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

    def verificar_coleta(self, coletavel):
        if coletavel.destruido:
            return

        if place_meeting(
            self,
            self.x,
            self.y,
            coletavel
        ):
            self.pontos += coletavel.valor
            coletavel.destruido = True
            
    def atualizar(self, input, dT, largura_tela, altura_tela, local_pouso=None):

        x_anterior = self.x
        y_anterior = self.y

        if input.pressionada("Left"):
            self.x -= 200 * dT

        if input.pressionada("Right"):
            self.x += 200 * dT

        if input.pressionada("Up"):
            self.y -= 200 * dT

        if input.pressionada("Down"):
            self.y += 200 * dT

        # Wrap horizontal
        if self.x + self.largura < 0:
            self.x = largura_tela

        elif self.x > largura_tela:
            self.x = -self.largura

        # Wrap vertical
        if self.y + self.altura < 0:
            self.y = altura_tela

        elif self.y > altura_tela:
            self.y = -self.altura

        self.colidindo = False

        if local_pouso is not None:

            if place_meeting(
                self,
                self.x,
                self.y,
                local_pouso
            ):
                self.x = x_anterior
                self.y = y_anterior
                self.colidindo = True
        