from flask import Flask, jsonify, render_template, request, redirect, url_for, send_file
import time, os
import threading
import lang
import markdown2
app = Flask(__name__)


slide = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = ''
        prompt = request.form['prompt']
        slide['prompt'] = prompt
        return redirect(url_for('options'))
    return render_template('index.html')

@app.route('/options', methods=['GET', 'POST'])
def options():
    if request.method == 'POST':
        slide['fileType'] = request.form['fileType']
        slide['nofpages'] = request.form['nofpages']
        slide['theme'] = request.form['theme']
        return redirect(url_for('generate'))
    return render_template('options.html')

@app.route('/generate', methods=['GET'])
def generate():
    thread = threading.Thread(target=prepare)
    thread.start()
    return render_template('generate.html', slide=slide)

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'progress': slide['progress'], 'status': slide['status']})

@app.route('/view_slide')
def view_slide():
    if slide['fileType'] == 'markdown':
        # Read Markdown content from file
        with open('output/slides.md', 'r') as file:
            markdown_content = file.read()

        # Convert Markdown to HTML
        #html_content = markdown2.markdown(markdown_content)
        slides = markdown_content.split('---')
        return render_template('view_markdown.html', slides=slides)
    if slide['fileType'] == 'latex':
        pdfpath = "slides.pdf"
        return send_file(pdfpath, as_attachment=False)


def prepare():
    if slide['fileType'] == 'markdown':
        print('Generating markdown slides...')
        slide['progress'] = 20
        slide['status'] = 'Generating markdown slides...'
        markdown = lang.generate_markdown_slide(slide['prompt'], slide['nofpages'])
        slide['progress'] = 40
        slide['status'] = 'markdown content generated...'
        md = lang.replace_images(markdown)
        slide['progress'] = 80
        slide['status'] = 'Images added...'
        with open('output/slides.md', 'w') as f:
            f.write(md)
        slide['progress'] = 90
        slide['status'] = 'Slides saved...'
        time.sleep(1)
        slide['progress'] = 100
        slide['status'] = 'Slides generated successfully!'

    if slide['fileType'] == 'latex':
        print('Generating latex slides...')
        slide['progress'] = 20
        slide['status'] = 'Generating latex slides...'
        latex = lang.generate_latex(slide['prompt'], slide['nofpages'])
        slide['progress'] = 40
        slide['status'] = 'latex content generated...'
        with open('output/slides.tex', 'w') as f:
            f.write(latex)
        slide['progress'] = 90
        slide['status'] = 'Slides saved...'
        os.system('pdflatex output/slides.tex')
        slide['progress'] = 100
        slide['status'] = 'Slides generated successfully!'
    return 0

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')