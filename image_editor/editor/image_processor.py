import cv2
import numpy as np


class ImageProcessor:
    def __init__(self):
        self.image = None
        self.original_image = None
        self.current_channel = "Оригинал"

    def load_image(self, file_path):
        """Загрузка изображения с обработкой ошибок"""
        try:
            if not file_path:
                raise ValueError("Путь к файлу не указан")

            self.original_image = cv2.imread(file_path)
            if self.original_image is None:
                raise ValueError(f"Не удалось загрузить изображение по пути: {file_path}")

            self.image = self.original_image.copy()
            return self.image
        except Exception as e:
            raise RuntimeError(f"Ошибка загрузки изображения: {str(e)}")

    def save_image(self, file_path):
        """Сохранение изображения"""
        try:
            if self.image is None:
                raise ValueError("Нет изображения для сохранения")

            if not file_path:
                raise ValueError("Путь для сохранения не указан")

            if not cv2.imwrite(file_path, self.image):
                raise RuntimeError("Ошибка при сохранении файла")

            return True
        except Exception as e:
            raise RuntimeError(f"Ошибка сохранения изображения: {str(e)}")

    def capture_from_camera(self):
        """Захват с камеры"""
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                raise RuntimeError("Не удалось подключиться к камере. Проверьте подключение.")

            ret, frame = cap.read()
            cap.release()

            if not ret:
                raise RuntimeError("Не удалось получить кадр с камеры")

            self.original_image = frame
            self.image = self.original_image.copy()
            return self.image
        except Exception as e:
            raise RuntimeError(f"Ошибка захвата с камеры: {str(e)}")

    def reset_image(self):
        """Сброс к исходному изображению"""
        try:
            if self.original_image is None:
                raise ValueError("Нет загруженного изображения")

            self.image = self.original_image.copy()
            self.current_channel = "Оригинал"
            return self.image
        except Exception as e:
            raise RuntimeError(f"Ошибка сброса изображения: {str(e)}")

    def show_channel(self, channel):
        """Отображение цветового канала"""
        try:
            if self.original_image is None:
                raise ValueError("Изображение не загружено")

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
                else:
                    raise ValueError(f"Неизвестный канал: {channel}")

            return self.image
        except ValueError as ve:
            raise ValueError(f"Ошибка выбора канала: {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Ошибка обработки цветового канала: {str(e)}")

    def apply_crop(self, x1, y1, x2, y2):
        """Обрезка изображения с валидацией координат"""
        try:
            if self.original_image is None:
                raise ValueError("Изображение не загружено")

            # Валидация координат
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            h, w = self.original_image.shape[:2]

            if any(coord < 0 for coord in [x1, y1, x2, y2]):
                raise ValueError("Координаты не могут быть отрицательными")
            if x1 >= x2 or y1 >= y2:
                raise ValueError("Некорректные координаты: x2 должно быть > x1, y2 > y1")
            if x2 > w or y2 > h:
                raise ValueError(f"Координаты выходят за границы изображения ({w}x{h})")

            self.image = self.original_image[y1:y2, x1:x2]
            return self.image
        except ValueError as ve:
            raise ValueError(f"Ошибка в параметрах обрезки: {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Ошибка при обрезке изображения: {str(e)}")

    def apply_rotation(self, angle):
        """Поворот изображения"""
        try:
            if self.original_image is None:
                raise ValueError("Изображение не загружено")

            angle = float(angle)
            (h, w) = self.original_image.shape[:2]
            center = (w // 2, h // 2)

            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            self.image = cv2.warpAffine(self.original_image, M, (w, h))
            return self.image
        except ValueError as ve:
            raise ValueError(f"Некорректный угол поворота: {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Ошибка при повороте изображения: {str(e)}")

    def draw_circle(self, x, y, radius):
        """Рисование круга"""
        try:
            if self.original_image is None:
                raise ValueError("Изображение не загружено")

            # Валидация параметров
            x, y, radius = map(int, [x, y, radius])
            h, w = self.original_image.shape[:2]

            if radius <= 0:
                raise ValueError("Радиус должен быть положительным числом")
            if x < 0 or y < 0:
                raise ValueError("Координаты центра не могут быть отрицательными")
            if x - radius < 0 or x + radius > w or y - radius < 0 or y + radius > h:
                raise ValueError("Круг выходит за границы изображения")

            self.image = self.original_image.copy()
            cv2.circle(self.image, (x, y), radius, (0, 0, 255), 2)
            return self.image
        except ValueError as ve:
            raise ValueError(f"Ошибка в параметрах круга: {str(ve)}")
        except Exception as e:
            raise RuntimeError(f"Ошибка при рисовании круга: {str(e)}")
