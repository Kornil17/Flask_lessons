from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_paginate import Pagination, get_page_args
from flask_security import login_required

from second_module.database import DataManager, Post
from .forms import PostForm


posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/')
def index():
    qstr = request.args.get('parametrs')
    page = request.args.get('page', type=int, default=1)
    per_page = 2  # количество записей на странице

    if qstr:
        posts = DataManager.get_all_posts(name=qstr)
    else:
        posts = DataManager.get_all_posts()

    total = len(posts)
    offset = (page - 1) * per_page
    pagination_posts = posts[offset: offset + per_page]
    print(total, offset, pagination_posts)

    pagination = Pagination(page=page, total=total, per_page=per_page,
                            record_name='posts', css_framework='bootstrap4')

    return render_template('posts/index.html', posts=pagination_posts, pagination=pagination,
                           methods_name=request.endpoint)
@posts.route('/<int:id_post>')
def get_post(id_post):
    if not isinstance(id_post, int):
        abort(404)
    post = DataManager.get_post_by_id(id_post)
    tag = DataManager.get_tag_by_id(id_post)
    return render_template('posts/post.html', post=post, title=post.title, tag=tag, methods_name='posts.index')

@posts.route('/create_post', methods=["GET", "POST"])
@login_required
def create_post():
    post_form = PostForm()
    if request.method == "POST":
        if post_form.validate_on_submit():
            post = DataManager.insert_data(Post, title=post_form.title.data, body=post_form.body.data)
            return redirect(url_for("posts.index"))
        else:
            print('error')
            print(post_form.errors)
    return render_template('posts/create_post.html', post_form=post_form)




