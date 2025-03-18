
import requests

# Функция для загрузки плейлиста по URL
def load_playlist(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.splitlines()
    else:
        raise Exception(f"Не удалось загрузить плейлист с URL: {url}")

# Функция для разбора плейлиста на группы и их содержимое
def parse_playlist(playlist):
    groups = {}
    current_group = None
    group_content = []

    for line in playlist:
        if line.startswith("#EXTINF"):
            group_content.append(line)
        elif line.startswith("http"):
            group_content.append(line)
        elif line.startswith("#EXTGRP:"):
            if current_group and group_content:
                groups[current_group] = group_content
            current_group = line.split(":")[1]
            group_content = []
    
    # Добавляем последнюю группу
    if current_group and group_content:
        groups[current_group] = group_content

    return groups

# Функция для объединения плейлистов
def merge_playlists(my_playlist, source_playlist):
    my_groups = parse_playlist(my_playlist)
    source_groups = parse_playlist(source_playlist)

    for group_name, group_content in my_groups.items():
        if group_name in source_groups:
            # Заменяем содержимое группы из моего плейлиста на содержимое из исходного
            my_groups[group_name] = source_groups[group_name]

    # Формируем обновлённый плейлист
    updated_playlist = []
    for group_name, group_content in my_groups.items():
        updated_playlist.append(f"#EXTGRP:{group_name}")
        updated_playlist.extend(group_content)

    return updated_playlist

# Основная функция
def main():
    # URL-ы плейлистов
    source_url = "https://raw.githubusercontent.com/Dimonovich/TV/Dimonovich/FREE/TV"
    my_url = "https://raw.githubusercontent.com/dikai669/playlist/refs/heads/main/dzm3.txt"

    # Загружаем плейлисты
    source_playlist = load_playlist(source_url)
    my_playlist = load_playlist(my_url)

    # Объединяем плейлисты
    updated_playlist = merge_playlists(my_playlist, source_playlist)

    # Сохраняем обновлённый плейлист в файл
    with open("updated_playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(updated_playlist))

    print("Обновлённый плейлист сохранён в файл 'updated_playlist.m3u'.")

if __name__ == "__main__":
    main()
