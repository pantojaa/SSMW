from endzone.models import User, Post
from flask import render_template, url_for, flash, redirect, request, abort
from endzone.forms import RegistrationForm, LoginForm, PostForm
from endzone import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required


# Routes will execute the function below when accessing specified URLs.
@app.route("/",     methods=['GET', 'POST'])  # methods allow it to request (GET) data and send (POST) data
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = RegistrationForm()

    # Validates data received with form
    if form.validate_on_submit():
        # encrypts user's password
        encrypt_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # creates user
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=encrypt_pwd)
        # Stages user
        db.session.add(user)
        # Commits user into database
        db.session.commit()

        flash(f'Account created successfully. Please sign in.', 'success')
        return redirect(url_for('login'))

    return render_template('home.html', title='Home', form=form)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/contact_us")
def contact_us():
    return render_template('contact.html', title='Contact Us')


@app.route("/feed")
@login_required
def feed():
    posts = Post.query.all()
    image = url_for('static', filename='pics/' + current_user.img_file)
    return render_template('feed.html', title='Sports Feed', posts=posts, image=image)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('feed')

    form = LoginForm()

    # Validates data received with form
    if form.validate_on_submit():
        # If data from form is valid it will check to see if it is a valid email and password from database
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('feed'))
        else:
            flash("Invalid email or password. Please try again.", 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html', title="Account")


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success')
        return redirect(url_for('feed'))

    return render_template('createpost.html', title="Create Post", form=form,  legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect( url_for('feed', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('createpost.html', title='Update Post', form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'danger')
    return redirect( url_for('feed'))

