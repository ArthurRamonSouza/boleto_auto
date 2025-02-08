import os
import sys
import tkinter as tk
from datetime import datetime
from dotenv import load_dotenv
from tkinter import BooleanVar, filedialog

# Company standard colors
# Primary color (orange), secondary color (green), background color (light gray), and text color (dark blue)
primary_color = '#E67E22'  # Orange
secondary_color = '#2ECC71'  # Green
bg_color = '#F8F9FA'  # Light Gray
text_color = '#2C3E50'  # Dark Blue

# RPA (Robotic Process Automation) variables to store user inputs and settings
load_dotenv()
interface_email_value = os.getenv('EMAIL_LOGIN')
interface_password_value = os.getenv('EMAIL_PASSWORD')
interface_invoice_path = os.getenv('FOLDER_PATH')
interface_start_date = datetime.now().strftime('%Y/%m/%d')

interface_on_date = ''
interface_end_date = ''
unread_only = False


def set_rpa_var():
    """
    This function sets the values of the RPA-related variables based on the user inputs
    from the corresponding entry fields. If no new value is provided, the global variable
    retains its previous value.
    """
    global interface_email_value, interface_password_value, interface_invoice_path, interface_start_date, interface_on_date, interface_end_date, unread_only
    interface_email_value = email_entry.get() or interface_email_value
    interface_password_value = password_entry.get() or interface_password_value
    interface_invoice_path = invoice_path_entry.get() or interface_invoice_path
    interface_start_date = start_date_entry.get() or interface_start_date
    interface_on_date = on_date_entry.get() or interface_on_date
    interface_end_date = end_date_entry.get() or interface_end_date
    unread_only = unread_var.get() or unread_only

def on_closing():
    """
    This function is triggered when the window is closed.
    It ensures that the application exits gracefully.
    """
    sys.exit()

def get_interface_login() -> tuple:
    """
    Returns the email and password stored in the interface's login fields as a tuple.
    """
    return (interface_email_value, interface_password_value)

def get_interface_download_folder_path() -> str:
    """
    Returns the file path of the folder selected for storing the invoices.
    """
    return interface_invoice_path

def get_interface_filters() -> tuple:
    """
    Returns a tuple with the selected filters: start date, on date, end date, and unread-only flag.
    """
    return (interface_start_date, interface_on_date, interface_end_date, unread_only)

def browse_folder() -> None:
    """
    Opens a file dialog allowing the user to select a folder for invoice storage.
    The selected path is displayed in the invoice path entry field.
    """
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        invoice_path_entry.delete(0, tk.END)
        invoice_path_entry.insert(0, folder_selected)

def start_rpa() -> None:
    """
    Starts the RPA process by first setting the RPA variables and then closing the window.
    """
    global root
    set_rpa_var()
    root.destroy()

# Main window setup
root = tk.Tk()
root.title('Leitor de Boleto')  # Title of the application
root.geometry('450x600')  # Set the window size
root.configure(bg=bg_color)  # Set the background color

# Set protocol for window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Title label
titulo = tk.Label(root, text='📜 Configurações do Leitor', font=('Arial', 18, 'bold'), fg=primary_color, bg=bg_color)
titulo.pack(pady=10)

# Function to dynamically create labeled entry widgets
def create_labeled_entry(label_text, show=""):
    """
    Creates a labeled entry field with the specified label text and an optional "show" argument
    (to mask text, like for passwords).
    """
    label = tk.Label(root, text=label_text, font=('Arial', 12, 'bold'), fg=text_color, bg=bg_color)
    label.pack()
    entry = tk.Entry(root, font=('Arial', 12), width=35, bd=2, relief='groove', show=show)
    entry.pack(pady=5)
    return entry

# Creating input fields for user data
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

# Invoice path entry
invoice_path_label = tk.Label(root, text='📂 Caminho da Pasta dos Boletos:', font=('Arial', 12, 'bold'), fg=text_color, bg=bg_color)
invoice_path_label.pack()
invoice_path_entry = tk.Entry(root, font=('Arial', 12), width=35, bd=2, relief='groove')
invoice_path_entry.pack(pady=5)

# Browse button for folder selection
browse_btn = tk.Button(root, text='📁 Selecionar Pasta', font=('Arial', 12, 'bold'), fg='white', bg=secondary_color, 
                       width=20, height=1, bd=0, relief='flat', cursor='hand2', command=browse_folder)

browse_btn.pack(pady=5)

# Hover effect for the "Browse" button
def on_enter(e):
    e.widget.config(bg='#27AE60')  # Darker green on hover

def on_leave(e):
    e.widget.config(bg=secondary_color)  # Original color when not hovering

browse_btn.bind('<Enter>', on_enter)
browse_btn.bind('<Leave>', on_leave)

# Start button to initiate the RPA process
start_btn = tk.Button(root, text='🚀 Iniciar', font=('Arial', 12, 'bold'), fg='white', bg=primary_color, 
                      width=20, height=1, bd=0, relief='flat', cursor='hand2', command=start_rpa)

start_btn.pack(pady=5)

# Button hover effects for "Start" button
def on_enter_start(e):
    e.widget.config(bg='#D35400')  # Darker orange on hover

def on_leave_start(e):
    e.widget.config(bg=primary_color)  # Original color when not hovering

start_btn.bind('<Enter>', on_enter_start)
start_btn.bind('<Leave>', on_leave_start)

# Footer label with copyright information
rodape = tk.Label(root, text='📡 Engelmig Energia © 2025', font=('Arial', 10, 'bold'), fg=primary_color, bg=bg_color)
rodape.pack(side='bottom', pady=10)
