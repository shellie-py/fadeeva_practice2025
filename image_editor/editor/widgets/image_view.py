import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk


class ImageView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas = tk.Canvas(self, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.image_tk = None

    def display_image(self, cv_image):
        """- Отображает OpenCV изображение на холсте
           - Автоматически масштабирует под размер окна
           - Сохраняет пропорции изображения
           - Центрирует изображение на холсте"""
        if cv_image is not None:
            # Конвертируем из BGR в RGB
            image = Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))

            # Масштабируем изображение под размер канваса
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            if canvas_width > 1 and canvas_height > 1:
                img_ratio = image.width / image.height
                canvas_ratio = canvas_width / canvas_height

                if img_ratio > canvas_ratio:
                    new_width = canvas_width
                    new_height = int(canvas_width / img_ratio)
                else:
                    new_height = canvas_height
                    new_width = int(canvas_height * img_ratio)

                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            self.image_tk = ImageTk.PhotoImage(image)
            self.canvas.delete("all")
            self.canvas.create_image(
                canvas_width // 2,
                canvas_height // 2,
                anchor=tk.CENTER,
                image=self.image_tk
            )