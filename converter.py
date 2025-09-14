import tarfile
import zipfile
import os
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox

def tar_gz_to_zip(tar_gz_path, zip_path):
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            # Extrair com filtro seguro
            with tarfile.open(tar_gz_path, "r:gz") as tar:
                tar.extractall(path=tmpdir, filter="data")

            # Compactar em ZIP
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(tmpdir):
                    for file in files:
                        filepath = os.path.join(root, file)
                        arcname = os.path.relpath(filepath, tmpdir)
                        zipf.write(filepath, arcname)

        messagebox.showinfo("Sucesso", f"Arquivo convertido com sucesso:\n{zip_path}")

    except Exception as e:
        messagebox.showerror("Erro", str(e))


def selecionar_arquivo():
    tar_gz_path = filedialog.askopenfilename(
        title="Selecione um arquivo .tar.gz",
        filetypes=[("Arquivos TAR.GZ", "*.tar.gz"), ("Todos os arquivos", "*.*")]
    )
    if not tar_gz_path:
        return
    
    zip_path = filedialog.asksaveasfilename(
        title="Salvar como",
        defaultextension=".zip",
        filetypes=[("Arquivos ZIP", "*.zip")]
    )
    if not zip_path:
        return

    tar_gz_to_zip(tar_gz_path, zip_path)


# Interface principal
root = tk.Tk()
root.title("Conversor TAR.GZ → ZIP")
root.geometry("400x200")

label = tk.Label(root, text="Conversor de arquivos TAR.GZ para ZIP", font=("Arial", 12))
label.pack(pady=20)

btn = tk.Button(root, text="Selecionar arquivo .tar.gz", command=selecionar_arquivo, font=("Arial", 10))
btn.pack(pady=10)

root.mainloop()
