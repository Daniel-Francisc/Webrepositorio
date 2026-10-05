class Input:
    def __init__(self, janela):
        self.teclas = set()

        janela.bind("<KeyPress>", self.tecla_pressionada)
        janela.bind("<KeyRelease>", self.tecla_liberada)

    def tecla_pressionada(self, evento):
        self.teclas.add(evento.keysym)

    def tecla_liberada(self, evento):
        self.teclas.discard(evento.keysym)

    def pressionada(self, tecla):
        return tecla in self.teclas