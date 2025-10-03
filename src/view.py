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

        go_back_button = tk.Button(
            self.get_points_frame,
            text="< Voltar",
            command=lambda: self.switch_screen("select_image")
        )
        go_back_button.pack()

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
        IMAGE_WIDTH = 500
        IMAGE_HEIGHT = 260
        NUM_COLUMNS = 3

        self.show_generated_images_frame = tk.Frame(self.root)
        self.show_generated_images_frame.pack(fill="both", expand=True)

        self.show_generated_images_frame.grid_rowconfigure(1, weight=1)
        self.show_generated_images_frame.grid_columnconfigure(0, weight=1)
        
        control_frame = tk.Frame(self.show_generated_images_frame)
        control_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

        obj_label = tk.Label(control_frame, text="Imagens Geradas")
        obj_label.pack(side="left")

        go_back_button = tk.Button(
            control_frame,
            text="< Voltar",
            command=lambda: self.switch_screen("get_points")
        )
        go_back_button.pack(side="right")

        images_container = tk.Frame(self.show_generated_images_frame)
        images_container.grid(row=1, column=0, sticky="nsew")

        self.generated_tk_images = []

        for index, path in enumerate(self.generated_images):
            image = Image.open(path).convert("RGB")
            image = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT), Image.Resampling.LANCZOS)
            
            tk_image = ImageTk.PhotoImage(image)
            self.generated_tk_images.append(tk_image)
            
            row = index // NUM_COLUMNS
            column = index % NUM_COLUMNS
            
            label = tk.Label(images_container, image=tk_image)
            label.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")

        for i in range(NUM_COLUMNS):
            images_container.grid_columnconfigure(i, weight=1)

        self.current_screen = self.show_generated_images_frame

        


    def run(self):
        self.select_image_screen()

        self.root.mainloop()