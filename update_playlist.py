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
    current_group = None
    group_content = []

    for line in lines:
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
        elif line.startswith("http"):
            group_content.append(line)

    # Добавляем последнюю группу
    if current_group and group_content:
        groups[current_group] = group_content

    return groups

# Функция для обновления плейлиста
def update_playlist(source_url, target_url, output_file):
    """Обновляет целевой плейлист на основе исходного."""
    source_groups = parse_m3u(source_url)
    target_groups = parse_m3u(target_url)
    
    # Обновляем группы в целевом плейлисте
    for group, channels in source_groups.items():
        if group in target_groups:
            print(f"Обновляется группа: {group}")
            target_groups[group] = channels  # Заменяем содержимое группы
    
    # Формируем обновлённый плейлист
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for group, channels in target_groups.items():
            for channel in channels:
                f.write(f"{channel}\n")
    
    print(f"Плейлист успешно обновлён и сохранён в {output_file}!")

# Основная функция
if __name__ == "__main__":
    # URL исходного и целевого плейлистов
    source_url = "https://raw.githubusercontent.com/IPTVSHARED/iptv/refs/heads/main/IPTV_SHARED.m3u"
    target_url = "https://raw.githubusercontent.com/dikai669/playlist/refs/heads/main/mpll.m3u"
    output_file = "mpll.m3u"

    # Обновляем плейлист
    try:
        update_playlist(source_url, target_url, output_file)
    except Exception as e:
        print(f"Ошибка: {e}")
