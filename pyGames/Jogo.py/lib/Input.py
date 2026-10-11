class Input:
    """Registra teclas mesmo quando o Canvas está com o foco."""

    def __init__(self, janela):
        self.teclas = set()
        self.janela = janela

        # Bind global evita perder as teclas quando o foco está no Canvas.
        janela.bind_all("<KeyPress>", self.tecla_pressionada)
        janela.bind_all("<KeyRelease>", self.tecla_liberada)

        # O jogo recebe foco assim que a janela abre.
        janela.after(100, janela.focus_force)

    def tecla_pressionada(self, evento):
        self.teclas.add(evento.keysym.lower())

    def tecla_liberada(self, evento):
        self.teclas.discard(evento.keysym.lower())

    def pressionada(self, tecla):
        return tecla.lower() in self.teclas
