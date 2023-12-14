from app import app, db, models
from flask import (render_template, flash, redirect,
                   url_for, request, jsonify, session)


from .forms import SignUpForm
from .forms import LogInForm
from .forms import SetUpForm
from .forms import UpdateForm
from .forms import GroupForm
from .forms import JoinGroupForm
from .forms import LeaveGroupForm

import os
from werkzeug.utils import secure_filename


@app.route('/', methods=['POST', 'GET'])
def index():
    form1 = LogInForm()
    form2 = SignUpForm()

    if request.method == 'POST':
        if 'signup_submit' in request.form:
            # Form 2 (SignUpForm) is submitted
            if form2.validate_on_submit():
                uservalue = form2.username.data
                passvalue = form2.password.data
                checkpassvalue = form2.checkpass.data

                existing_user = models.Users.query.filter_by(
                                                             username=uservalue
                                                             ).first()

                if existing_user is None:
                    if passvalue == checkpassvalue:
                        new_user = models.Users(username=uservalue,
                                                password=passvalue)
                        db.session.add(new_user)
                        db.session.commit()
                        # Redirect after successful signup
                        return redirect("/setup/" + uservalue)
                    else:
                        flash("Passwords do not match", 'error')
                else:
                    # Redirect if user already exists
                    flash("Username already taken.", 'error')

        elif 'login_submit' in request.form:
            # Form 1 (LogInForm) is submitted
            if form1.validate_on_submit():
                logging_user = (models.Users.query.
                                filter_by
                                (
                                 username=form1.username.data
                                 ).first())

                if (logging_user
                    is not None and
                    (logging_user.password ==
                     form1.password.data)):
                    return redirect(url_for
                                    ('home',
                                     username=form1.username.data))
                else:
                    flash("Incorrect Username or Password", 'error')

    return render_template('index.html', form2=form2, form1=form1)


@app.route('/home/<string:username>', methods=['POST', 'GET'])
def home(username):
    form1 = UpdateForm()
    if 'update_submit' in request.form:
        existing_user = models.Users.query.filter_by(username=username).first()

        # Update fields only if they are not None and not empty
        if form1.firstName.data is not None and form1.firstName.data.strip():
            existing_user.firstName = form1.firstName.data
        if form1.secondName.data is not None and form1.secondName.data.strip():
            existing_user.secondName = form1.secondName.data
        if form1.weight.data is not None:
            existing_user.weight = form1.weight.data
        if form1.height.data is not None:
            existing_user.height = form1.height.data
        if form1.squat.data is not None:
            existing_user.squat = form1.squat.data
        if form1.bench.data is not None:
            existing_user.bench = form1.bench.data
        if form1.deadlift.data is not None:
            existing_user.deadlift = form1.deadlift.data
        db.session.commit()
        return redirect("/home/" + username)
    session['loggedUsername'] = username

    user = models.Users.query.filter_by(username=username).first()
    return render_template('home.html', username=username,
                           user=user, form1=form1)


@app.route('/upload/<string:username>', methods=['POST'])
def upload(username):
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # Ensure the uploads directory exists
            uploads_dir = os.path.join(app.root_path,
                                       app.config['UPLOAD_FOLDER'])
            os.makedirs(uploads_dir, exist_ok=True)

            file_path = os.path.join(uploads_dir, filename)
            file.save(file_path)

            # Update the user's profile image in the database
            user = (models.Users.query.
                    filter_by(username=username).first())

            user.profile_image = filename
            db.session.commit()

    return "Error uploading image", 400


def get_suggestions_from_db(search_term):
    # Query the database to get suggestions based on the search term
    suggestions = models.Users.query.filter(models.Users.username
                                            .ilike(f"%{search_term}%"
                                                   )).limit(5).all()
    return [user.username for user in suggestions]


def get_group_suggestions_from_db(search_term):
    # Query the database to get suggestions based on the search term
    suggestions = (models.Groups.query.filter
                   (models.Groups.groupName.
                    ilike(f"%{search_term}%")).
                   limit(5).all())
    return [group.groupName for group in suggestions]


@app.route('/get_suggestions', methods=['GET'])
def get_suggestions():
    search_term = request.args.get('search_term')
    suggestions = get_suggestions_from_db(search_term)
    return jsonify(suggestions)


@app.route('/get_group_suggestions', methods=['GET'])
def get_group_suggestions():
    search_term = request.args.get('search_term')
    suggestions = get_group_suggestions_from_db(search_term)
    return jsonify(suggestions)


def allowed_file(filename):
    return ('.' in filename and filename.rsplit('.', 1)[1].lower()
            in app.config['ALLOWED_EXTENSIONS'])


@app.route('/groups/<string:username>', methods=['POST', 'GET'])
def groups(username):
    form1 = GroupForm()
    user = models.Users.query.filter_by(username=username).first()
    if 'group_submit' in request.form:
        nameVal = form1.groupName.data
        bioVal = form1.groupBio.data
        new_group = models.Groups(groupName=nameVal,
                                  groupBio=bioVal)
        db.session.add(new_group)
        new_group.users.append(user)
        db.session.commit()
        print("you made it here")

    all_groups = user.groups

    return render_template('groups.html', user=user,
                           form1=form1, groups=all_groups)


@app.route('/profile/<string:username>', methods=['POST', 'GET'])
def profile(username):
    user = models.Users.query.filter_by(username=username).first()
    all_groups = user.groups
    total_lift = user.squat + user.bench + user.deadlift
    if total_lift <= 350:
        overalllevel = "bronze.png"
        overval = ((total_lift)/350)*100
    elif 350 < total_lift <= 500:
        overalllevel = "silver.png"
        overval = ((total_lift-350)/150)*100
    elif 500 < total_lift <= 700:
        overalllevel = "gold.png"
        overval = ((total_lift-500)/200)*100
    else:
        overalllevel = "diamond.png"
        overval = 100

    if user.squat <= 100:
        squatlevel = "bronze.png"
        squatval = ((user.squat)/100)*100
    elif 100 < user.squat <= 150:
        squatlevel = "silver.png"
        squatval = ((user.squat-100)/50)*100
    elif 150 < user.squat <= 200:
        squatlevel = "gold.png"
        squatval = ((user.squat-200)/50)*100
    else:
        squatlevel = "diamond.png"
        squatval = 100

    if user.bench <= 100:
        benchlevel = "bronze.png"
        benchval = user.bench
    elif 100 < user.bench <= 150:
        benchlevel = "silver.png"
        benchval = ((user.bench-100)/50)*100
    elif 150 < user.bench <= 200:
        benchlevel = "gold.png"
        benchval = ((user.bench-200)/50)*100
    else:
        benchlevel = "diamond.png"
        benchval = 100

    if user.deadlift <= 100:
        deadliftlevel = "bronze.png"
        deadliftval = user.deadlift
    elif 100 < user.bench <= 200:
        deadliftlevel = "silver.png"
        deadliftval = ((user.deadlift-100)/100)*100
    elif 200 < user.bench <= 300:
        deadliftlevel = "gold.png"
        deadliftval = ((user.deadlift-200)/100)*100
    else:
        deadliftlevel = "diamond.png"
        deadliftval = 100
    loggeduser = session.get("loggedUsername")
    return render_template('profile.html', username=username, user=user,
                           groups=all_groups, level=overalllevel,
                           deadlift=deadliftlevel, bench=benchlevel,
                           squat=squatlevel, squatval=squatval,
                           benchval=benchval, deadliftval=deadliftval,
                           overval=overval, loggeduser=loggeduser)


@app.route('/setup/<string:username>', methods=['POST', 'GET'])
def setup(username):
    form1 = SetUpForm()
    if 'setup_submit' in request.form:
        if form1.validate_on_submit():
            existing_user = (models.Users.query.filter_by
                             (username=username).first())
            existing_user.firstName = form1.firstName.data
            existing_user.secondName = form1.secondName.data
            existing_user.weight = form1.weight.data
            existing_user.height = form1.height.data
            existing_user.squat = form1.squat.data
            existing_user.bench = form1.bench.data
            existing_user.deadlift = form1.deadlift.data
            db.session.commit()
            return redirect("/home/" + username)

    user = models.Users.query.filter_by(username=username).first()
    return render_template('setup.html', user=user, form1=form1)


@app.route('/group/<string:groupName>/<string:username>',
           methods=['POST', 'GET'])
def group(groupName, username):
    user = models.Users.query.filter_by(username=username).first()
    username = username
    group = models.Groups.query.filter_by(groupName=groupName).first()
    return render_template('group.html', group=group,
                           user=user, username=username)


@app.route('/join_group/<string:groupName>/<string:username>',
           methods=['POST'])
def join_group(groupName, username):
    user = models.Users.query.filter_by(username=username).first()
    group = models.Groups.query.filter_by(groupName=groupName).first()

    if user not in group.users:
        p = 1

    group.users.append(user)
    db.session.commit()

    return redirect(url_for('group', groupName=groupName,
                    username=username, p=p))


@app.route('/leave_group/<string:groupName>/<string:username>',
           methods=['POST'])
def leave_group(groupName, username):
    user = models.Users.query.filter_by(username=username).first()
    group = models.Groups.query.filter_by(groupName=groupName).first()

    group.users.remove(user)
    db.session.commit()

    return redirect(url_for('groups', username=username))


@app.route('/milestones/<string:username>', methods=['POST', 'GET'])
def milestones(username):
    user = models.Users.query.filter_by(username=username).first()
    total_lift = user.squat + user.bench + user.deadlift
    if total_lift <= 350:
        overalllevel = "bronze.png"
        overval = ((total_lift)/350)*100
    elif 350 < total_lift <= 500:
        overalllevel = "silver.png"
        overval = ((total_lift-350)/150)*100
    elif 500 < total_lift <= 700:
        overalllevel = "gold.png"
        overval = ((total_lift-500)/200)*100
    else:
        overalllevel = "diamond.png"
        overval = 100

    if user.squat <= 100:
        squatlevel = "bronze.png"
        squatval = ((user.squat)/100)*100
    elif 100 < user.squat <= 150:
        squatlevel = "silver.png"
        squatval = ((user.squat-100)/50)*100
    elif 150 < user.squat <= 200:
        squatlevel = "gold.png"
        squatval = ((user.squat-200)/50)*100
    else:
        squatlevel = "diamond.png"
        squatval = 100

    if user.bench <= 100:
        benchlevel = "bronze.png"
        benchval = user.bench
    elif 100 < user.bench <= 150:
        benchlevel = "silver.png"
        benchval = ((user.bench-100)/50)*100
    elif 150 < user.bench <= 200:
        benchlevel = "gold.png"
        benchval = ((user.bench-200)/50)*100
    else:
        benchlevel = "diamond.png"
        benchval = 100

    if user.deadlift <= 100:
        deadliftlevel = "bronze.png"
        deadliftval = user.deadlift
    elif 100 < user.bench <= 200:
        deadliftlevel = "silver.png"
        deadliftval = ((user.deadlift-100)/100)*100
    elif 200 < user.bench <= 300:
        deadliftlevel = "gold.png"
        deadliftval = ((user.deadlift-200)/100)*100
    else:
        deadliftlevel = "diamond.png"
        deadliftval = 100

    return render_template("milestones.html", user=user, level=overalllevel,
                           deadlift=deadliftlevel, bench=benchlevel,
                           squat=squatlevel, squatval=squatval,
                           benchval=benchval, deadliftval=deadliftval,
                           overval=overval)
