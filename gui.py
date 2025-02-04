import tkinter as tk
from tkinter import filedialog

# Company standart colors
primary_color: str = '#E59933'  # Orange
secondary_color: str = '#D1F050'  # Light green
bg_color: str = '#ffffff'  # White

# RPA variables
interface_email_value: str = 'arthuramon.souza93@gmail.com'
interface_password_value: str = 'hzqr hvvr ifhm yfjh '
interface_invoice_path: str = './boletos_lidos'

def set_rpa_var() -> None:
    global interface_email_value, interface_password_value, interface_invoice_path
    interface_email_value = email_entry.get()
    interface_password_value = password_entry.get()
    interface_invoice_path = invoice_path_entry.get()

def get_login() -> tuple:
    return (interface_email_value, interface_password_value)

def browse_folder() -> None:
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        invoice_path_entry.delete(0, tk.END)  # Clear the current entry
        invoice_path_entry.insert(0, folder_selected)

# Main window
root: tk.Tk = tk.Tk()
root.title('Leitor de Boleto')
root.geometry('400x400')
root.configure(bg=bg_color)

# Title
titulo: tk.Label = tk.Label(root, text='Login', font=('Arial', 18, 'bold'), fg=primary_color, bg=bg_color)
titulo.pack(pady=10)

# Email label
email_label: tk.Label = tk.Label(root, text='Email:', font=('Arial', 12), fg=primary_color, bg=bg_color)
email_label.pack()
email_entry: tk.Entry = tk.Entry(root, font=('Arial', 12), width=30, bd=2, relief='groove')
email_entry.pack(pady=5)

# Password label
password_label: tk.Label = tk.Label(root, text='Senha:', font=('Arial', 12), fg=primary_color, bg=bg_color)
password_label.pack()
password_entry: tk.Entry = tk.Entry(root, font=('Arial', 12), width=30, bd=2, relief='groove', show='*')
password_entry.pack(pady=5)

# Invoice Path label
invoice_path_label: tk.Label = tk.Label(root, text='Caminho da Pasta dos Boletos:', font=('Arial', 12), fg=primary_color, bg=bg_color)
invoice_path_label.pack()
invoice_path_entry: tk.Entry = tk.Entry(root, font=('Arial', 12), width=30, bd=2, relief='groove')
invoice_path_entry.pack(pady=5)

# Browse button for folder selection
browse_btn: tk.Button = tk.Button(root, text='Selecionar Pasta', font=('Arial', 12), fg='#ffffff', bg=secondary_color, 
                                  width=15, height=1, bd=0, relief='flat', command=browse_folder)
browse_btn.pack(pady=5)

# Start button
login_btn: tk.Button = tk.Button(root, text='Iniciar', font=('Arial', 12, 'bold'), fg='#ffffff', bg=primary_color, 
                      width=15, height=1, bd=0, relief='flat')
login_btn.pack(pady=15)

# Footer
rodape: tk.Label = tk.Label(root, text='Engelmig Energia', font=('Arial', 10), fg=primary_color, bg=bg_color)
rodape.pack(side='bottom', pady=10)