from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm
from app.FinancialModelingPrep import Calendars, CompanyValuation, StockMarket

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Lorum'}

    session = StockMarket()

    active = session.most_active_stock()
    active_head = list(active[0].keys())
    gainers = session.most_gainer_stock()
    gainers_head = list(gainers[0].keys())
    losers = session.most_loser_stock()
    losers_head = list(losers[0].keys())

    return render_template('index.html', title='Home', user=user, gainers=gainers, gainers_head=gainers_head, losers=losers, losers_head=losers_head, active=active, active_head=active_head)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/ipo', methods=['GET'])
def upcoming_ipo():
    user = {'username': 'Lorum1'}
    session = Calendars()
    data = session.ipo_calendar('2021-03-10', '2021-03-30')

    return render_template('upcomingipo.html', title='Upcoming IPO', user=user, data=data)


@app.route('/company/<symbol>', defaults={'symbol': 'AAPL'}, methods=['GET'])
def company_profile(symbol):

    session = CompanyValuation()
    data = session.company_quote(symbol)

    return render_template('companyProfile.html', title='Company Profile', data=data)
