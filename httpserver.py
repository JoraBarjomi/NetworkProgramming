from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Получен запрос: {self.path}")
        if self.path == '/':
            self.main_page()
        elif self.path == '/success':
            self.send_success_page()
        elif self.path == '/about':
            self.send_page("О нас", "Информация о компании")
        elif self.path == '/contact':
            self.send_page("Контакты", "Email: info@example.com")       
        elif self.path == '/services':
            self.send_form()        
        else:
            self.send_404()

    def render_template(self, title, content):
        nav = '''
            <nav>
                <a href="/">Главная</a>
                <a href="/about">О нас</a>
                <a href="/services">Услуги</a>
                <a href="/contact">Контакты</a>
            </nav>
        '''

        html = f'''
        <html>
            <head><title>{title}</title></head>
            <body>
                {nav}
                <h1>{title}</h1>
                <p>{content}</p>
            </body>
        </html>
        '''
        return html


    def send_page(self, title, content):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf8')
        self.end_headers()
        html = self.render_template(title, content)
        self.wfile.write(html.encode('utf-8'))

    def send_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write('<h1>404 - Страница не найдена</h1>'.encode('utf-8'))

    def do_POST(self):
        if self.path == '/submit':
            self.handle_form_submission()

    def main_page(self):
        self.send_page("Добро пожаловать!", "Hello, world!!!")
    

    def send_form(self):
        form_html = '''
            <h1>Обратная связь</h1>
            <form action="/submit" method="post">
                <p>
                    <label>Имя:</label><br>
                    <input type="text" name="name" required>
                </p>
                <p>
                    <label>Email:</label><br>
                    <input type="email" name="email" required>
                </p>
                <p>
                    <label>Тема сообщения:</label><br>
                    <textarea name="message" rows="1" cols="25"></textarea>
                </p>
                <p>
                    <label>Сообщение:</label><br>
                    <textarea name="message" rows="5" cols="50"></textarea>
                </p>
                <p>
                    <button type="submit">Отправить</button>
                </p>
            </form>
        '''
        self.send_page("Форма обратной связи", form_html)

    def send_success_page(self):
        form_html = '''
        <html>
                <h1>Обратная связь</h1>
                <p>Спасибо за обратную связь!!!</p>
        '''
        self.send_page("Форма обратной связи", form_html)


    def handle_form_submission(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        # Парсинг данных формы
        form_data = urllib.parse.parse_qs(post_data)
        
        # Валидация
        if not form_data.get('name') or not form_data.get('email'):
            self.send_error(400, "Имя и email обязательны")
            return
        
        # Обработка данных (в реальном приложении - сохранение в БД)
        print(f"Получены данные: {form_data}")
        
        # Перенаправление на страницу успеха
        self.send_response(302)
        self.send_header('Location', '/success')
        self.end_headers()


server = HTTPServer(('localhost', 8080), MyHandler)
print("Сервер запущен на http://localhost:8080") 
server.serve_forever()      