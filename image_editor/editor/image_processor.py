import cv2
import numpy as np


class ImageProcessor:
    def __init__(self):
        self.image = None
        self.original_image = None
        self.current_channel = "Оригинал"

    def load_image(self, file_path):
        """Загрузка изображения из файла"""
        try:
            self.original_image = cv2.imread(file_path)
            if self.original_image is None:
                return None

            self.image = self.original_image.copy()
            return self.image

        except Exception as e:
            print(f"Ошибка загрузки изображения: {str(e)}")
            return None

    def capture_from_camera(self):
        """Захват изображения с камеры"""
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if ret:
            self.original_image = frame
            self.image = self.original_image.copy()
        return self.image if ret else None

    def reset_image(self):
        """Сброс к исходному изображению"""
        if self.original_image is not None:
            self.image = self.original_image.copy()
            self.current_channel = "Оригинал"
        return self.image

    def save_image(self, file_path):
        """Сохранение изображения в файл"""
        if self.image is not None:
            cv2.imwrite(file_path, self.image)
            return True
        return False

    def show_channel(self, channel):
        """Отображение цветового канала"""
        if self.original_image is None:
            return None

        self.current_channel = channel

        if channel == "Оригинал":
            self.image = self.original_image.copy()
        else:
            channels = cv2.split(self.original_image)
            blank = np.zeros_like(channels[0])

            if channel == "Красный":
                self.image = cv2.merge([blank, blank, channels[2]])
            elif channel == "Зеленый":
                self.image = cv2.merge([blank, channels[1], blank])
            elif channel == "Синий":
                self.image = cv2.merge([channels[0], blank, blank])

        return self.image

    def apply_crop(self, x1, y1, x2, y2):
        """Обрезка изображения по координатам"""
        if self.original_image is None:
            return None

        height, width = self.original_image.shape[:2]

        # Проверка координат
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(width, x2), min(height, y2)

        if x1 >= x2 or y1 >= y2:
            return None

        self.image = self.original_image[y1:y2, x1:x2]
        return self.image

    def apply_rotation(self, angle):
        """Поворот изображения на заданный угол"""
        if self.original_image is None:
            return None

        (h, w) = self.original_image.shape[:2]
        center = (w // 2, h // 2)

        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        self.image = cv2.warpAffine(self.original_image, M, (w, h))
        return self.image

    def draw_circle(self, x, y, radius):
        """Рисование круга на изображении"""
        if self.original_image is None:
            return None

        self.image = self.original_image.copy()
        cv2.circle(self.image, (x, y), radius, (0, 0, 255), 2)
        return self.image