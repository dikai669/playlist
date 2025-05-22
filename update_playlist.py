import requests
import re

# Функция для загрузки данных из URL без кэширования
def fetch_url(url):
    """Загружает данные из URL без кэширования."""
    response = requests.get(url.strip(), headers={"Cache-Control": "no-cache"})
    if response.status_code != 200:
        raise Exception(f"Не удалось загрузить плейлист с URL: {url}. Статус: {response.status_code}")
    
    # Принудительно декодируем данные в UTF-8
    try:
        content = response.content.decode("utf-8")
    except UnicodeDecodeError:
        # Если не UTF-8, пробуем MacRoman или другую кодировку
        content = response.content.decode("MacRoman", errors="replace")
    
    return content.splitlines()

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
    """Обновляет целевой плейлист на основе одного или нескольких исходников."""
    print("Загрузка целевого плейлиста...")
    target_groups = parse_m3u(target_url)
    print(f"Группы в целевом плейлисте: {list(target_groups.keys())[:20]} (выведено до 20)")

    # Обновляем группы из первого исходника
    source_groups = parse_m3u(source_urls[0])
    print(f"Группы в первом исходнике: {list(source_groups.keys())[:20]} (выведено до 20)")

    # Логирование изменений
    updated_groups = set()
    for group in target_groups:
        if group in source_groups:
            print(f"[ОБНОВЛЕНИЕ] Группа '{group}' удалена из целевого плейлиста и заменена на данные из первого исходника.")
            target_groups[group] = source_groups[group]
            updated_groups.add(group)

    print(f"Обновленные группы: {sorted(updated_groups)}")

    # Обновляем специальную группу из второго исходника
    if special_group and special_source:
        special_source_groups = parse_m3u(special_source)
        if special_group in special_source_groups and special_group in target_groups:
            print(f"[ОБНОВЛЕНИЕ] Группа '{special_group}' удалена из целевого плейлиста и заменена на данные из второго исходника.")
            target_groups[special_group] = special_source_groups[special_group]

    # Извлекаем строки метаданных
    metadata_lines = extract_metadata(target_url)

    # Формируем обновлённый плейлист
    with open(output_file, "w", encoding="utf-8") as f:
        # Добавляем строки метаданных
        for metadata_line in metadata_lines:
            f.write(f"{metadata_line}\n")
        
        # Добавляем группы и каналы
        for group, channels in target_groups.items():
            for channel in channels:
                f.write(f"{channel}\n")
    
    print(f"Плейлист успешно обновлён и сохранён в {output_file}!")


# Основная функция
if __name__ == "__main__":
    # URL исходных плейлистов
    source_url_1 = "https://raw.githubusercontent.com/IPTVSHARED/iptv/refs/heads/main/IPTV_SHARED.m3u"
    source_url_2 = "https://raw.githubusercontent.com/Dimonovich/TV/Dimonovich/FREE/TV"
    target_url = "https://cdn.jsdelivr.net/gh/dikai669/playlist@main/mpll.m3u"
    output_file = "mpll.m3u"

    # Название группы для обновления из второго исходника
    special_group = "Lime (VPN 🇷🇺)"

    # Обновляем плейлист
    try:
        update_playlist(
            source_urls=[source_url_1, source_url_2],
            target_url=target_url,
            output_file=output_file,
            special_group=special_group,
            special_source=source_url_2
        )
    except Exception as e:
        print(f"Ошибка: {e}")
