from flask import Flask, make_response, render_template, url_for, request, after_this_request, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'my unobvious secret keyasdfasdf1234123xxx'

@app.before_request
def get_rq():
    c = request.cookies.get('un')
    if c is not None:
        @after_this_request
        def get_afq(response):
            response.set_cookie('ts', c)

@app.route('/')
def hello():
    resp = make_response(render_template('index.html'))
    resp.set_cookie('vt', 'vistors')
    return resp

@app.route('/login/', methods=['GET', 'POST'])
def login():
    isOK=False
    print(request.form)
    if request.method == 'POST':
        uname = request.form['username']
        upwd = request.form['password']
        print("Username:%s, password:%s" % (uname, upwd))
        msg=''
        if uname == 'admin' and upwd == '123':
            isOK = True
            msg = 'auth successfull!'
        else:
            msg = 'auth failed'
        flash(msg)

    return render_template('/auth/login.html')


@app.route('/logout')
def logout():
    return 'logout'


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/post/<int:post_id>')
def post(post_id):
    return 'Post %d' % post_id


@app.route('/user/<user_name>')
def user(user_name):
    return 'User: %s' % user_name


@app.route('/profile/<user_name>')
def profile(user_name):
    return '{}\'s profile'.format(user_name)


@app.route('/path/<path:subpath>')
def show_path(subpath):
    return 'Subpath: %s' % subpath


@app.route('/req', methods=['GET', 'POST'])
def req():
    if request.method == 'GET':
        return req_get()
    else:
        return req_post()


def req_get():
    return 'http get req'


def req_post():
    return 'http post req'

@app.route('/items/')
@app.route('/items/<name>')
def get_item_list(name=None):
    ablist = ['a', 'b', 'c', 'e']
    ALL_ITEMS = [{'title': 'java', 'item_id': 1}, {'item_id':2, 'title': 'python'}, {'item_id':3, 'title': 'golang'}]

    return render_template('item_list.html', items=ALL_ITEMS, name=name, ablist=ablist)

@app.route('/up/', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/tmp/' + secure_filename(f.filename))

        with open('/tmp/a.txt','r') as ff:
            print(ff.readlines())
    return 'up ok!'


@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp


with app.test_request_context():
    print(url_for('register'))
    print(url_for('hello'))
    # print(url_for('login'))
    # print(url_for('login', next='/'))
    print(url_for('profile', user_name='John'))
    print(url_for('static', filename='style.css'))

if __name__ == '__main__':
    # app.run(host='0.0.0.0')
    app.run()
