import requests
import re
import chardet

# Функция для загрузки данных из URL без кэширования
def fetch_url(url):
    """Загружает данные из URL без кэширования."""
    response = requests.get(url, headers={"Cache-Control": "no-cache"})
    if response.status_code != 200:
        raise Exception(f"Не удалось загрузить плейлист с URL: {url}. Статус: {response.status_code}")
    
    # Определяем кодировку ответа
    detected_encoding = chardet.detect(response.content)["encoding"]
    print(f"Обнаруженная кодировка файла: {detected_encoding}")  # Логирование кодировки
    
    # Обработка MacRoman
    if detected_encoding == "MacRoman":
        return response.content.decode("MacRoman").splitlines()
    else:
        return response.content.decode(detected_encoding).splitlines()

# Функция для парсинга M3U плейлиста
def parse_m3u(url):
    """Парсит M3U файл и возвращает словарь групп."""
    lines = fetch_url(url)
    groups = {}
    current_group = None
    group_content = []

    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF"):
            # Извлекаем название группы из тега EXTGRP
            match = re.search(r'group-title="([^"]+)"', line)
            if match:
                group_name = match.group(1).strip()
                print(f"Найдена группа: {group_name}")  # Логирование найденной группы
                if group_name != current_group:
                    if current_group and group_content:
                        groups[current_group] = group_content
                    current_group = group_name
                    group_content = []
            group_content.append(line)
        elif line.startswith("#EXTVLCOPT") or line.startswith("http"):
            # Добавляем строки с EXTVLCOPT и ссылки
            group_content.append(line)

    # Добавляем последнюю группу
    if current_group and group_content:
        groups[current_group] = group_content

    return groups


# Функция для извлечения строк метаданных
def extract_metadata(url):
    """Извлекает строки метаданных из целевого плейлиста."""
    lines = fetch_url(url)
    metadata_lines = []

    for line in lines:
        if line.startswith("#EXTM3U") or line.startswith("#---"):
            metadata_lines.append(line)  # Сохраняем строки с метаданными

    return metadata_lines


# Функция для обновления плейлиста
def update_playlist(source_urls, target_url, output_file, special_group=None, special_source=None):
    """Обновляет целевой плейлист на основе одного или нескольки
