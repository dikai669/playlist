import requests
import re

# Функция для загрузки данных из URL без кэширования
def fetch_url(url):
    """Загружает данные из URL без кэширования."""
    response = requests.get(url, headers={"Cache-Control": "no-cache"})
    if response.status_code != 200:
        raise Exception(f"Не удалось загрузить плейлист с URL: {url}. Статус: {response.status_code}")
    
    # Принудительно декодируем данные в UTF-8
    try:
        content = response.content.decode("utf-8")
    except UnicodeDecodeError:
        # Если не UTF-8, пробуем MacRoman или другую кодировку
        content = response.content.decode("MacRoman", errors="replace")
    
    return content.splitlines()

# Функция для извлечения названий групп и каналов
def extract_groups_and_channels(url):
    """Извлекает названия групп и каналов из M3U файла."""
    lines = fetch_url(url)
    groups = set()  # Для хранения уникальных названий групп
    channels = []   # Для хранения названий каналов

    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF"):
            # Извлекаем название группы (если есть)
            group_match = re.search(r'group-title="([^"]+)"', line)
            if group_match:
                group_name = group_match.group(1).strip()
                if group_name:  # Проверяем, что название группы не пустое
                    groups.add(group_name)
            
            # Извлекаем название канала
            channel_match = re.search(r',\s*(.+)$', line)
            if channel_match:
                channel_name = channel_match.group(1).strip()
                if channel_name:  # Проверяем, что название канала не пустое
                    channels.append(channel_name)
            else:
                print(f"Не удалось извлечь название канала из строки: {line}")

    return groups, channels

# Основная функция
if __name__ == "__main__":
    # URL исходных плейлистов
    source_url_1 = "https://raw.githubusercontent.com/IPTVSHARED/iptv/refs/heads/main/IPTV_SHARED.m3u"
    source_url_2 = "https://raw.githubusercontent.com/Dimonovich/TV/Dimonovich/FREE/TV"

    # Извлекаем данные из первого исходника
    print("=== Исходник 1 ===")
    groups_1, channels_1 = extract_groups_and_channels(source_url_1)
    print("Найденные группы:")
    for group in sorted(groups_1):
        print(f"- {group}")
    print("Найденные каналы:")
    for channel in channels_1[:10]:  # Выводим первые 10 каналов
        print(f"- {channel}")

    # Извлекаем данные из второго исходника
    print("\n=== Исходник 2 ===")
    groups_2, channels_2 = extract_groups_and_channels(source_url_2)
    print("Найденные группы:")
    for group in sorted(groups_2):
        print(f"- {group}")
    print("Найденные каналы:")
    for channel in channels_2[:10]:  # Выводим первые 10 каналов
        print(f"- {channel}")  # Добавляем блок кода после for
