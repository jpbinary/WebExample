from flask import Flask, render_template, request, make_response, session, redirect, url_for, escape
import os
app = Flask(__name__)

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    else:
        response_cookie = make_response(render_template('hello.html'))
        response_cookie.set_cookie('username', 'the username')
        return response_cookie

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

# catch all URLs
@app.route('/<path:path>')
def catch_all(path):
    return('You want path: %s' % path)
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    try:
        app.secret_key = os.environ['secret_key'] 
    except KeyError:
        print "Please set (export secret_key=<secret_key>) the secret_key environmental variable"

    app.run(debug=True)

