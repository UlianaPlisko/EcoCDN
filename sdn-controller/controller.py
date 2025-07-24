from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Список доступных CDN-узлов (можно расширять)
EDGE_NODES = [
    {"name": "edge-1", "url": "http://cdn-edge-1:5001"},
    # В будущем можно добавить другие факультеты / edge-2, edge-3 и т.д.
]

@app.route('/route', methods=['GET'])
def route():
    """
    Простейший контроллер маршрутизации: выбирает случайный edge.
    В будущем здесь можно реализовать логику на основе:
    - Задержки
    - Нагрузки
    - Потребления энергии
    - Географии
    """
    item = request.args.get('item')
    selected = random.choice(EDGE_NODES)
    return jsonify({
        "route_to": f"{selected['url']}/books/{item}",
        "edge": selected["name"]
    })

@app.route('/')
def status():
    return "<h2>SDN Controller is Running</h2><p>Use /route?item=book1.pdf</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)