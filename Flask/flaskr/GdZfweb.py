from flask import Flask
from flask import render_template
from flask import redirect,url_for
import config

app =Flask(__name__)
app.config.from_object(config)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=7913)
