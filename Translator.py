from flask import Flask, request, jsonify, render_template
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    app.logger.info("Solicitud POST recibida en /translate")
    data = request.get_json()

    if not data:
        app.logger.error("No se recibieron datos en la solicitud.")
        return jsonify({'error': 'No se recibieron datos en la solicitud.'}), 400

    text = data.get('text')
    target_language = data.get('target_language')

    if not text or not target_language:
        app.logger.error("Faltan datos en la solicitud.")
        return jsonify({'error': 'Faltan datos de texto o idioma destino'}), 400

    try:
        translated = translator.translate(text, dest=target_language)
        app.logger.info(f"Texto traducido: {translated.text}")
        return jsonify({'translated_text': translated.text})
    except Exception as e:
        app.logger.error(f"Error al traducir: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
