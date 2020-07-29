from endzone.models import User, Post, EventPost, Event
from flask import render_template, url_for, flash, redirect, request, abort
from endzone.forms import RegistrationForm, LoginForm, PostForm, UpdateProfileForm, CreateEventForm
from endzone import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image

import secrets
import os


# Routes will execute the function below when accessing specified URLs.
@app.route("/",     methods=['GET', 'POST'])  # methods allow it to request (GET) data and send (POST) data
@app.route("/home", methods=['GET', 'POST'])
def home():
    # Form used to accept user input
    form = RegistrationForm()
    # Validates data received from POST request
    if form.validate_on_submit():
        # encrypts user's password
        encrypt_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        if request.method == 'POST':
            selection = request.form.get('gender')
            month = request.form.get('birthday_month')
            day = request.form.get('birthday_day')
            year = request.form.get('birthday_year')
            user_age = get_age(year)
            # Sets gender
            if selection == '1':
                gender = 'Male'
            elif selection == '2':
                gender = 'Female'
        # creates user
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=encrypt_pwd, gender=gender,
                    birth_date=day, birth_month=month, birth_year=year, age=user_age, city=form.city.data, state=form.state.data,
                    high_school=form.high_school.data, sport=form.sport.data, position=form.position.data)
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
    # Gets all posts from databse
    posts = Post.query.all()
    # Form used to accept user input
    form = PostForm()
    return render_template('feed.html', title='Sports Feed', posts=posts, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    video_ext = '.mp4'
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        if form.image.data:
            # Gets the filename and splits into name and extension
            # name is not used so it is declared as '_' (dummy variable)
            _, f_ext = os.path.splitext(form.image.data.filename)
            # Checks to see if file is not an mp4 file
            if f_ext != video_ext:
                post.post_image = save_image(form.image.data)
            else:
                post.post_video = save_video(form.image.data)

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
        if form.image.data:
            picture = save_image(form.image.data)
            post.post_image = picture
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('feed', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('createpost.html', title='Update Post', form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'danger')
    return redirect(url_for('feed'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    # If a user is already logged in
    if current_user.is_authenticated:
        return redirect('feed')
    # Form used for accepting user input
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


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    posts = Post.query.all()
    form = UpdateProfileForm()
    image = url_for('static', filename='pics/' + current_user.img_file)
    banner = url_for('static', filename='pics/' + current_user.banner_file)
    return render_template('profile.html', title="Account", posts=posts, banner_image=banner, image=image, form=form)


@app.route('/update-profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.select_file.data:
            current_user.img_file = save_profile_pic(form.select_file.data)

        if form.banner.data:
            current_user.banner_file = save_image(form.banner.data)

        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.high_school = form.high_school.data
        current_user.sport = form.sport.data
        current_user.position = form.position.data
        current_user.about = form.bio.data
        current_user.city = form.city.data
        current_user.state = form.state.data

        # Commits changes made
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.high_school.data = current_user.high_school
        form.sport.data = current_user.sport
        form.position.data = current_user.position
        form.bio.data = current_user.about
        form.city.data = current_user.city
        form.state.data = current_user.state

    image = url_for('static', filename='pics/' + current_user.img_file)
    return render_template('update_profile.html', form=form, image=image)


@app.route('/profile/user%%<int:author_id>', methods=['GET', 'POST'])
@login_required
def get_profile(author_id):
    get_user = User.query.get_or_404(author_id)
    all_posts = Post.query.all()
    image = url_for('static', filename='pics/' + get_user.img_file)
    # If profile selected is profile of current user.
    if get_user.id == current_user.id:
        return redirect(url_for('profile'))
    return render_template('global_profile.html', title=get_user.first_name + ' ' + get_user.last_name, user=get_user, posts=all_posts, image=image)


@app.route('/event')
@login_required
def event():
    # Gets all events in the database
    event_form = Event.query.all()
    return render_template('event.html', event_form=event_form)


@app.route('/event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def get_event(event_id):
    event = Event.query.get_or_404(event_id)
    image = url_for('static', filename='pics/' + event.author.img_file)
    posts = EventPost.query.all()
    return render_template('event_page.html', event=event, image=image, event_id=event_id, posts=posts)


@app.route('/create-event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = CreateEventForm()
    if form.validate_on_submit():
        event_post = Event(title=form.title.data, date=form.date.data, time=form.time.data,
                           location=form.location.data, content=form.content.data, user_id=current_user.id)
        db.session.add(event_post)
        db.session.commit()
        return redirect(url_for('event'))
    return render_template('create_event.html', form=form)


@app.route('/event/update-<int:event_id>', methods=['GET', 'POST'])
@login_required
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.author != current_user:
        abort(403)
    form = CreateEventForm()
    if form.validate_on_submit():
        event.title = form.title.data
        event.date = form.date.data
        event.time = form.time.data
        event.location = form.location.data
        event.content = form.content.data
        db.session.commit()
        return redirect(url_for('event'))
    elif request.method == 'GET':
        form.title.data = event.title
        form.date.data = event.date
        form.time.data = event.time
        form.location.data = event.location
        form.content.data = event.content
    return render_template('update_event.html', title='Update Event', form=form, legend='Update Event')


@app.route('/event/delete-<int:event_id>')
def delete_event(event_id):
    all_posts = EventPost.query.all()
    event = Event.query.get_or_404(event_id)

    # Deletes all posts within the event before deleting actual event
    for post in all_posts:
        if post.event_id == event.id:
            db.session.delete(post)
            db.session.commit()

    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('event'))


@app.route('/event/<int:e_id>/new_post', methods=['GET', 'POST'])
@login_required
def create_event_post(e_id):
    form = PostForm()
    legend = 'Event Post'
    video_ext = '.mp4'
    if form.validate_on_submit():
        new_event = EventPost(title=form.title.data, content=form.content.data, event_id=e_id)
        if form.image.data:
            # Gets the filename and splits into name and extension
            # name is not used so it is declared as '_' (dummy variable)
            _, f_ext = os.path.splitext(form.image.data.filename)
            # Checks to see if file is not an mp4 file
            if f_ext != video_ext:
                new_event.post_image = save_image(form.image.data)
            else:
                new_event.post_video = save_video(form.image.data)
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('get_event', event_id=e_id))
    return render_template('create_eventpost.html', form=form, legend=legend)


@app.route("/event/<int:post_id>/delete/<int:event_ID>", methods=['GET', 'POST'])
@login_required
def update_event_post(post_id, event_ID):
    post = EventPost.query.get_or_404(post_id)
    form = PostForm()
    legend = 'Update Event Post'
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        if form.image.data:
            post.post_image = save_image(form.image.data)
        db.session.commit()
        return redirect(url_for('get_event', event_id=event_ID))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('update_event_post.html', form=form, legend=legend)


@app.route("/event/<int:post_id>/delete/<int:event_ID>", methods=['GET', 'POST'])
@login_required
def delete_event_post(post_id, event_ID):
    post = EventPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'danger')
    return redirect(url_for('get_event', event_id=event_ID))


@app.route("/trending")
@login_required
def trending():
    return render_template('trending.html')


@app.route("/team")
@login_required
def team():
    return render_template('team.html')


@app.route('/friends')
def friends():
    posts = Post.query.all()
    return render_template('friends.html', posts=posts)

# Helper Functions #


# ----------------------------------
# Function: Calculates user's age
#    Input: Year - String
#   Output: Age  - Int
# ----------------------------------
def get_age(year):
    age = 2020 - int(year)
    return age


# ----------------------------------
# Function: Saves profile picture using encoded file name
#    Input: File name - String
#   Output: New file name  - String
# ----------------------------------
def save_profile_pic(form_image):
    encoded_key = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form_image.filename)
    new_file_name = encoded_key + file_extension
    f_path = os.path.join(app.root_path, 'static\pics', new_file_name)
    form_image.save(f_path)
    return new_file_name


# ----------------------------------
# Function: Saves video using encoded file name
#    Input: File name - String
#   Output: New file name  - String
# ----------------------------------
def save_video(video):
    encoded_key = secrets.token_hex(8)
    _, f_ext = os.path.splitext(video.filename)
    new_f_name = encoded_key + f_ext
    f_path = os.path.join(app.root_path, 'static\pics', new_f_name)
    video.save(f_path)
    return new_f_name


# ----------------------------------
# Function: Saves post image using encoded file name
#    Input: File name - String
#   Output: New file name  - String
# ----------------------------------
def save_image(form_image):
    encoded_key = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form_image.filename)
    new_file_name = encoded_key + file_extension
    f_path = os.path.join(app.root_path, 'static\pics', new_file_name)
    form_image.save(f_path)
    return new_file_name
