from flask import Flask, render_template, redirect, url_for,request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import date
today=str(date.today())

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy()
db.init_app(app)


# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

class AddPost(FlaskForm):
    title=StringField("title",[DataRequired()])
    subtitle=StringField("subtitle",[DataRequired()])
    author_name=StringField("author_name",[DataRequired()])
    img=StringField("img",[DataRequired()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField('submit')

with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    posts = db.session.execute(db.select(BlogPost)).scalars().all()
    return render_template("index.html", all_posts=posts)

# TODO: Add a route so that you can click on individual posts.
@app.route('/show_post/<int:post_id>')
def show_post(post_id):

    requested_post =db.get_or_404(BlogPost,post_id)

    return render_template("post.html", post=requested_post)


# TODO: add_new_post() to create a new blog post
@app.route('/add_post',methods=["POST","GET"])
def add_post():
    new_form=AddPost()
    if request.method=="POST":
        new_post=BlogPost(
            title=new_form.title.data,
            subtitle=new_form.subtitle.data,
            date=today,
            body=new_form.body.data,
            author=new_form.author_name.data,
            img_url=new_form.img.data
        )
        db.session.add(new_post)
        db.session.commit()
        return  redirect('/')
    return render_template("make-post.html",form=new_form)


# TODO: edit_post() to change an existing blog post

@app.route('/edit_post/<int:post_id>',methods=["POST",'GET'])
def edit_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)

    new_form=AddPost(
        title=requested_post.title,
        subtitle=requested_post.subtitle,
        author_name=requested_post.author,
        img=requested_post.img_url,
        body=requested_post.body

    )
    if request.method=="POST":
        requested_post.body=new_form.body.data
        requested_post.title=new_form.title.data
        requested_post.subtitle=new_form.subtitle.data
        requested_post.author=new_form.author_name.data
        requested_post.img_url=new_form.img.data
        db.session.commit()
        return redirect("/")


    return render_template("make-post.html",form=new_form,edit=True)

@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    post = db.get_or_404(BlogPost,post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')

# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
