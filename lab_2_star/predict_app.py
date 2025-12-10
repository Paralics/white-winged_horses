from flask import Flask, request
import sys
from transformers import pipeline
import mysql.connector
import os


app = Flask(__name__)
print("Loading sentiment analysis model...", file=sys.stderr)
classifier = pipeline("sentiment-analysis", model="./local_model")

required_vars = ['DB_NAME', 'DB_USER', 'DB_PASSWORD']
missing = [var for var in required_vars if not os.getenv(var)]

if missing:
    print(f"❌ Отсутствуют переменные: {missing}")
    exit(1)

# Используем
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'db'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
    # 'ssl_disabled': True,
    # 'auth_plugin': 'mysql_native_password'
}


def save_to_db(text, sentiment, probability):
    """Сохранение результата в БД"""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO analysis_results (text, sentiment, probability)
        VALUES (%s, %s, %s)
    ''', (text, sentiment, probability))

    conn.commit()
    cursor.close()
    conn.close()


@app.route('/', methods=['GET', 'POST'])
def analyse_sentiment():
    if request.method == 'GET':
        # Показываем форму для ввода текста
        return '''
        <form method="POST">
            <textarea name="text" rows="4" cols="50"></textarea>
            <br>
            <input type="submit" value="Analyze Sentiment">
        </form>
        '''
    else:  # POST
        text = request.form.get('text', '').strip()

        if not text:
            return "<h3>Ошибка: Введите текст для анализа</h3><a href='/analyse_sentiment'>Назад</a>"

        # Анализ тональности
        result = classifier(text)[0]
        sentiment = str.lower(result['label'])
        score = result['score']
        save_to_db(text, sentiment, score)

        # Красивый текстовый вывод
        return f'''
                <h2>Analysis results</h2>

                <div>
                    <strong>Text:</strong>
                    "{text}"
                </div>

                <div>
                    <strong>Sentiment: {sentiment.upper()}</strong><br>
                    <strong>Probability: {score:.4f}</strong>
                </div>

                <br>
                <a href="/">Analyse more</a>
                '''


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
