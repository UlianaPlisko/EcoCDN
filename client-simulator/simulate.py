import requests
import sys
import time

SDN_CONTROLLER = "http://sdn-controller:5005"


def request_book(book_name):
    print(f"Запрашиваю маршрут для: {book_name}...")
    try:
        route_resp = requests.get(f"{SDN_CONTROLLER}/route", params={"item": book_name}, timeout=5)
        route_resp.raise_for_status()
        data = route_resp.json()
        edge_url = data["route_to"]
        print(f"Маршрут получен: {edge_url}")

        # Запрашиваем PDF у edge-сервера
        print("Получаю файл от edge-сервера...")
        start_time = time.time()
        file_resp = requests.get(edge_url, timeout=10)
        duration = time.time() - start_time

        if file_resp.status_code == 200:
            print(f"Файл получен. Размер: {len(file_resp.content)} байт")
            print(f"Время загрузки: {duration:.3f} сек")
            print(f"Кэш: {file_resp.headers.get('X-Cache', 'N/A')}")

            # Сохраняем результат
            with open(f"received_{book_name}", "wb") as f:
                f.write(file_resp.content)
            print(f"Файл сохранён как received_{book_name}")
        else:
            print(f"Ошибка при получении файла: {file_resp.status_code}")

    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python simulate.py <название_файла>")
    else:
        request_book(sys.argv[1])
