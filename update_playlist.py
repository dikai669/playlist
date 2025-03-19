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
    output_file = "mpll.m3u"  # Изменено на имя вашего файла

    # Обновляем плейлист
    try:
        update_playlist(source_url, target_url, output_file)
    except Exception as e:
        print(f"Ошибка: {e}")
