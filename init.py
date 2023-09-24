
#FOR DEBUGGING PURPOSES
from tkinter import messagebox

try:
    import main
except Exception as e:
    messagebox.showerror(title='Ajajjj, error!', message=e)
    stop = input("STOP")