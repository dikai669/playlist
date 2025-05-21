import requests

def test_fetch_file(url):
    try:
        print(f"Попытка загрузки файла из URL: {url}")
        response = requests.get(url, headers={"Cache-Control": "no-cache"})
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            print("Файл успешно загружен.")
            print("Первые 10 строк файла:")
            for line in response.text.splitlines()[:10]:
                print(line)
        else:
            print(f"Ошибка при загрузке файла. Статус: {response.status_code}")
    
    except Exception as e:
        print(f"Произошла ошибка при загрузке файла: {str(e)}")

if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/dikai669/playlist/refs/heads/main/mpll.m3u "
    test_fetch_file(url)
