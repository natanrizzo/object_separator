import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class View:
    def __init__(self):
        self.controller = None
        
        self.root = tk.Tk()
        self.root.title("Separador de Objeto")
        self.root.geometry("720x460")
        
        self.screens = {
            "select_image": self.select_image_screen,
            "get_points": self.get_points_screen
        }

        self.image = None
        self.image_path = ""
    
    def set_controller(self, controller):
        self.controller = controller
    
    def switch_screen(self, current_screen: tk.Frame, new_screen: str):
        current_screen.destroy()
        screen = self.screens[new_screen]
        if (screen):
            screen()

    def select_image_screen(self):
        self.select_file_frame = tk.Frame(self.root)
        self.select_file_frame.pack()

        select_file_button = tk.Button(
            self.select_file_frame, text="Selecione uma imagem.",
            command=self.select_image
        )
        select_file_button.pack()

        self.file_label = tk.Label(
            self.select_file_frame,
            text="Nenhum arquivo selecionado."
        )
        self.file_label.pack()

        select_file_next_button = tk.Button(
            self.select_file_frame, text="Próximo",
            command= lambda: self.switch_screen(
                self.select_file_frame, "get_points"
                )
            )
        select_file_next_button.pack()

    def select_image(self):
        file_path = filedialog.askopenfile(filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff *.tif *.webp")
        ]).name
        
        if file_path:
            self.file_label.config(text=file_path)
            self.image_path = file_path

        return file_path
    
    def get_points_screen(self):
        self.group = ["Fundo", "Objeto"]
        self.current_group = 0

        self.get_points_frame = tk.Frame(self.root)
        self.get_points_frame.pack()

        if (self.image_path == None or self.image_path == ""):
            self.switch_screen(self.get_points_frame, "select_image")
            return

        self.get_points_label = tk.Label(
            self.get_points_frame,
            text=f"Pegando pontos de: {self.group[self.current_group]}"
        )
        self.get_points_label.pack()

        self.canvas = tk.Canvas(self.get_points_frame)
        self.canvas.pack()
        
        self.image = Image.open(self.image_path).convert("RGB")
        self.tk_image = ImageTk.PhotoImage(self.image)

        self.canvas.config(width=self.tk_image.width(), height=self.tk_image.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.canvas.bind("<Button-1>", self.get_point)

        previous_group_button = tk.Button(
            self.get_points_frame,
            text="Grupo Anterior",
            command=lambda: self.get_point_group(value=-1)
        )
        previous_group_button.pack()
        next_group_button = tk.Button(
            self.get_points_frame,
            text="Próximo Grupo",
            command=lambda: self.get_point_group(value=1)
        )
        next_group_button.pack()
    
    def get_point(self, event):
        x, y = event.x, event.y
        pixel = self.image.getpixel((x, y))
        self.controller.save_pixel(pixel, self.current_group)
        r = 3 # Dot radius
        color = "red" if self.current_group == 0 else "blue"
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline=color)

    def get_point_group(self, value: int):
        if (value == 1):
            if self.current_group + 1 < len(self.group):
                self.current_group += 1
            else:
                self.controller.separate_object(self.image_path)
        else:
            if self.current_group - 1 >= 0:
                self.current_group -= 1
        self.get_points_label.config(text=f"Pegando pontos de: {self.group[self.current_group]}")

    def run(self):
        self.select_image_screen()

        self.root.mainloop()