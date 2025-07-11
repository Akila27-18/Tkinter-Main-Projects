import tkinter as tk
from tkinter import filedialog, messagebox
from crypto_utils import encrypt_file, decrypt_file
from db import init_db, log_action
import os

init_db()

def lock_file():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    password = password_entry.get()
    if not password:
        messagebox.showwarning("Missing Password", "Enter a password.")
        return

    try:
        enc_file = encrypt_file(file_path, password)
        log_action(os.path.basename(enc_file), "LOCKED")
        messagebox.showinfo("Success", f"File encrypted:\n{enc_file}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def unlock_file():
    file_path = filedialog.askopenfilename(filetypes=[("Locked Files", "*.lock")])
    if not file_path:
        return
    password = password_entry.get()
    if not password:
        messagebox.showwarning("Missing Password", "Enter a password.")
        return

    result = decrypt_file(file_path, password)
    if result:
        log_action(os.path.basename(result), "UNLOCKED")
        messagebox.showinfo("Success", f"File decrypted:\n{result}")
    else:
        messagebox.showerror("Failed", "Incorrect password or corrupt file.")

# GUI
root = tk.Tk()
root.title("Secure File Locker")
root.geometry("400x250")
root.resizable(False, False)

tk.Label(root, text="Secure File Locker", font=("Helvetica", 16, "bold")).pack(pady=10)

tk.Label(root, text="Enter Password:").pack()
password_entry = tk.Entry(root, show="*", width=30)
password_entry.pack(pady=5)

tk.Button(root, text="Lock File", command=lock_file, width=25).pack(pady=10)
tk.Button(root, text="Unlock File", command=unlock_file, width=25).pack(pady=5)

tk.Label(root, text="Encrypted files use .lock extension").pack(pady=10)
root.mainloop()
