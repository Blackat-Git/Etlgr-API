import time
from bs4 import BeautifulSoup
from flask import Flask, jsonify
import requests

app = Flask(__name__)

# settings
app.config['JSON_AS_ASCII'] = False  # Кодирование в ASCII
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # Отступы
app.config['JSON_SORT_KEYS'] = False  # Упорядоченные ключи


# возобновление работы сервера
@app.route('/re')
def restart():
    a = 0
    while True:
        url = 'http://127.0.0.1:4567'  # url
        r = requests.get(url)  # отправляем HTTP запрос
        a += 1
        print(f'Restart server {a}')
        time.sleep(300)  # 5 минут


@app.route("/")
def index():
    return jsonify('api etlgr')


@app.route('/<id_tg>')
def get_etlgr(id_tg):
    global status, username, date
    try:
        url = f'http://etlgr.io/conversations/{id_tg}/subscription/'  # url страницы
        r = requests.get(url)  # отправляем HTTP запрос и получаем результат
        soup = BeautifulSoup(r.text, 'html.parser')
        username = soup.find('p').get_text(strip=True).replace(' ', '').replace('.', '')
        # Date
        date = soup.find_all('td')
        for date in date:
            soup.find('td').get_text(strip=True)
        date = date.get_text(strip=True)
        status = True
    except:
        status = False
        username = ''
        date = ''
        id_tg = ''
    finally:
        etlgr = {'status': status,
                 'id_tg': id_tg,
                 'username': username,
                 'date': date}
        # print
        print(etlgr)
        return jsonify(etlgr)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4567)
