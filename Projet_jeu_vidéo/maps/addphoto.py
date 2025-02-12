import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
import shutil
import os
GRID_SIZE = 32
presetfilepath= "imageloadfile.txt"
def addtotxt(filepath, txt):
    with open(filepath, "a") as file :
        file.write(txt + "\n")

img =None
class IntervalApp:
    def __init__(self, root):
        self.img = None
        self.name = ""
        self.image = None
        self.img_tk = None
        self.interval = []

        self.root = root
        self.root.title("Sélecteur de tile map")
    
        self.image_label = tk.Label(root, text="Aucune image sélectionnée")
        self.image_label.pack()

        self.select_button = tk.Button(root, text="enregister", command=lambda:[self.valid(), root.destroy()])
        self.select_button.pack()

        self.select_button = tk.Button(root, text="Sélectionner une Image", command=self.load_image)
        self.select_button.pack()
        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)
        self.canvas = tk.Canvas(self.frame, bg="white")
        self.canvas.pack()


    def newimg (self):
        if self.img != None:
            reponse = tk.messagebox.askokcancel(title="Attention", message="Vous avez déjà une image de configurer. Voulez vous la suprimer pour en crée une nouvelle ?")
            
            if reponse == True:
                self.img =None
                self.name = ""
                self.interval = []
                self.canvas.delete("all")
                self.canvas.config(width=100, height=100)
                self.image_label.config(text=self.img)         

    def load_image(self):
        if self.img == None:
            file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
            self.img = file_path
            self.name = os.path.basename(self.img)
            if file_path:
                self.image = Image.open(file_path)
                self.update_canvas()
        else:
            self.newimg()

    def update_canvas(self):
        if self.image is None:
            return

        img_width, img_height = self.image.size
        
        self.canvas.config(width=img_width, height=img_height)
        self.interval.append(img_width // GRID_SIZE)
        self.interval.append(img_height // GRID_SIZE)
        self.img_tk = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img_tk)

        self.draw_grid(img_width, img_height)

    def draw_grid(self, width, height):
        self.canvas.delete("grid")  

        cols = width // GRID_SIZE
        rows = height // GRID_SIZE

        for i in range(cols + 1):
            x = i * GRID_SIZE
            self.canvas.create_line(x, 0, x, height, fill="red", tags="grid")

        for j in range(rows + 1):
            y = j * GRID_SIZE
            self.canvas.create_line(0, y, width, y, fill="red", tags="grid")

        self.canvas.create_text(10, 10, anchor="nw", text=f"Cols: {cols}, Rows: {rows}", fill="black", font=("Arial", 12, "bold"), tags="grid")


    def valid(self):
        shutil.copy(self.img, "tilemaps")
        addtotxt(presetfilepath, f"{self.name} = {self.interval}")

def run_tkinter():
    root = tk.Tk()
    app = IntervalApp(root)
    root.mainloop()


TXT_FILE = "imageloadfile.txt"
IMAGE_FOLDER = "tilemaps"  

class ImageManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("modifier images loads")

        self.open_button = tk.Button(root, text="liste image", command=self.open_list_window)
        self.open_button.pack(pady=10)

    def open_list_window(self):
        self.list_window = tk.Toplevel(self.root)
        self.list_window.title("Image")
        self.load_entries()

    def load_entries(self):
        try:
            with open(TXT_FILE, "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            messagebox.showerror("Error", f"Fichier '{TXT_FILE}' introuvable")
            return

        if not lines:
            messagebox.showinfo("Info", "Aucune image chargée")
            return

        for line in lines:
            if "=" in line:
                filename = line.split("=")[0].strip()

                frame = tk.Frame(self.list_window)
                frame.pack(fill=tk.X, padx=5, pady=2)

                label = tk.Label(frame, text=filename, anchor="w")
                label.pack(side=tk.LEFT, expand=True)

                delete_button = tk.Button(frame, text="suprimer", command=lambda f=filename: self.delete_entry(f))
                delete_button.pack(side=tk.RIGHT)

    def delete_entry(self, filename):
        try:
            with open(TXT_FILE, "r") as file:
                lines = file.readlines()

            with open(TXT_FILE, "w") as file:
                for line in lines:
                    if not line.startswith(filename):
                        file.write(line)

            image_path = os.path.join(IMAGE_FOLDER, filename)
            if os.path.exists(image_path):
                os.remove(image_path)
                messagebox.showinfo("yeppi", f"Supression effectuer pour '{filename}'")
            else:
                messagebox.showwarning("mince", f"Image '{filename}' introuvable dans '{IMAGE_FOLDER}'.")

            # Refresh list window
            for widget in self.list_window.winfo_children():
                widget.destroy()
            self.load_entries()

        except Exception as e:
            messagebox.showerror("Erreur", f"erreur: {e}")

def runtk2():
    root = tk.Tk()
    app = ImageManagerApp(root)
    root.mainloop()