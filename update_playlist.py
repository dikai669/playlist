import requests
import re

# Функция для парсинга M3U плейлиста
def parse_m3u(url):
    """Парсит M3U файл и возвращает словарь групп."""
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Не удалось загрузить плейлист с URL: {url}")
    
    lines = response.text.splitlines()
    groups = {}
    current_group = "Без группы"  # Группа по умолчанию для каналов без EXTGRP
    group_content = []

    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF"):
            # Добавляем канал в текущую группу
            group_content.append(line)
        elif line.startswith("#EXTGRP"):
            # Извлекаем название группы из тега EXTGRP
            match = re.search(r'^#EXTGRP:(.+)$', line)
            if match:
                new_group = match.group(1).strip()
                if new_group != current_group:
                    if current_group and group_content:
                        groups[current_group] = group_content
                    current_group = new_group
                    group_content = []
        elif line.startswith("http"):
            # Добавляем ссылку на канал
            group_content.append(line)

    # Добавляем последнюю группу
    if current_group and group_content:
        groups[current_group] = group_content

    return groups


# Функция для извлечения строк метаданных
def extract_metadata(url):
    """Извлекает строки метаданных из целевого плейлиста."""
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Не удалось загрузить плейлист с URL: {url}")
    
    lines = response.text.splitlines()
    metadata_lines = []

    for line in lines:
        if line.startswith("#EXTM3U") or line.startswith("#---"):
            metadata_lines.append(line)  # Сохраняем строки с метаданными

    return metadata_lines


# Функция для обновления плейлиста
def update_playlist(source_urls, target_url, output_file, special_groups=None):
    """Обновляет целевой плейлист на основе одного или нескольких исходников."""
    # Парсим целевой плейлист
    target_groups = parse_m3u(target_url)
    print(f"Группы в целевом плейлисте: {list(target_groups.keys())}")
    
    # Обновляем только указанные группы из специальных источников
    if special_groups:
        for special_group, special_source in special_groups.items():
            special_source_groups = parse_m3u(special_source)
            if special_group in special_source_groups:
                print(f"Обновляется группа: {special_group} из второго исходника")
                target_groups[special_group] = special_source_groups[special_group]
            elif special_group in target_groups:
                print(f"Группа '{special_group}' не найдена во втором исходнике, сохраняем её")

    # Извлекаем строки метаданных
    metadata_lines = extract_metadata(target_url)

    # Формируем обновлённый плейлист
    with open(output_file, "w", encoding="utf-8") as f:
        # Добавляем строки метаданных
        for metadata_line in metadata_lines:
            f.write(f"{metadata_line}\n")
        
        # Добавляем группы и каналы
        for group, channels in target_groups.items():
            f.write(f"#EXTGRP:{group}\n")  # Добавляем тег EXTGRP для группы
            for channel in channels:
                f.write(f"{channel}\n")
    
    print(f"Плейлист успешно обновлён и сохранён в {output_file}!")


# Основная функция
if __name__ == "__main__":
    # URL исходных плейлистов
    source_url_1 = "https://raw.githubusercontent.com/IPTVSHARED/iptv/refs/heads/main/IPTV_SHARED.m3u"
    source_url_2 = "https://raw.githubusercontent.com/Dimonovich/TV/Dimonovich/FREE/TV"
    target_url = "https://raw.githubusercontent.com/dikai669/playlist/refs/heads/main/mpll.m3u"
    output_file = "mpll.m3u"

    # Специальные группы для обновления
    special_groups = {
        "Lime (VPN 🇷🇺)": source_url_2
    }

    # Обновляем плейлист
    try:
        update_playlist(
            source_urls=[source_url_1],
            target_url=target_url,
            output_file=output_file,
            special_groups=special_groups
        )
    except Exception as e:
        print(f"Ошибка: {e}")
