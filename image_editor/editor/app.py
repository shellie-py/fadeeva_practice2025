import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .image_processor import ImageProcessor
from .widgets.image_view import ImageView


class ImageEditorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Редактор изображений")
        self.root.geometry("1000x800")

        self.image_processor = ImageProcessor()
        self.create_widgets()
        self.setup_menu()

    def create_widgets(self):
        """Главный контейнер. Создает все элементы интерфейса:
               - Область просмотра изображения
               - Панель управления с кнопками
               - Элементы для операций с изображением
               - Меню"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        #Область изображения
        self.image_view = ImageView(main_frame)
        self.image_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        #Панель управления
        control_frame = ttk.Frame(main_frame, width=300)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        #Кнопки операций
        btn_frame = ttk.LabelFrame(control_frame, text="Операции", padding=10)
        btn_frame.pack(fill=tk.X, pady=5)

        ttk.Button(btn_frame, text="Открыть", command=self.open_image).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="С камеры", command=self.capture_from_camera).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Сохранить", command=self.save_image).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Сбросить", command=self.reset_image).pack(fill=tk.X, pady=2)

        #Цветовые каналы
        channel_frame = ttk.LabelFrame(control_frame, text="Цветовые каналы", padding=10)
        channel_frame.pack(fill=tk.X, pady=5)

        self.channel_var = tk.StringVar(value="Оригинал")
        channels = ["Оригинал", "Красный", "Зеленый", "Синий"]
        for channel in channels:
            ttk.Radiobutton(
                channel_frame,
                text=channel,
                variable=self.channel_var,
                value=channel,
                command=self.update_channel
            ).pack(anchor=tk.W, pady=2)

        #Операции с изображением
        ops_frame = ttk.LabelFrame(control_frame, text="Редактирование", padding=10)
        ops_frame.pack(fill=tk.X, pady=5)

        #Обрезка
        ttk.Label(ops_frame, text="Обрезка (x1,y1,x2,y2):").pack(anchor=tk.W)
        self.crop_entries = []
        crop_frame = ttk.Frame(ops_frame)
        crop_frame.pack(fill=tk.X)
        for _ in range(4):
            entry = ttk.Entry(crop_frame, width=5)
            entry.pack(side=tk.LEFT, padx=2)
            self.crop_entries.append(entry)
        ttk.Button(ops_frame, text="Применить обрезку", command=self.apply_crop).pack(fill=tk.X, pady=5)

        #Поворот
        ttk.Label(ops_frame, text="Поворот (градусы):").pack(anchor=tk.W)
        self.rotate_slider = ttk.Scale(ops_frame, from_=-180, to=180, command=lambda _: self.apply_rotation())
        self.rotate_slider.pack(fill=tk.X)

        #Круг
        ttk.Label(ops_frame, text="Круг (x,y,радиус):").pack(anchor=tk.W)
        self.circle_entries = []
        circle_frame = ttk.Frame(ops_frame)
        circle_frame.pack(fill=tk.X)
        for _ in range(3):
            entry = ttk.Entry(circle_frame, width=5)
            entry.pack(side=tk.LEFT, padx=2)
            self.circle_entries.append(entry)
        ttk.Button(ops_frame, text="Нарисовать круг", command=self.draw_circle).pack(fill=tk.X, pady=5)

    def setup_menu(self):
        """Создает главное меню приложения с пунктами:
               - Открыть/Сохранить файл
               - Выход из приложения"""
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Открыть", command=self.open_image)
        file_menu.add_command(label="Сохранить", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)

        menubar.add_cascade(label="Файл", menu=file_menu)
        self.root.config(menu=menubar)

    def open_image(self):
        """- Открывает диалоговое окно выбора файла
           - Загружает изображение через ImageProcessor
           - Отображает изображение в интерфейсе"""
        file_types = [
            ("Изображения", "*.jpg *.jpeg *.png *.bmp"),
            ("Все файлы", "*.*")
        ]

        try:
            file_path = filedialog.askopenfilename(filetypes=file_types)
            if not file_path:
                return

            if not os.path.exists(file_path):
                messagebox.showerror("Ошибка", "Файл не найден!")
                return

            if os.path.getsize(file_path) == 0:
                messagebox.showerror("Ошибка", "Файл поврежден или пустой!")
                return

            image = self.image_processor.load_image(file_path)
            if image is None:
                messagebox.showerror("Ошибка",
                                     "Не удалось открыть изображение!\n"
                                     "Поддерживаемые форматы: JPG, JPEG, PNG, BMP")
            else:
                self.image_view.display_image(image)
        except Exception as e:
            messagebox.showerror("Критическая ошибка",
                                 f"Произошла непредвиденная ошибка:\n{str(e)}")

    def capture_from_camera(self):
        """- Захватывает изображение с веб-камеры
           - Отображает полученный снимок"""
        image = self.image_processor.capture_from_camera()
        if image is not None:
            self.image_view.display_image(image)

    def save_image(self):
        """- Открывает диалоговое окно сохранения
           - Сохраняет текущее изображение в файл"""
        if self.image_processor.image is None:
            messagebox.showwarning("Ошибка", "Нет изображения для сохранения")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")]
        )
        if file_path:
            self.image_processor.save_image(file_path)

    def reset_image(self):
        """- Восстанавливает исходное изображение
           - Сбрасывает все примененные изменения"""
        image = self.image_processor.reset_image()
        if image is not None:
            self.image_view.display_image(image)
            self.channel_var.set("Оригинал")

    def update_channel(self):
        """- Обновляет отображаемый цветовой канал
           - Поддерживает режимы: оригинал, красный, зеленый, синий"""
        channel = self.channel_var.get()
        image = self.image_processor.show_channel(channel)
        if image is not None:
            self.image_view.display_image(image)

    def apply_crop(self):
        """- Обрезает изображение по заданным координатам
           - Проверяет корректность введенных значений"""
        try:
            coords = [int(entry.get()) for entry in self.crop_entries]
            image = self.image_processor.apply_crop(*coords)
            if image is not None:
                self.image_view.display_image(image)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные координаты")

    def apply_rotation(self):
        """- Поворачивает изображение на заданный угол
           - Использует значение из слайдера"""
        angle = self.rotate_slider.get()
        image = self.image_processor.apply_rotation(angle)
        if image is not None:
            self.image_view.display_image(image)

    def draw_circle(self):
        """- Рисует круг на изображении
           - Использует введенные координаты и радиус"""
        try:
            params = [int(entry.get()) for entry in self.circle_entries]
            image = self.image_processor.draw_circle(*params)
            if image is not None:
                self.image_view.display_image(image)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные параметры круга")

    def run(self):
        """Запускает главный цикл приложения"""
        self.root.mainloop()