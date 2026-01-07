def error_message_box(message: str):
    """
    Display a modal error dialog with the given message.
    
    Shows a Tkinter error message box titled "Erro" using a hidden root window.
    
    Parameters:
        message (str): Text to display in the error dialog.
    """
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk() # Criar a janela principal (pode ficar oculta)
    root.withdraw()  # Esconde a janela principal
    messagebox.showerror("Erro", message)
    root.destroy()
    return