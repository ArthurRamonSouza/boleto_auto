import tkinter as tk
from tkinter import BooleanVar, filedialog

# Company standard colors
primary_color = '#E67E22'  # Orange
secondary_color = '#2ECC71'  # Green
bg_color = '#F8F9FA'  # Light Gray
text_color = '#2C3E50'  # Dark Blue

# RPA variables
interface_email_value = 'arthuramon.souza93@gmail.com'
interface_password_value = 'hzqr hvvr ifhm yfjh'
interface_invoice_path = '/home/arthur/Documents/Visual Studio Code/freela/engelmig/boleto_auto/download_folder'
interface_start_date = '2025/02/03'
interface_on_date = ''
interface_end_date = ''
unread_only = False

def set_rpa_var():
    global interface_email_value, interface_password_value, interface_invoice_path, interface_start_date, interface_on_date, interface_end_date, unread_only
    interface_email_value = email_entry.get() or interface_email_value
    interface_password_value = password_entry.get() or interface_password_value
    interface_invoice_path = invoice_path_entry.get() or interface_invoice_path
    interface_start_date = start_date_entry.get() or interface_start_date
    interface_on_date = on_date_entry.get() or interface_on_date
    interface_end_date = end_date_entry.get() or interface_end_date
    unread_only = unread_var.get() or unread_only

def get_login() -> tuple:
    return (interface_email_value, interface_password_value)

def get_download_folder_path() -> str:
    return interface_invoice_path

def get_filters() -> tuple:
    return (interface_start_date, interface_on_date, interface_end_date, unread_only)

def browse_folder() -> None:
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        invoice_path_entry.delete(0, tk.END)
        invoice_path_entry.insert(0, folder_selected)

def start_rpa() -> None:
    global root
    set_rpa_var()
    root.destroy()

# Main window
root = tk.Tk()
root.title('Leitor de Boleto')
root.geometry('450x600')
root.configure(bg=bg_color)

# Title
titulo = tk.Label(root, text='📜 Configurações do Leitor', font=('Arial', 18, 'bold'), fg=primary_color, bg=bg_color)
titulo.pack(pady=10)

# Function to create labels and entries dynamically
def create_labeled_entry(label_text, show=""):
    label = tk.Label(root, text=label_text, font=('Arial', 12, 'bold'), fg=text_color, bg=bg_color)
    label.pack()
    entry = tk.Entry(root, font=('Arial', 12), width=35, bd=2, relief='groove', show=show)
    entry.pack(pady=5)
    return entry

# Creating input fields
email_entry = create_labeled_entry('📧 Email:')
password_entry = create_labeled_entry('🔑 Senha:', show="*")
start_date_entry = create_labeled_entry('📅 Data de Início (YYYY/MM/DD):')
on_date_entry = create_labeled_entry('📍 Dia Específico (YYYY/MM/DD):')
end_date_entry = create_labeled_entry('⏳ Data de Fim (YYYY/MM/DD):')

# Unread emails checkbox
unread_var = BooleanVar()
unread_checkbox = tk.Checkbutton(root, text='📩 Somente emails não lidos', variable=unread_var, font=('Arial', 12), 
                                 fg=primary_color, bg=bg_color, selectcolor=bg_color)
unread_checkbox.pack(pady=5)

# Invoice Path label
invoice_path_label = tk.Label(root, text='📂 Caminho da Pasta dos Boletos:', font=('Arial', 12, 'bold'), fg=text_color, bg=bg_color)
invoice_path_label.pack()
invoice_path_entry = tk.Entry(root, font=('Arial', 12), width=35, bd=2, relief='groove')
invoice_path_entry.pack(pady=5)

# Browse button for folder selection
browse_btn = tk.Button(root, text='📁 Selecionar Pasta', font=('Arial', 12, 'bold'), fg='white', bg=secondary_color, 
                       width=20, height=1, bd=0, relief='flat', cursor='hand2', command=browse_folder)

browse_btn.pack(pady=5)

# Button hover effects
def on_enter(e):
    e.widget.config(bg='#27AE60')  # Darker green

def on_leave(e):
    e.widget.config(bg=secondary_color)

browse_btn.bind('<Enter>', on_enter)
browse_btn.bind('<Leave>', on_leave)

# Start button
start_btn = tk.Button(root, text='🚀 Iniciar', font=('Arial', 14, 'bold'), fg='white', bg=primary_color, 
                      width=20, height=1, bd=0, relief='flat', cursor='hand2', command=start_rpa)

start_btn.pack(pady=20)

# Button hover effects
def on_enter_start(e):
    e.widget.config(bg='#D35400')  # Darker orange

def on_leave_start(e):
    e.widget.config(bg=primary_color)

start_btn.bind('<Enter>', on_enter_start)
start_btn.bind('<Leave>', on_leave_start)

# Footer
rodape = tk.Label(root, text='📡 Engelmig Energia © 2025', font=('Arial', 10, 'bold'), fg=primary_color, bg=bg_color)
rodape.pack(side='bottom', pady=10)