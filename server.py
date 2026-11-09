from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
from datetime import datetime

# http://10.1.141.103
# Список для хранения сообщений в оперативной памяти
messages = []

class ChatHandler(SimpleHTTPRequestHandler):
    # Отдаем список сообщений (GET /api) или сам сайт (GET /)
    def do_GET(self):
        if self.path == '/api':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(messages).encode('utf-8'))
        else:
            super().do_GET()

    # Принимаем новое сообщение (POST /api)
    def do_POST(self):
        if self.path == '/api':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            user = data.get('user', 'Anon')[:15]
            text = data.get('text', '')[:200]

            if text.strip():
                messages.append({
                    'user': user,
                    'text': text,
                    'time': datetime.now().strftime('%H:%M')
                })
                # Оставляем только последние 30 сообщений
                del messages[:-30]

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(messages).encode('utf-8'))

print("Сервер запущен! Откройте в браузере: http://localhost:8080")
HTTPServer(('0.0.0.0', 8080), ChatHandler).serve_forever()
