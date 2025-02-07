import pandas as pd
from collections import Counter

# Путь к файлу
file_path = r"C:\Users\pasha\OneDrive\Рабочий стол\data900\marking.csv"

# Чтение CSV файла
df = pd.read_csv(file_path)

# Объединение всех текстовых данных в одну строку
all_text = "".join(df["text"].astype(str))

# Подсчет количества вхождений каждого символа
char_counts = Counter(all_text)

# Сортировка символов по убыванию частоты
sorted_chars = sorted(char_counts.items(), key=lambda x: x[1], reverse=True)

# Создание словаря {индекс: (символ, количество повторов)}
char_dict = {i: (char, count) for i, (char, count) in enumerate(sorted_chars)}

# Вывод словаря в консоль
print(char_dict)

# Вывод всех символов в строковом формате (без экранирования, в нормальном виде)
char_string = "".join([char for char, _ in sorted_chars])
print(f"Все символы по частоте: '{char_string}'")
