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
            "get_points": self.get_points_screen,
            "show_generated_images": self.show_generated_images_screen
        }

        self.current_screen = None

        self.image = None
        self.image_path = ""
    
    def set_controller(self, controller):
        self.controller = controller
    
    def switch_screen(self, new_screen: str):
        self.current_screen.destroy()
        screen = self.screens[new_screen]
        if (screen):
            self.current_screen = screen
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
                "get_points"
                )
            )
        select_file_next_button.pack()
        self.current_screen = self.select_file_frame

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
            self.switch_screen("select_image")
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
        self.next_group_button = tk.Button(
            self.get_points_frame,
            text="Próximo Grupo",
            command=lambda: self.get_point_group(value=1)
        )
        self.next_group_button.pack()

        self.current_screen = self.get_points_frame
    
    def get_point(self, event):
        x, y = event.x, event.y
        pixel = self.image.getpixel((x, y))
        self.controller.save_pixel(pixel, self.current_group)
        radius = 3
        color = "red" if self.current_group == 0 else "blue"
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, outline=color)

    def get_point_group(self, value: int):
        if (value == 1):
            if self.current_group + 1 < len(self.group):
                self.current_group += 1
                
                if (self.current_group == len(self.group) - 1):
                    self.next_group_button.config(text="Gerar Imagens")
                else:
                    self.next_group_button.config(text="Próximo Grupo")

            else:
                self.controller.separate_object(self.image_path)
                return
        else:
            if self.current_group - 1 >= 0:
                self.current_group -= 1
        self.get_points_label.config(text=f"Pegando pontos de: {self.group[self.current_group]}")
    
    def show_image(self, image_path):
        self.image = Image.open(image_path).convert("RGB")
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.config(width=self.tk_image.width(), height=self.tk_image.height())

    def set_generated_images(self, images: list[str]):
        self.generated_images = images
        self.switch_screen("show_generated_images")

    def show_generated_images_screen(self):
        self.show_generated_images_frame = tk.Frame(self.root)
        self.show_generated_images_frame.pack()

        obj_label = tk.Label(self.show_generated_images_frame, text="Imagens Geradas")
        obj_label.pack()

        self.generated_tk_images = []

        for path in self.generated_images:
            image = Image.open(path).convert("RGB")
            tk_image = ImageTk.PhotoImage(image)
            self.generated_tk_images.append(tk_image)
            label = tk.Label(self.show_generated_images_frame, image=tk_image)
            label.pack(pady=5)

        self.current_screen = self.show_generated_images_frame


    def run(self):
        self.select_image_screen()

        self.root.mainloop()