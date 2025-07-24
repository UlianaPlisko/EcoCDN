import os
from flask import Flask, send_from_directory, abort

# Рабочая директория для хранения книг
BOOK_DIR = os.path.join(os.getcwd(), 'books')

app = Flask(__name__)

@app.route('/books/<filename>')
def serve_book(filename):
    """
    Отдаёт файл PDF из папки 'books'.
    Если файл не найден — возвращает 404.
    """
    # Безопасная отдача файлов
    try:
        return send_from_directory(BOOK_DIR, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route('/')
def index():
    """
    Список доступных книг в каталоге.
    """
    files = os.listdir(BOOK_DIR)
    pdfs = [f for f in files if f.lower().endswith('.pdf')]
    links = [f"<li><a href='/books/{pdf}'>{pdf}</a></li>" for pdf in pdfs]
    return f"<h1>Digital Library</h1><ul>{''.join(links)}</ul>"

if __name__ == '__main__':
    # Убедимся, что папка с книгами существует
    os.makedirs(BOOK_DIR, exist_ok=True)
    app.run(host='0.0.0.0', port=5000)