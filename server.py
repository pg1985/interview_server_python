from bottle import *
from datetime import datetime
import calendar
from pymongo import Connection
import bson
from json import dumps

client = Connection('localhost', port=27017)
db = client.todo

@post('/create/')
def create_post():
	new_post = {}
	post_data = request.forms
	new_post['title'] = post_data['title']
	new_post['desc'] = post_data['desc']
	new_post['is_deleted'] = 0
	new_post['created_date'] = calendar.timegm(datetime.utctimetuple(datetime.now()))
	new_post['updated_date'] = new_post['created_date']
	new_post['is_completed'] = 0

	db.items.insert(new_post)

	new_post['_id'] = str(new_post['_id'])

	return new_post


@post('/delete/')
def delete_post():
	post = request.forms
	post = db['items'].find_one({'_id':bson.ObjectId(post['_id'])})
	post['is_deleted'] = 1
	db.items.save(post)
	post['_id'] = str(post['_id'])
	return post


@post('/edit_post/')
def edit_post():
	post = request.json
	post['_id'] = bson.ObjectId(post['_id'])
	db.items.update({'_id': post['_id']},{'$set':post})
	post['_id'] = str(post['_id'])
	return post


@get('/get_post/:post_id')
def get_post(post_id):
	post = db['items'].find_one({'_id':bson.ObjectId(post_id)})
	post['_id'] = str(post['_id'])

	if post['is_deleted'] == 0:
		return post  
	else: 
		return {}


run (host='localhost', port=5150)

