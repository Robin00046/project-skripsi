from flask import Flask, render_template
import pdfkit
import os

app = Flask(__name__)
app.config['PDF_FOLDER'] = 'static/pdf/'
app.config['TEMPLATE_FOLDER'] = 'templates/'


@app.route('/')
def index():
    return render_template('test.html')


@app.route('/convert')
def konversi():
    htmlfile = app.config['TEMPLATE_FOLDER'] + 'test.html'
    pdffile = app.config['PDF_FOLDER'] + 'demo.pdf'
    pdfkit.from_file(htmlfile, pdffile)
    return '''Click here to open the
    <a href="http://localhost:5000/static/pdf/demo4.pdf">pdf</a>.'''


if __name__ == '__main__':
    app.run(debug=True)