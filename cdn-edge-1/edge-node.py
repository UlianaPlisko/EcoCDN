import os
import requests
import gzip
from flask import Flask, send_file, abort, Response
from io import BytesIO

# Настройки
ORIGIN_SERVER = 'http://cdn-origin:5000'
CACHE_DIR = os.path.join(os.getcwd(), 'cache')

app = Flask(__name__)

# Убедимся, что папка для кэша существует
os.makedirs(CACHE_DIR, exist_ok=True)

@app.route('/books/<filename>')
def get_book(filename):
    cache_path = os.path.join(CACHE_DIR, filename + '.gz')

    # Если файл есть в кэше — отдаём его
    if os.path.exists(cache_path):
        with open(cache_path, 'rb') as f:
            compressed = f.read()
        return Response(compressed, mimetype='application/pdf', headers={
            'Content-Encoding': 'gzip',
            'X-Cache': 'HIT'
        })

    # Если нет — получаем с origin
    try:
        origin_resp = requests.get(f"{ORIGIN_SERVER}/books/{filename}", timeout=3)
        origin_resp.raise_for_status()
        content = origin_resp.content

        # Сохраняем сжатую версию в кэш
        with gzip.open(cache_path, 'wb') as f:
            f.write(content)

        return Response(content, mimetype='application/pdf', headers={
            'Content-Encoding': 'identity',
            'X-Cache': 'MISS'
        })

    except requests.RequestException:
        abort(404)

@app.route('/')
def index():
    files = [f[:-3] for f in os.listdir(CACHE_DIR) if f.endswith('.gz')]
    links = [f"<li><a href='/books/{name}'>{name}</a></li>" for name in files]
    return f"<h1>CDN Edge Cache</h1><ul>{''.join(links)}</ul>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)