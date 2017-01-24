import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)
# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'portfolio.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='root'
))

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.cli.command('compile')
def compile():
    """Compiles content into static file"""
    # check if exist and delete
    import os
    for f in os.listdir("./output"):
        os.remove(f)
    # generate new file
    compile_index()
    compile_projects()

def compile_index():
    db = get_db()
    cur = db.execute('select title, content from entries order by id desc')
    entries = cur.fetchall() 
    output = render_template('index.html', entries=entries)
    with open('output/index.html', 'w') as f:
        f.write(output)

def compile_projects():
    db = get_db()
    cur = db.execute('select title, content from entries order by id desc')
    entries = cur.fetchall() 
    i = 1
    for entry in entries:
        page = render_template('project.html', entry=entry)
        with open('output/project%d.html' % i, 'w') as f:
            f.write(page)
        i += 1

@app.route("/")
def index():
    db = get_db()
    cur = db.execute('select * from entries order by id desc')
    entries = cur.fetchall() 
    return render_template('dashboard.html', entries=entries)

@app.route("/settings")
def setting():
    return "Setting page"

@app.route("/new", methods=['GET', 'POST'])
def new_project():
    if request.method == 'GET':
        return render_template('form.html')
    elif request.method == 'POST':
        #print request.form
        # save file
        db = get_db()
        db.execute('insert into entries (title, content, url, tags) values (?, ?, ?, ?)',
                 [request.form['name'], request.form['content'], request.form['url'], request.form['tags']])
        db.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('index'))

@app.route("/project/<int:post_id>")
def show_project(post_id):
    return "Post id: %d" % post_id
    #return render_template('')





if __name__ == "__main__":
    app.run()
