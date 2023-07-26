import os

# Папки с исходными и обработанными файлами
source_dir = "f:\\dataset_noise\\prepared"
processed_dir = "e:\\hifigan\\data\\clean"

# Получаем имена всех исходных файлов без изменений
source_files = [f for f in os.listdir(source_dir) if f.endswith('.wav')]

# Получаем имена всех обработанных файлов
processed_files = os.listdir(processed_dir)

# Проверяем, есть ли обработанные файлы для каждого исходного файла
for source_file in source_files:
    # Создаем фильтр для поиска обработанных файлов, соответствующих исходному файлу
    processed_file_filter = source_file[:-4] + "_segment_"  # убираем расширение .wav и добавляем префикс сегмента
    # Ищем обработанные файлы, соответствующие исходному файлу
    matching_files = [f for f in processed_files if f.startswith(processed_file_filter)]
    
    if len(matching_files) == 0:
        print(f"No processed files found for source file {source_file}")
