def error_message_box(message: str):
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk() # Criar a janela principal (pode ficar oculta)
    root.withdraw()  # Esconde a janela principal
    messagebox.showerror("Erro", message)
    root.destroy()
    return