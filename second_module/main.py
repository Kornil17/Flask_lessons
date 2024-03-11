from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import view
from database import PostTag, session, Tag, Post, engine
from app import app
from sqlalchemy import Column, Integer

admin = Admin(app)
admin.add_view(ModelView(PostTag, session=session()))
admin.add_view(ModelView(Tag, session=session()))
admin.add_view(ModelView(Post, session=session()))


if __name__ == "__main__":
    app.run()