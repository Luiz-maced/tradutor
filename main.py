from flask import Flask, render_template, request, send_file
from deep_translator import GoogleTranslator
import time
import io

app = Flask(__name__)

app.config['SECRET_KEY'] = 'systemctl'
app.config['DEBUG'] = False 

def enhance_horror_tone(text):
    horror_words = {
        "strange": "perturbador",
        "dark": "sombrio",
        "cold": "gélido",
        "silent": "silencioso demais",
        "alone": "totalmente só",
        "shadow": "sombra ameaçadora",
        "fear": "terror profundo",
        "death": "morte iminente",
        "creep": "arrepio na espinha"
    }
    for word, horror_word in horror_words.items():
        text = text.replace(word, horror_word)
    return text

def translate_large_text(text, source_lang='en', target_lang='pt', chunk_size=3000):
    segments = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    translated_text = ""
    translator = GoogleTranslator(source=source_lang, target=target_lang)
    for segment in segments:
        try:
            translated_segment = translator.translate(segment)
            translated_segment = enhance_horror_tone(translated_segment)
            translated_text += translated_segment + " "
            time.sleep(1)
        except Exception as e:
            translated_text += " [Erro na tradução de um segmento] "
    return translated_text.strip()

@app.route('/', methods=['GET', 'POST'])
def translate():
    translation = ""
    if request.method == 'POST':
        original_text = request.form['text']
        try:
            translation = translate_large_text(original_text)
        except Exception as e:
            translation = "Erro na tradução. Tente novamente mais tarde."
    return render_template('index.html', translation=translation)

@app.route('/download', methods=['POST'])
def download():
    translated_text = request.form['translated_text']
    filename = "CreepyTradutor.txt"
    file_content = f"--- CreepyTradutor ---\n\n{translated_text}"

    return send_file(
        io.BytesIO(file_content.encode('utf-8')),
        as_attachment=True,
        download_name=filename,
        mimetype='text/plain'
    )

if __name__ == '__main__':
    app.run(debug=False)