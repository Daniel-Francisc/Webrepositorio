import tkinter as tk

class Tela:
    def __init__(self,debug = True, titulo = "pygames"):
        self.debug = debug
        self.janela = tk.Tk()
        self.janela.title(titulo)
        
        self.largura = self.janela.winfo_screenwidth()
        self.altura = self.janela.winfo_screenheight()
        
        self.janela.geometry(f"{self.largura}x{self.altura}")
        
        self.canvas = tk.Canvas( 
            self.janela, 
            width=self.largura,
            height=self.altura, 
            bg="black", 
            highlightthickness=0 
        )
        self.canvas.pack()
        
    def atualizar(self): pass
    def desenhar(self): self.canvas.delete("all")
    
    def executar(self): 
        self.atualizar()
        self.desenhar()
        
        self.janela.after(16, self.executar) 
        self.janela.mainloop()