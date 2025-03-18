import requests
import re

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

    # Ищем группу, содержащую слово "Lime" в исходном плейлисте
    lime_vpn_content = None
    for group_name, group_content in source_groups.items():
        print(f"Проверяется группа: '{group_name}'")  # Отладочный вывод
        if re.search(r'Lime', group_name, re.IGNORECASE):  # Ищем частичное совпадение, игнорируем регистр
            print(f"Найдена группа '{group_name}' в исходном плейлисте")
            lime_vpn_content = group_content
            break

    # Если нашли группу, заменяем содержимое группы "Lime" в моём плейлисте
    if lime_vpn_content:
        if "Lime" in my_groups:
            print("Заменяем содержимое группы 'Lime' на найденную группу")
            my_groups["Lime"] = lime_vpn_content
        else:
            print("Группа 'Lime' не найдена в вашем плейлисте")
    else:
        print("Группа, содержащая слово 'Lime', не найдена в исходном плейлисте")

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
    my_url = "https://raw.githubusercontent.com/dikai669/playlist/refs/heads/main/dzm4.txt"

    # Загружаем плейлисты
    try:
        source_playlist = load_playlist(source_url)
        my_playlist = load_playlist(my_url)
    except Exception as e:
        print(f"Ошибка при загрузке плейлиста: {e}")
        return

    # Объединяем плейлисты
    updated_playlist = merge_playlists(my_playlist, source_playlist)

    # Перезаписываем старый файл dzm4.txt
    try:
        with open("dzm4.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(updated_playlist))
        print("Старый файл 'dzm4.txt' успешно обновлён.")
    except Exception as e:
        print(f"Ошибка при записи файла: {e}")

if __name__ == "__main__":
    main()
