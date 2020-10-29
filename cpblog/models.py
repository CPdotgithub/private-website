from cpblog.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin


class Admin(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(254),unique=True,index=True)
    blog_title = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(100))
    name = db.Column(db.String(30))
    member_since = db.Column(db.DateTime,default=datetime.utcnow())
    about = db.Column(db.Text)
    confirmed = db.Column(db.Boolean,default=False)
    def confirmed_user(self,flag):
        self.confirmed = flag
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

# class Order(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     stock_id = db.Column(db.Integer,db.ForeignKey('stock.id'))
#     buyer_id = db.Column(db.Integer,db.ForeignKey('admin.id'))
#     admin = db.relationship('admin',back_populates='orders')
#     exchange_date = db.Column(db.DateTime)
#     exchange_type = db.Column(db.Boolean)
#     exchange_amount = db.Column(db.Integer)

# class stock(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     full_id = db.Column(db.String(30),unique=True,index=True)






class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),unique=True)
    posts = db.relationship('Post',back_populates='category')
    def delete(self):
        default_category = Category.query.get(1)
        posts = self.posts[:]
        for post in posts:
            post.category = default_category
        db.session.delete(self)
        db.session.commit()

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)
    can_comment = db.Column(db.Boolean, default=True)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    category = db.relationship('Category',back_populates='posts')
    comments = db.relationship('Comment',back_populates='post',cascade='all,delete-orphan')


class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean,default=False)#是否为管理员 
    reviewed = db.Column(db.Boolean,default=False)#是否经过审核
    timestamp = db.Column(db.DateTime,default=datetime.utcnow,index=True)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    post = db.relationship('Post',back_populates='comments')
    replied_id = db.Column(db.Integer,db.ForeignKey('comment.id'))
    replied = db.relationship('Comment',back_populates='replies',remote_side=[id])
    replies = db.relationship('Comment',back_populates='replied',cascade='all,delete-orphan')




    


# class VedioCategory(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     name = db.Column(db.String(30),unique=True)
    


# class Vedio(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     title = db.Column(db.String(60))
#     body = db.Column(db.Text)
#     timrstamp = db.Column(db.DateTime,default=datetime.utcnow)






#financial data


