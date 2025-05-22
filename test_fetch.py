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
                groups.add(group_name)  # Добавляем название группы
            
            # Извлекаем название канала
            channel_match = re.search(r',\s*(.+)$', line)
            if channel_match:
                channel_name = channel_match.group(1).strip()
                channels.append(channel_name)  # Добавляем название канала

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
        print(f"- {channel}")
