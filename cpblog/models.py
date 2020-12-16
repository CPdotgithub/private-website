from cpblog.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin


class Admin(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(254),unique=True,index=True)
    blog_title = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(100))
    name = db.Column(db.String(30))
    member_since = db.Column(db.DateTime,default=datetime.utcnow())
    about = db.Column(db.Text)
    confirmed = db.Column(db.Boolean,default=False)
    account = db.relationship("Account",back_populates='admin')
    videos = db.relationship("VideoHistory",back_populates='admin')
    def confirmed_user(self,flag):
        self.confirmed = flag 
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class VideoHistory(db.Model):
    __tablename__='videohistory'  
    id = db.Column(db.Integer,primary_key=True) 
    user_id = db.Column(db.Integer,db.ForeignKey('admin.id'))
    admin = db.relationship('Admin',back_populates='videos')
    videoname = db.Column(db.String(255),index=True)
    lasttime = db.Column(db.DateTime,default=datetime.now())
    url = db.Column(db.String(255))
  
    




class Account(db.Model,UserMixin):
    __tablename__='account'    
    id = db.Column(db.Integer,db.ForeignKey("admin.id"),primary_key=True)
 
    
    orders = db.relationship('Order',back_populates='account')
    balance = db.Column(db.Float)
    loanorders = db.relationship('LoanOrder',back_populates='account')
    isactive =  db.Column(db.Boolean,default=True)
    admin = db.relationship('Admin',back_populates='account')




class Order(db.Model):
    id = db.Column(db.Integer,primary_key=True) 
    account_id = db.Column(db.Integer,db.ForeignKey('account.id'))

    account = db.relationship('Account',back_populates='orders')
    type = db.Column(db.Boolean)
    date = db.Column(db.DateTime,default=datetime.now())    
    stock_id = db.Column(db.Integer,index=True)
    price = db.Column(db.Float)
    shares = db.Column(db.Integer) 
    commission = db.Column(db.Float)
    profit = db.Column(db.Float)   



    
class LoanOrder(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    account_id = db.Column(db.Integer,db.ForeignKey('account.id'))

    account = db.relationship('Account',back_populates='loanorders')
    value = db.Column(db.Float)
    starttime = db.Column(db.DateTime)
    endtime = db.Column(db.DateTime)
    isended = db.Column(db.Boolean,default=False)




    

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


class IndustryInfo(db.Model):
    #行业信息
    __tablename__='industryinfo'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer,primary_key=True) 
    name = db.Column(db.String(50),unique=True,index=True)
    stocks = db.relationship('StockInfo',back_populates='industryinfo')

class StockCategory(db.Model):
    __tablename__='stockcategory'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),unique=True,index=True)
    stocks = db.relationship('StockInfo',back_populates='stockcategory')

class StockInfo(db.Model): 
    __tablename__='stockinfo'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer,primary_key=True)
    a_code = db.Column(db.Integer,index=True )
    h_code = db.Column(db.Integer,index=True)
    name = db.Column(db.String(50),index=True)
    exchange_market = db.Column(db.String(10))
    industry_id = db.Column(db.Integer,db.ForeignKey('industryinfo.id'))
    stockcategory_id = db.Column(db.Integer,db.ForeignKey('stockcategory.id'))
    industryinfo = db.relationship("IndustryInfo",back_populates='stocks')
    url = db.Column(db.String(255),unique=True)
    stockcategory = db.relationship("StockCategory",back_populates='stocks')




class InstitutionInfo(db.Model): 
    #机构信息
    __tablename__='institutioninfo'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),index=True)
    url = db.Column(db.String(255))


class InstitutionStockDaily(db.Model):
    __tablename__='institutiondaily'
    __table_args__ = {'extend_existing': True}
    date = db.Column(db.DateTime,primary_key=True)
    h_stock_code = db.Column(db.Integer,index=True)
    stock_name = db.Column(db.String(50))
    a_stock_code = db.Column(db.Integer,primary_key=True)
    institution_id = db.Column(db.Integer,primary_key=True)
    institution_name = db.Column(db.String(255))
    #持股比例
    holdstockratio = db.Column(db.Float)
    stockvalue = db.Column(db.Float)
    #持股市值1，5，10日变化
    valuechange1 = db.Column(db.Float)
    valuechange5 = db.Column(db.Float)
    valuechange10 = db.Column(db.Float)




class StockDaily(db.Model):

# volume	成交数量	单位：股
# amount	成交金额	精度：小数点后4位；单位：人民币元
# adjustflag	复权状态	不复权、前复权、后复权
# turn	换手率	精度：小数点后6位；单位：%
# tradestatus	交易状态	1：正常交易 0：停牌
# pctChg	涨跌幅（百分比）	精度：小数点后6位
# peTTM	滚动市盈率	精度：小数点后6位
# psTTM	滚动市销率	精度：小数点后6位
# pcfNcfTTM	滚动市现率	精度：小数点后6位
# pbMRQ	市净率	精度：小数点后6位
# isST
    __tablename__ = 'stockdaily'
    
    date  = db.Column(db.DateTime,primary_key=True)
    code =  db.Column(db.String(50),primary_key=True)
    open =  db.Column(db.Float)
    high =  db.Column(db.Float)
    low =  db.Column(db.Float)
    close =  db.Column(db.Float)
    preclose =  db.Column(db.Float)
    volume =  db.Column(db.Float)
    amount =  db.Column(db.Float)
    turn =  db.Column(db.Float)
    tradestatus	= db.Column(db.Boolean,default=True)
    pctChg =  db.Column(db.Float)
    peTTM =  db.Column(db.Float)
    psTTM =  db.Column(db.Float)
    pcfNcfTTM =  db.Column(db.Float)
    pbMRQ =  db.Column(db.Float)
    isST = db.Column(db.Boolean,default=False)

    


