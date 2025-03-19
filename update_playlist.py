import requests

def parse_m3u(url):
    """Парсит M3U файл и возвращает словарь групп."""
    response = requests.get(url)
    lines = response.text.splitlines()
    
    groups = {}
    current_group = None
    
    for line in lines:
        if line.startswith("#EXTINF"):
            # Извлекаем название группы из тега EXTGRP
            group = None
            for part in line.split():
                if "group-title=" in part:
                    group = part.split('"')[1]
                    break
            if group:
                current_group = group
                if group not in groups:
                    groups[group] = []
        elif line.startswith("http"):
            if current_group:
                groups[current_group].append(line)
    
    return groups

def update_playlist(source_url, target_url, output_file):
    """Обновляет целевой плейлист на основе исходного."""
    source_groups = parse_m3u(source_url)
    target_groups = parse_m3u(target_url)
    
    # Обновляем группы в целевом плейлисте
    for group, channels in source_groups.items():
        if group in target_groups:
            target_groups[group] = channels  # Заменяем содержимое группы
    
    # Формируем обновлённый плейлист
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for group, channels in target_groups.items():
            for channel in channels:
                f.write(f'#EXTINF:-1 group-title="{group}"\n')
                f.write(f"{channel}\n")

# URL исходного и целевого плейлистов
source_url = "https://raw.githubusercontent.com/IPTVSHARED/iptv/refs/heads/main/IPTV_SHARED.m3u"
target_url = "https://raw.githubusercontent.com/dikai669/playlist/refs/heads/main/mpll.m3u"
output_file = "updated_playlist.m3u"

# Обновляем плейлист
update_playlist(source_url, target_url, output_file)
print("Плейлист успешно обновлён!")
