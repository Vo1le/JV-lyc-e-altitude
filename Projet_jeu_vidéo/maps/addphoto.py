import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
import shutil
import os

presetfilepath= "imageloadfile.txt"
def addtotxt(filepath, txt):
    with open(filepath, "a") as file :
        file.write(txt + "\n")

img =None
class IntervalApp:
    def __init__(self, root):
        self.img = None
        self.name = ""
        self.root = root
        self.root.title("Sélecteur de tile map")
    
        self.image_label = tk.Label(root, text="Aucune image sélectionnée")
        self.image_label.pack()

        self.select_button = tk.Button(root, text="Sélectionner une Image", command=self.load_image)
        self.select_button.pack()

        self.intervals = []
        self.add_interval_button = tk.Button(root, text="Ajouter un Intervalle", command=self.add_interval)
        self.add_interval_button.pack()

        self.listbox = tk.Listbox(root)
        self.listbox.pack()

        self.remove_button = tk.Button(root, text="Supprimer les intervals", command=self.remove_intervals)
        self.remove_button.pack()

        self.canvas = tk.Canvas(root, width=300, height=300)
        self.canvas.pack()

        self.select_button = tk.Button(root, text="valider", command=lambda:[self.valid(), root.destroy()])
        self.select_button.pack()


    def newimg (self):
        if self.img != None:
            reponse = tk.messagebox.askokcancel(title="Attention", message="Vous avez déjà une image de configurer. Voulez vous la suprimer pour en crée une nouvelle ?")
            
            if reponse == True:
                self.img =None
                self.name = ""
                self.intervals= None
                self.canvas.delete("all")
                self.image_label.config(text=self.img)
            


    def load_image(self):
        if self.img == None:
            file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
            self.img = file_path
            self.name = os.path.basename(self.img)
            if file_path:
                self.image = Image.open(file_path)
                self.image.thumbnail((300, 300))
                self.tk_image = ImageTk.PhotoImage(self.image)
                self.canvas.create_image(150, 150, image=self.tk_image)
                self.image_label.config(text=file_path)
        else:
            self.newimg()

    def add_interval(self):
        if self.img != None :
            start = self.intervals[-1][1] + 1 if self.intervals else 0
            if start != None:
                fin = simpledialog.askinteger("Fin", "Entrez la fin de l'intervalle:")
                if fin != None:
                    type_window = tk.Toplevel(self.root)
                    type_window.title("Sélectionner un d'interval")

                    tk.Label(type_window, text="Choisissez un type:").pack()

                    type_options = ["Rien", "MUR"]
                    selected_type = tk.StringVar(type_window)
                    selected_type.set(type_options[0])

                    type_menu = tk.OptionMenu(type_window, selected_type, *type_options)
                    type_menu.pack()

                    def confirm_selection():
                        category = selected_type.get()
                        self.intervals.append((start, fin, category))
                        addtotxt(presetfilepath, f"{self.name} = {self.intervals}")
                        self.listbox.insert(tk.END, f"{start} à {fin} : {category}")
                        print(self.intervals)
                        type_window.destroy() 
                    def delete():
                        type_window.destroy()
                    tk.Button(type_window, text="Valider", command=confirm_selection).pack()
                    tk.Button(type_window, text="Annuler", command=delete).pack()
        else :
            tk.messagebox.showwarning(title="Attention", message="choississez une image avant de continuer")

    def remove_intervals(self):
        if self.intervals:
            self.intervals.clear()
            self.listbox.delete(0, tk.END)
            messagebox.showinfo("Suppression", "Tous les intervalles ont été supprimés.")


    def valid(self):
        shutil.copy(self.img, "tilemaps")

def run_tkinter():
    root = tk.Tk()
    app = IntervalApp(root)
    root.mainloop()


