def place_meeting(self, x, y, objeto):
    return (
        x < objeto.x + objeto.largura
        and x + self.largura > objeto.x
        and y < objeto.y + objeto.altura
        and y + self.altura > objeto.y
    )