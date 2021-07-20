from flask import Flask
from markupsafe import escape
from flask import request,render_template,redirect,url_for
from os import path
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>/gist/<name></p>"




@app.route('/gist/<name>', methods=['GET','POST'])
def gist(name):
    if not name.isalnum():
        return '<p>evil <img src="/static/evil.jpg"/></p>'

    if request.method == 'POST':
        content = request.form['content']
        with open(path.join("./gists/",name),"w") as f:
            f.write(content)
        return redirect(url_for('gist', name=name))
    else:
        content = "Not Found"
        try:
            with open(path.join("./gists/",name)) as f:
                content = f.read()
                return render_template('gist.html',content=content, name=name)
        except:
            return render_template('new.html', name=name)



