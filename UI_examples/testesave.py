import tkinter as tk
from tkinter import messagebox

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("App com Alerta de Salvar")

        self.text_widget = tk.Text(root)
        self.text_widget.pack(fill=tk.BOTH, expand=True)

        # Controlar se houve alterações no texto
        self.text_changed = False

        # Adicionar evento quando o texto é modificado
        self.text_widget.bind("<Key>", self.on_text_change)

        # Adicionar evento ao fechar a janela
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_text_change(self, event):
        self.text_changed = True

    def on_close(self):
        if self.text_changed:
            # Mostrar um alerta de confirmação
            result = messagebox.askyesnocancel("Salvar", "Deseja salvar as alterações antes de sair?")
            
            if result is None:  # Clicou em "Cancelar"
                return
            elif result:  # Clicou em "Sim"
                self.save_changes()
            
        self.root.destroy()

    def save_changes(self):
        # Lógica para salvar as alterações
        # Por exemplo, você pode abrir um diálogo de salvar arquivo
        # ou salvar automaticamente em um local predefinido.
        # Aqui, estou apenas imprimindo uma mensagem.
        print("Alterações salvas!")

root = tk.Tk()
app = MyApp(root)
root.mainloop()
