from myapp import app
from flask import render_template, request, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import required, Email
from myapp.models.searches import Search
from google.appengine.ext import ndb

import logging
import json
import urllib, urllib2
import re

API_KEY = 'your-key'
MASHAPE_KEY = 'your-key'


class MyForm(FlaskForm):
    email = StringField('email', [Email(), required()])
    type = SelectField('search type', choices=[('IMDbID','IMDbID'), ('title', 'title')], validators=[required()])
    value = StringField('value', [required()])
    plot = SelectField('plot length', choices=[('Short', 'Short'), ('Full', 'Full')], validators=[required()])
    submit = SubmitField('search', [required()])


@app.route('/search', methods=['GET'])
def showForm():
    form = MyForm()
    return render_template('data.html', form=form)


@app.route('/search', methods=['POST'])
def submitForm():
    form = MyForm(request.form)
    if not form.validate():
        return render_template('data.html', form=form), 400

    # retrieve user inserted parameters
    email_ins = form.email.data
    type_ins = form.type.data
    value_ins = form.value.data
    plot_ins = form.plot.data

    # verify that user's email address sintax is correct
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email_ins):
        flash('Please, insert a valid email address.')
        return redirect('/search')

    # save searches data in the Datastore
    qry = Search.query(ndb.AND(Search.email == email_ins,
                               Search.value == value_ins)).get()
    if not qry:
        s = Search(email=email_ins, type=type_ins, value=value_ins, plot=plot_ins)
        s.put()
        logging.info('Correctly inserted new Search')
    else:
        qry.counter = qry.counter + 1
        qry.put()
        logging.info('Correctly updated Search')

    param = {}
    # if the field inserted type (type_ins) is 'IMDbID', the first and the second character of the field value_ins
    # must be letters, remaining characters must be numbers instead
    if type_ins == 'title':
        param = {
            't': value_ins,
            'plot': plot_ins,
            'apikey': API_KEY
        }
    elif type_ins == 'IMDbID':
        param = {
            'i': value_ins,
            'plot': plot_ins,
            'apikey': API_KEY
        }
        if value_ins[0].isalpha() and value_ins[1].isalpha() and value_ins[2:].isdigit():
            logging.info('The value inserted is correct.')
        else:
            flash('The value inserted is not correct.')
            logging.warning('Error. Value inserted {} is not correct'.format(value_ins))
            return redirect('/search')

    # use omdbapi site API
    url = 'http://www.omdbapi.com/'
    params = urllib.urlencode(param)
    myurl = '{}?{}'.format(url, params)
    logging.info('Myurl: {}'.format(myurl))
    req = urllib2.Request(myurl)
    url_resp = urllib2.urlopen(req)
    content = url_resp.read()
    risp = json.loads(content)
    title = risp['Title']

    # use IMG4Me API
    url2 = 'https://img4me.p.mashape.com/'
    param2 = {
        'bcolor': 'FFFFFF',
        'fcolor': '000000',
        'font': 'trebuchet',
        'size': 25,
        'text': title,
        'type': 'gif'
    }
    params2 = urllib.urlencode(param2)
    myurl2 = '{}?{}'.format(url2, params2)
    logging.info('Myurl: {}'.format(myurl2))
    req2 = urllib2.Request(myurl2)
    req2.add_header('X-Mashape-Key', MASHAPE_KEY)
    req2.add_header('Accept', 'text/plain')
    url_resp2 = urllib2.urlopen(req2)
    content2 = url_resp2.read()

    return render_template('response.html', risp=risp, tit=content2)
