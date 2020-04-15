from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

import json
from flaskr.auth import login_required
from flaskr.db import get_db

from flaskr.db import get_db, select_sql, insert_sql

bp = Blueprint('item', __name__)

def list_split(items, n):
    return [items[i:i+n] for i in range(0, len(items), n)]

@bp.route('/')
def index():
    posts = select_sql('SELECT * FROM `1982906`.item ORDER BY id DESC;')
    posts_list = list_split(posts, 3)
    return render_template('item/index.html', posts_list=posts_list)

@bp.route('/search', methods=('GET', 'POST'))
def search():
    info = request.values['info']
    posts = select_sql(f'SELECT * FROM `1982906`.item where name LIKE \'%{info}%\' ORDER BY id DESC;')
    posts_list = list_split(posts, 3)
    return render_template('item/index.html', posts_list=posts_list)

@bp.route('/pay', methods=('GET', 'POST'))
@login_required
def pay():
    if not request.json['cardinfo']['num']:
        return json.dumps({'result': False, 'msg': 'the card num is null.'})
    if not request.json['cardinfo']['password'] or not request.json['cardinfo']['checkpassword']:
        return json.dumps({'result': False, 'msg': 'the card password is null.'})

    if request.json['cardinfo']['password'] != request.json['cardinfo']['checkpassword']:
        return json.dumps({'result': False, 'msg': 'the card password is different from checkpassword.'})
    try:
        money = int(request.json['cardinfo']['price'])
    except:
        return json.dumps({'result': False, 'msg': 'pleace enter the price with type of num like 999999999'})
    userid = g.user[0]['id']
    orders = select_sql(f'SELECT * FROM `1982906`.order where user_id={userid} and status=1;')
    price = 0
    for (index, order) in enumerate(orders):
        item_id = order['item_id']
        info = select_sql(f'SELECT * FROM `1982906`.item where id={item_id};')[0]
        price += info['price']
    if money < price:
        return json.dumps({'result': False, 'msg': 'the price is not enough.'})
    insert_sql(f'UPDATE `1982906`.order SET status = 2 WHERE user_id = {userid};')
    return json.dumps({'result': True, 'msg': True})



@bp.route('/shopping', methods=('GET', 'POST'))
@login_required
def shopping():
    userid = g.user[0]['id']
    orders = select_sql(f'SELECT * FROM `1982906`.order where user_id={userid} and status=1;')
    price = 0
    for (index, order) in enumerate(orders):
        item_id = order['item_id']
        info = select_sql(f'SELECT * FROM `1982906`.item where id={item_id};')[0]
        orders[index]['iteminfo'] = info
        price += info['price']
    return render_template('item/shopping.html', posts_list=orders, totalprice=price)

@bp.route('/deleteorder', methods=('GET', 'POST'))
@login_required
def deleteshopping():
    if request.method == 'POST':
        order_id = request.json['item']['id']
        insert_sql(f'DELETE FROM `1982906`.order WHERE id = {order_id};')

    return redirect(url_for('item.shopping'))


@bp.route('/addshopping', methods=('GET', 'POST'))
@login_required
def addshopping():
    if request.method == 'POST':
        item_id = int(request.json['item']['id'])
        userid = g.user[0]['id']
        print(f'{item_id}---{userid}')
        insert_sql(f'INSERT INTO `1982906`.`order` (`item_id`,`user_id`,`status`,`idcard_name`,`idcard_password`) VALUES ({item_id}, {userid}, 1,1,1);')
    return json.dumps({'fffdf':31321})

@bp.route('/createcomment', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        import pdb
        # pdb.set_trace()
        item_id = int(request.json['item']['id'])
        comment = request.json['comment']
        error = None

        if not comment and not item_id:
            error = 'item_id or comment is required.'

        if error is not None:
            flash(error)
        else:
            name = g.user[0]['username']
            insert_sql(f'INSERT INTO `1982906`.`comment` (`value`,`item_id`,`name`) VALUES (\'{comment}\', {item_id}, \'{name}\');')
            return json.dumps({'name':name, 'value':comment})
            # return redirect(url_for('blog.index'))

    return render_template('item/create.html')

@bp.route('/getcomment', methods=('GET', 'POST'))
@login_required
def getcomment():
    if request.method == 'POST':
        item_id = int(request.json['item']['id'])
        error = None
        if not item_id:
            error = 'item_id or comment is required.'
        if error is not None:
            flash(error)
        else:
            infos = select_sql(f'SELECT name,value FROM `1982906`.comment where item_id={item_id};')
            return json.dumps(infos)
            # return redirect(url_for('blog.index'))

    return render_template('item/create.html')

def get_post(id, check_author=True):
    post = select_sql(f'SELECT p.id, title, body, created, author_id, username FROM post p JOIN user u ON p.author_id = u.id WHERE p.id = {id}')

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            insert_sql(f'UPDATE post SET title = {title}, body = {body} WHERE id = {id}')
            return redirect(url_for('item.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    insert_sql(f'DELETE FROM post WHERE id = {id}')
    return redirect(url_for('item.index'))