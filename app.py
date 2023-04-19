from flask import Flask, flash, request, redirect, render_template, session, jsonify
from models import connect_database, database, User, Feedback
from forms import RegisterAccountForm, LoginAccountForm, FeedbackForm


app = Flask(__name__)
app.app_context().push()

DATABASE_NAME = 'flask_feedback'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{DATABASE_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config["SECRET_KEY"] = "Phanu!"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_database(app)

@app.route('/')
def index_page():
    """ Hompeage that redirects to register """
    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register_page():
    """ Register page that redirects to user page if logged in if not, goes to register """
    if session.get('username', False):
        return redirect(f'/users/{session["username"]}')
    else:
        form = RegisterAccountForm()
        if form.validate_on_submit():
            user = User.register(form.username.data, form.password.data, form.email.data, form.first_name.data, form.last_name.data)
            database.session.add(user)
            database.session.commit()
            session['username'] = user.username
            return redirect(f'/users/{session["username"]}')
        else:
            return render_template('register.html', form=form)
    
@app.route('/login', methods=["GET", "POST"])
def login_page():
    """ Login page does to user page if already logged in if not goes to login """
    if session.get('username', False):
        return redirect(f'/users/{session["username"]}')
    else:
        form = LoginAccountForm()
        if form.validate_on_submit():
            user = User.authenticate(form.username.data, password=form.password.data)
            if user:
                session['username'] = user.username
                return redirect(f'/users/{session["username"]}')
            else:
                form.username.errors = ['Incorrect username or password']
        
        return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    """ Logout user """
    del session['username']
    return redirect('/')

@app.route('/secret')
def secret_page():
    """ Secret page """
    if session.get('username', False):  
        return render_template('secret.html')
    return redirect('/login')

# USER
@app.route('/users/<string:username>')
def user_page(username):
    """ User page """
    if session.get('username', False) == username:
        user = User.get_user(session['username'])
        return render_template('user.html', user=user, feedbacks=user.feedbacks)
    elif session.get('username', False) == False:
        return redirect('/login')
    else:
        return redirect(f'/users/{session["username"]}')
    
@app.route('/users/<string:username>/delete', methods=['POST'])
def delete_user(username):
    """ Deletes an user """
    if session.get('username', False) == username:
        user = User.get_user(username)
        for feedback in user.feedbacks:
            database.session.delete(feedback)
            database.session.commit()
        database.session.delete(user)
        database.session.commit()
        del session['username']
        return redirect('/')
    elif session.get('username', False) == False:
        return redirect('/login')
    else:
        return redirect(f'/users/{session["username"]}')

@app.route('/users/<string:username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """ Add a feedback """
    if session.get('username', False) == username:
        form = FeedbackForm()

        if form.validate_on_submit():
            feedback = Feedback(title=form.title.data, content=form.content.data, username=session['username'])
            database.session.add(feedback)
            database.session.commit()
            return redirect(f'/users/{session["username"]}')
        else:
            return render_template('feedback_add.html', form=form)
    elif session.get('username', False) == False:
        return redirect('/login')
    else:
        return redirect(f'/users/{session["username"]}')
    
@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    """ Update a feedback """
    feedback = Feedback.query.get_or_404(feedback_id)
    if session.get('username', False) == feedback.username:
        form = FeedbackForm(obj=feedback)
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            database.session.add(feedback)
            database.session.commit()
            return redirect(f'/users/{session["username"]}')
        else:
            return render_template('feedback_update.html', form=form)
    elif session.get('username', False) == False:
        return redirect('/login')
    else:
        return redirect(f'/users/{session["username"]}')
    
@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    """ Delete a feedback """
    feedback = Feedback.query.get_or_404(feedback_id)
    print('--------------------------------------------------------------------')
    print(feedback)

    if session.get('username', False) == feedback.username:
        database.session.delete(feedback)
        database.session.commit()
        return redirect(f'/users/{session["username"]}')

    elif session.get('username', False) == False:
        return redirect('/login')
    else:
        return redirect(f'/users/{session["username"]}')
    
