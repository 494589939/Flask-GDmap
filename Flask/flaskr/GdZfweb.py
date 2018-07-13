from flask import Flask
from flask import render_template
from flask import redirect,url_for
import config

app =Flask(__name__)
app.config.from_object(config)

@app.route('/')
def index():
    return render_template('index.html')

    
@app.route('/login/')
def login():
    return '这是登录页面'
    

@app.route('/question/<user_name>/')
def question(user_name):    
    if user_name == '1':
        return '成功登录'
    else:
        return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=7913)
