from flask import Flask
from flask import session
from markupsafe import escape
from flask import request, render_template, redirect, url_for
from os import path
import os

app = Flask(__name__)

# Generate yours use: import os; print(os.urandom(16))
# app.secret_key = b'\x05\x81X\xca\xbf\x13#jI\xc7\x9eOH?\xa1\xa5'
app.secret_key = os.urandom(16)

# Generate yours use:
#''.join(random.choices(string.ascii_uppercase + string.digits, k=32))
KEY = "DFYXKCVABP0J3JD8HDTSPX29VGN9FOG1"

if not path.exists("gists"):
    os.mkdir("gists")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        key = request.form['key']
        if key != KEY:
            return '<p>winner here! <img src="/static/evil.jpg"/></p>'
        session['key'] = key
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=key>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/logout')
def logout():
    session.pop('key', None)
    return redirect(url_for('login'))


@app.route("/")
def index():
    return "<p>Go to <code>/gist/NEW_NAME</code> to create new gist</p>"


@app.route('/gist/<name>', methods=['GET', 'POST'])
def gist(name):
    if 'key' not in session:
        return '<p>pity <img src="/static/evil.jpg"/></p>'

    # Do we need `werkzeug.utils.secure_filename` here
    if not name.isalnum():
        return '<p>evil <img src="/static/evil.jpg"/></p>'

    if request.method == 'POST':
        content = request.form['content']
        with open(path.join("./gists/", name), "w") as f:
            f.write(content)
        return redirect(url_for('gist', name=name))
    else:
        content = "Not Found"

        try:
            with open(path.join("./gists/", name)) as f:
                content = f.read()
                return render_template('gist.html', content=content, name=name)
        except BaseException:
            return render_template('new.html', name=name)
