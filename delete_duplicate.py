import pandas as pd

# Шаг 1: Чтение исходного файла
input_file = "csv_filename.csv"  # Укажите путь к вашему файлу
output_file = "unique_sku.csv"  # Укажите имя выходного файла

# Загрузка данных из CSV
df = pd.read_csv(input_file)

# Шаг 2: Удаление дубликатов по колонке 'sku'
df_unique = df.drop_duplicates(subset="sku", keep="first")  # Можно использовать 'last' вместо 'first'

# Шаг 3: Сохранение в новый CSV файл
df_unique.to_csv(output_file, index=False)

print(f"Уникальные строки сохранены в файл: {output_file}")
