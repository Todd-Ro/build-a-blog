from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    archived = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        self.archived = False


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        post_name = request.form['blog_post']
        new_post = Post(post_name)
        db.session.add(new_post)
        db.session.commit()

    posts = Post.query.filter_by(archived=False).all()
    archived_posts = Post.query.filter_by(archived=True).all()
    return render_template('blog.html', title="Build a Blog", 
        posts=posts, archived_posts=archived_posts)


@app.route("/archive-post", methods=['POST'])
def archive_post():
     
    post_id = int(request.form['post-id'])
    post = Post.query.get(post_id)
    post.archived = True
    db.session.add(post)
    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run()