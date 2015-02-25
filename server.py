from bottle import *
from datetime import datetime
import calendar
from pymongo import Connection
import bson

client = Connection('localhost', port=27017)
db = client.todo

@post('/create_user')
def create_user():
    new_user = {}
    user_post_data = request.forms.dict
    new_user['username'] = user_post_data['username']
    new_user['password'] = user_post_data['password']
    new_user['is_deleted'] = 0
    db.user.insert(new_user)
    new_user['_id'] = str(new_user['_id'])

    return new_user

@get('/get_user/:user_id')
def get_user():
    new_user = {}
    user_post_data = request.forms.dict
    new_user['username'] = user_post_data['username']
    new_user['password'] = user_post_data['password']


@post('/create/')
def create_post():
    new_post = {}
    post_data = request.forms.dict
    new_post['title'] = post_data['title']
    new_post['desc'] = post_data['desc']
    new_post['is_deleted'] = '0'
    new_post['created_date'] = calendar.timegm(datetime.utctimetuple(datetime.now()))
    new_post['updated_date'] = new_post['created_date']
    new_post['is_completed'] = '0'

    db.post.insert(new_post)

    new_post['_id'] = str(new_post['_id'])

    return new_post


@post('/delete/')
def delete_post():
    post_data = request.forms.dict
    post_to_delete = db['post'].find_one({'_id': bson.ObjectId(post_data['_id'])})
    post_to_delete['is_deleted'] = '1'
    db.post.save(post_to_delete)
    post_to_delete['_id'] = str(post_to_delete['_id'])

    return '{"deleted": "true"}'


@post('/edit_post/')
def edit_post():
    post = request.forms.dict
    post['_id'] = bson.ObjectId(post['_id'])
    db.post.update({'_id': post['_id']}, {'$set': post})
    post['_id'] = str(post['_id'])
    return post


@post('/set_completed/')
def set_completed(post_id):
    post_data = request.forms.dict
    completed_post = db['post'].find_one({'_id': bson.ObjectId(post_id)})
    completed_post['is_completed'] = post_data['is_completed']
    db.post.save(completed_post)
    completed_post['_id'] = str(completed_post['_id'])
    return completed_post


@get('/get_post/:post_id')
def get_post(post_id):
    found_post = db['post'].find_one({'_id': bson.ObjectId(post_id)})
    found_post['_id'] = str(found_post['_id'])

    if found_post['is_deleted'] == '0' or found_post['is_deleted'] == 0:
        return found_post
    else:
        return '{"error": "no post found with given ID"}'


run(host='0.0.0.0', port=4567)