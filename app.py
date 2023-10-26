from flask import Flask, render_template, request
from plagiarism_checker import plagiarism_checker


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_plagiarism():
    text_to_check = request.form['text_to_check']

    result=plagiarism_checker(text_to_check)
    
#     plagiarism_results = {
#   "Disaster studies have measured food insecurity\r\nprimarily following events such as hurricanes\r\nand during the COVID-19 pandemic in the\r\nUnited States. Individual households are often\r\nmost heavily affected. This is clear in studies of\r\nhouseholds displaced by Hurricanes Katrina\r\nand Harvey, in which participants were asked\r\nwhether they had enough money for food the\r\nfamily needed.": {
#     "score": 100,
#     "url": "https://mdsoar.org/handle/11603/27623"
#   }}
    
    return render_template('index.html', plagiarism_results=result)


if __name__ == '__main__':
    app.run(debug=True)
