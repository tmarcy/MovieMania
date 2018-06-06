from myapp.flask_app import app, csrf
from flask import make_response, request, flash, redirect
from myapp.models.searches import Search
from google.appengine.ext import ndb
import json
import logging


@app.route('/api/v1.0/list', methods=['GET'])
def showList():
    """
    It shows a list of all searches of a specified type
    relative to a single user.
    User email and search type are GET request parameters.
    :return: response in json format
    """
    params = request.args
    required_param = ['searchType', 'email']
    for r in required_param:
        if r not in params.keys():
            flash('A parameter is missing.')
            return redirect('/')
    type = request.args.get('searchType')
    email = request.args.get('email')
    logging.info('Parameters: {}, {}'.format(type, email))

    qry = Search.query((ndb.AND(Search.email == email,
                                Search.type == type))).fetch()
    mydata = []
    for each in qry:
        datadic = {}
        datadic['value'] = each.value
        datadic['plot'] = each.plot
        datadic['counter'] = each.counter
        mydata.append(datadic)

    # set response
    json_response = {}
    json_response['user'] = email
    json_response['search type'] = type
    json_response['data'] = mydata
    json_response['status'] = 'OK'
    json_response['message'] = 'Successfully retourned the resource'
    risp = make_response(json.dumps(json_response, ensure_ascii=True), 200)
    risp.headers['content-type'] = 'application/json'
    return risp


@app.route('/api/v1.0/statistics', methods=['GET'])
def showStat():
    """
       It shows a statistics list about searches of
       a specified type.
       Search type is a GET request parameter.
       :return: response in json format
       """
    param = request.args
    required_param = 'searchType'
    if required_param not in param.keys():
        flash('A parameter is missing.')
        return redirect('/')
    type = request.args.get('searchType')
    logging.info('Parameter: {}'.format(type))

    qry = Search.query(Search.type == type).fetch()

    mydata = []
    for each in qry:
        user = each.email
        mydata.append(user)
    # remove duplicated list values
    mydata = list(set(mydata))

    # set response
    json_response = {}
    json_response['search type'] = type
    json_response['total requests'] = len(qry)
    json_response['data'] = mydata
    json_response['status'] = 'OK'
    json_response['message'] = 'Successfully returned the resource'
    risp = make_response(json.dumps(json_response, ensure_ascii=True), 200)
    risp.headers['content-type'] = 'application/json'
    return risp


@csrf.exempt
@app.route('/api/v1.0/list', methods=['POST'])
def insertNew():
    """
       It allows inserting a new search in the Datastore,
       without any parameters control.
       All Search model properties are POST requests parameter.
       :return: response in json format
       """
    email = request.args.get('email')
    type = request.args.get('type')
    value = request.args.get('value')
    plot = request.args.get('plot')

    # save searches data in the Datastore
    qry = Search.query(ndb.AND(Search.email == email,
                               Search.value == value)).get()
    if not qry:
        s = Search(email=email, type=type, value=value, plot=plot)
        s.put()
        logging.info('Correctly inserted new Search')
    else:
        qry.counter = qry.counter + 1
        qry.put()
        logging.info('Correctly updated Search')

    # set response
    json_response = {}
    json_response['status'] = 'OK'
    json_response['message'] = 'Successfully completed the request'
    risp = make_response(json.dumps(json_response, ensure_ascii=True), 200)
    risp.headers['content-type'] = 'application/json'
    return risp
