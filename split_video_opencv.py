import cv2
import os
from pathlib import Path
import time
import datetime

def crop_video_opencv(
    input_video_path: str,
    output_video_path: str,
    crop_x: int,
    crop_y: int,
    crop_width: int,
    crop_height: int
) -> bool:
    """
    Обрізає відео, вибираючи прямокутну область з кожного кадру,
    задану координатами та розмірами.

    Аргументи:
        input_video_path (str): Шлях до вхідного відеофайлу.
        output_video_path (str): Шлях для збереження обрізаного відеофайлу.
        crop_x (int): Координата X (горизонтальна) верхнього лівого кута області обрізки.
        crop_y (int): Координата Y (вертикальна) верхнього лівого кута області обрізки.
        crop_width (int): Ширина області обрізки.
        crop_height (int): Висота області обрізки.

    Повертає:
        bool: True, якщо обрізка пройшла успішно, False в іншому випадку.
    """
    if not os.path.exists(input_video_path):
        print(f"Error: Input video '{input_video_path}' not found.")
        return False

    cap = cv2.VideoCapture(input_video_path)

    if not cap.isOpened():
        print(f"Error: Can't open video '{input_video_path}' ")
        return False

    # Отримуємо властивості вхідного відео
    fps = cap.get(cv2.CAP_PROP_FPS)
    input_frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    input_frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"Input video: {input_frame_width}x{input_frame_height} @ {fps} FPS, Всього кадрів: {total_frames}")
    print(f"Обрізка області: X={crop_x}, Y={crop_y}, Ширина={crop_width}, Висота={crop_height}")

    # Перевіряємо, чи область обрізки знаходиться в межах кадру
    if (crop_x < 0 or crop_y < 0 or
        crop_x + crop_width > input_frame_width or
        crop_y + crop_height > input_frame_height):
        print(f"Помилка: Область обрізки ({crop_x},{crop_y}) W{crop_width} H{crop_height} "
              f"виходить за межі вхідного відео {input_frame_width}x{input_frame_height}.")
        cap.release()
        return False
    if crop_width <= 0 or crop_height <= 0:
        print("Помилка: Ширина або висота області обрізки повинні бути більше нуля.")
        cap.release()
        return False


    # Налаштовуємо VideoWriter для запису обрізаного відео
    # Обрізане відео матиме розмір, рівний crop_width x crop_height
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Кодек для MP4.
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (crop_width, crop_height))

    if not out.isOpened():
        print(f"Помилка: Не вдалося створити вихідний відеофайл '{output_video_path}'.")
        print("Переконайтеся, що FourCC кодек ('mp4v') сумісний з вашою системою та форматом файлу (.mp4).")
        cap.release()
        return False

    current_frame_index = 0
    frames_written = 0
    print("Починаємо обрізку кадрів...")

    try:
        while True:
            ret, frame = cap.read() # Зчитуємо поточний кадр
            if not ret:
                break # Кінець відео або помилка зчитування

            # Обрізка кадру: NumPy-масиви дозволяють обрізати їх як звичайні масиви
            # [Y_start:Y_end, X_start:X_end]
            cropped_frame = frame[crop_y : crop_y + crop_height, crop_x : crop_x + crop_width]
            
            out.write(cropped_frame) # Записуємо обрізаний кадр
            frames_written += 1
            current_frame_index += 1

        print(f"Обрізку завершено. Записано {frames_written} кадрів.")
        return True

    except Exception as e:
        print(f"Виникла помилка під час обробки кадрів: {e}")
        return False
    finally:
        cap.release() # Завжди звільняємо VideoCapture
        out.release() # Завжди звільняємо VideoWriter

def trim_video_opencv(
    input_video_path: str,
    output_video_path: str,
    start_time_seconds: float,
    duration_seconds: float
) -> bool:
    """
    Обрізає (вирізає) сегмент відео з вказаного часу початку та тривалості
    за допомогою OpenCV.

    Аргументи:
        input_video_path (str): Шлях до вхідного відеофайлу.
        output_video_path (str): Шлях для збереження обрізаного відеофайлу.
        start_time_seconds (float): Час початку сегмента у секундах.
        duration_seconds (float): Тривалість сегмента у секундах.

    Повертає:
        bool: True, якщо обрізка пройшла успішно, False в іншому випадку.
    """
    if not os.path.exists(input_video_path):
        print(f"Помилка: Вхідне відео '{input_video_path}' не знайдено.")
        return False

    cap = cv2.VideoCapture(input_video_path)

    if not cap.isOpened():
        print(f"Помилка: Не вдалося відкрити відеофайл '{input_video_path}'. Перевірте формат або цілісність файлу.")
        return False

    # Отримуємо властивості відео
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Обчислюємо індекси початкового та кінцевого кадрів
    start_frame_index = int(start_time_seconds * fps)
    end_frame_index = int((start_time_seconds + duration_seconds) * fps)

    # Перевіряємо, чи індекси не виходять за межі загальної кількості кадрів
    if start_frame_index >= total_frames:
        print(f"Помилка: Час початку {start_time_seconds}с (кадр {start_frame_index}) виходить за межі відео ({total_frames} кадрів).")
        cap.release()
        return False
    if end_frame_index > total_frames:
        print(f"Попередження: Час кінця {start_time_seconds + duration_seconds}с (кадр {end_frame_index}) виходить за межі відео ({total_frames} кадрів). Обрізаю до кінця відео.")
        end_frame_index = total_frames

    print(f"Відео: {frame_width}x{frame_height} @ {fps} FPS, Всього кадрів: {total_frames}")
    print(f"Обрізка з кадру {start_frame_index} до кадру {end_frame_index}.")

    # Налаштовуємо VideoWriter для запису обрізаного відео
    # 'mp4v' - це FourCC кодек для MP4. Можливо, 'XVID' для .avi або інший.
    # Для MP4, 'avc1' або 'H264' також можуть бути використані, але 'mp4v' досить поширений.
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # або cv2.VideoWriter_fourcc(*'XVID') for .avi
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    if not out.isOpened():
        print(f"Помилка: Не вдалося створити вихідний відеофайл '{output_video_path}'.")
        print("Переконайтеся, що FourCC кодек ('mp4v') сумісний з вашою системою та форматом файлу (.mp4).")
        cap.release()
        return False

    current_frame_index = 0
    frames_written = 0
    print("Починаємо обрізку...")

    try:
        while True:
            ret, frame = cap.read() # Зчитуємо поточний кадр
            if not ret:
                break # Кінець відео або помилка зчитування

            if current_frame_index >= start_frame_index:
                if current_frame_index < end_frame_index:
                    out.write(frame) # Записуємо кадр, якщо він знаходиться в потрібному діапазоні
                    frames_written += 1
                else:
                    break # Досягли кінця обрізки, зупиняємо
            
            current_frame_index += 1

        print(f"Обрізку завершено. Записано {frames_written} кадрів.")
        return True

    except Exception as e:
        print(f"Виникла помилка під час обробки кадрів: {e}")
        return False
    finally:
        cap.release() # Завжди звільняємо VideoCapture
        out.release() # Завжди звільняємо VideoWriter

# --- Приклад використання ---
#   test_channel_url = "https://www.youtube.com/@VisualMelodies"
if __name__ == "__main__":
    start_time = time.time()
    instagram_video_width = 1080
    instagram_video_height = 1920
    #for 1080
    crop_width = 608
    crop_height = 1080
    crop_x = 656
    crop_y = 0
    #for 720
    #crop_width = 405
    #crop_height = 720
    #crop_x = 338
    crop_y = 0
    #for shorts W1080*H1920
    crop_width = 405
    crop_height = 850
    crop_x = 478
    crop_y = 1069
    #current_script_dir = Path(__file__).parent
    current_script_dir = Path("C:/")
    file_input_path_trim = str(current_script_dir / "video" / "input_video" / "video_2025-06-23_07-42-40.mp4")
    file_output_path_trim = str(current_script_dir / "video" / "output_video" / "video_trimmed.mp4")
    start = 0
    for i in range(22):
        start_time_trim = time.time()
        print(f"Video processing: {i + 1}/10")
        start= start + 2
        success_trim = trim_video_opencv(file_input_path_trim, file_output_path_trim, start, 8)
        if success_trim:
            print(f"Success: Trim duration: {time.time() - start_time_trim:.4f} sec.")
        else:
            print("Error trim")
        #-------------
        start_time_crop = time.time()        
        file_input_path_crop = file_output_path_trim
        file_name= 'video '+datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")+'.mp4'
        file_output_path_crop = str(current_script_dir / "video" / "output_video" / file_name)

        success_crop = crop_video_opencv(file_input_path_crop, file_output_path_crop, crop_x, crop_y, crop_width, crop_height )
        if success_crop:
            print(f"Success: Crop duration: {time.time() - start_time_crop:.4f} sec.")
        else:
            print("Error crop")

        print(f"Total duration: {time.time() - start_time:.4f} sec.") 