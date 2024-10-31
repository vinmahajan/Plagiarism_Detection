from flask import Flask, render_template, request
from src.plagiarism_checker import plagiarism_checker

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>VINM Home page.   go to : /plagiarism-checker </h1>"


@app.route('/plagiarism-checker')
def index():
    return render_template('index.html')

@app.route('/plagiarism-checker', methods=['POST'])
def check_plagiarism():
    text_to_check = request.form['text_to_check']

    result=plagiarism_checker(text_to_check)
    
    return render_template('index.html', plagiarism_results=result)


if __name__ == '__main__':
    app.run(debug=True)
