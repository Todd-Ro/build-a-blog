from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Post(db.Model):

    post_keyid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    archived = db.Column(db.Boolean)
    post_heading = db.Column(db.String(50))

    def __init__(self, name, heading):
        self.name = name
        self.archived = False
        self.post_heading = heading


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        post_name = request.form['blog_post']
        post_header = request.form['post_heading']
        new_post = Post(post_name, post_header)

        db.session.add(new_post)
        db.session.commit()

    posts = Post.query.filter_by(archived=False).all()
    archived_posts = Post.query.filter_by(archived=True).all()
    return render_template('home.html', title="Build a Blog", 
        posts=posts, archived_posts=archived_posts)

@app.route('/blog', methods=['GET', 'POST'])
def blog_posts():
    posts = Post.query.filter_by(archived=False).all()
    archived_posts = Post.query.filter_by(archived=True).all()
    return render_template('blog.html', title="Build a Blog Posts", 
        posts=posts, archived_posts=archived_posts)

@app.route('/newpost', methods=['GET', 'POST'])
def new_post():
    warning = ""
    post_heading=""
    new_post=""
    if request.method == 'POST':
        post_name = request.form['blog_post']
        post_header = request.form['post_heading']
        if post_name and post_header:
            new_post = Post(post_name, post_header)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/onepost?onepostid='+str(new_post.post_keyid))
        else:
            warning="Make sure to enter both post text and a header"
            new_post=post_name
            post_heading=post_header

    posts = Post.query.filter_by(archived=False).all()
    return render_template('newpost.html', title="New Post Submission",
        posts=posts, warning=warning, post_heading=post_heading, new_post=new_post)


@app.route("/archive-post", methods=['POST'])
def archive_post():
     
    post_keyid = int(request.form['post-id'])
    post = Post.query.get(post_keyid)
    post.archived = True
    db.session.add(post)
    db.session.commit()

    return redirect('/')

@app.route("/onepost", methods=['POST', 'GET'])
def show_a_blog():
    post = Post.query.filter_by(post_keyid=request.args.get('onepostid')).first()
    return render_template('onepost.html', title="This Blog",
        post=post)

if __name__ == '__main__':
    app.run()