import csv
import random
import os
from PIL import Image
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm


def process_image(sample_info):
    try:
        sample_id, row, stage, image_folder, crop_output_folder, output_path_prefix = (
            sample_info
        )
        image_name = row[0]  # Имя файла

        try:
            image_width = int(row[1])
            image_height = int(row[2])
            x_center = float(row[3])
            y_center = float(row[4])
            box_width = float(row[5])
            box_height = float(row[6])
        except ValueError as ve:
            print(f"Ошибка преобразования данных в строке: {row} -> {ve}")
            return None

        text = row[8].strip()  # Последний столбец - текст

        # Определение координат для обрезки
        x_min = int((x_center - box_width / 2) * image_width)
        y_min = int((y_center - box_height / 2) * image_height)
        x_max = int((x_center + box_width / 2) * image_width)
        y_max = int((y_center + box_height / 2) * image_height)

        # Обрезка изображения
        image_path = os.path.join(image_folder, image_name)
        cropped_image_name = f"{os.path.splitext(image_name)[0]}_{sample_id}.jpg"
        cropped_image_path = os.path.join(crop_output_folder, cropped_image_name)

        if not os.path.exists(image_path):
            print(f"Файл отсутствует: {image_path}")
            return None

        try:
            with Image.open(image_path) as img:
                cropped_img = img.crop((x_min, y_min, x_max, y_max)).convert("RGB")
                cropped_img.save(cropped_image_path, format="JPEG")
        except Exception as e:
            print(f"Ошибка при обработке {image_path}: {e}")
            return None

        return [
            f"{sample_id:03}",
            f"{output_path_prefix}{cropped_image_name}",
            stage,
            text,
        ]
    except Exception as e:
        print(f"Ошибка при обработке строки: {row} -> {e}")
        return None


def main():
    # Входные и выходные файлы
    input_file = r"C:\Users\USER\Desktop\data900\annotations_with_image_size.csv"
    output_file = r"C:\Users\USER\Desktop\data900\marking.csv"
    image_folder = (
        r"C:\Users\USER\Desktop\data900\combined_images"  # Папка с изображениями
    )
    output_path_prefix = "reports/images/"
    crop_output_folder = (
        r"C:\Users\USER\Desktop\data900\cropped_images"  # Папка для сохранения обрезков
    )

    # Создание папки для обрезков, если её нет
    os.makedirs(crop_output_folder, exist_ok=True)

    # Чтение входного файла и фильтрация пустых строк в decoding
    with open(input_file, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Пропускаем заголовок
        data = [
            row for row in reader if row[8].strip()
        ]  # Убираем строки с пустым decoding

    # Перемешивание данных
    random.shuffle(data)

    # Определение границ для разделения на train/valid/test
    num_samples = len(data)
    train_end = int(num_samples * 0.7)
    valid_end = train_end + int(num_samples * 0.2)

    # Подготовка данных для обработки в нескольких потоках
    sample_data = []
    for i, row in enumerate(data):
        if i < train_end:
            stage = "train"
        elif i < valid_end:
            stage = "valid"
        else:
            stage = "test"
        sample_data.append(
            (i + 1, row, stage, image_folder, crop_output_folder, output_path_prefix)
        )

    # Используем ProcessPoolExecutor для параллельной обработки с прогресс-баром
    processed_data = []
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_image, item): item for item in sample_data}
        for future in tqdm(
            as_completed(futures), total=len(futures), desc="Processing images"
        ):
            result = future.result()
            if result is not None:
                processed_data.append(result)

    # Запись в новый CSV файл
    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["sample_id", "path", "stage", "text"])  # Заголовок
        writer.writerows(processed_data)

    print(
        f"Конвертация завершена. Обрезки сохранены в {crop_output_folder}, разметка - в {output_file}"
    )


if __name__ == "__main__":
    main()
