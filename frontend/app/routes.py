from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm
# import FinancialModelingPrep

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Lorum'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


# @app.route('/ipo', methods=['GET','POST'])
# def upcoming_ipo():
#     session = FinancialModelingPrep.Calendars()
#     data = session.ipo_calendar('2021-03-10', '2021-03-30')

#     data = json_normalize(data)

#     return render_template('upcomingipo.html',tables=[data.to_html(classes='ipo')], titles = ['Upcoming IPO'])



