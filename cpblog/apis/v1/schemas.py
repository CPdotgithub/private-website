from flask import url_for




def order_schema(order):
    return  {
        'id' : order.id,
        'user_id' : order.user_id,
        'admin' : order.admin,
        'stock_id' :order.stock_id ,
        'value' : order.value,
        'ammount' : order.ammount,
        'starttime' : order.starttime,
        'endtime' : order.endtime,
        'isprofitable' : order.isprofitable, 
        'ishistory' : order.ishistory,
    }

def account_schema(account):
    return {
        'account_id' : account.account_id,
        'username' : account.username,
        'orders':account.orders,
        'balance':account.balance,
        'loans':account.loans,
        'isactive' :account.isactive
    }
             
    
    

class LoanOrder(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,ForeignKey='admin.id')
    value = db.Column(db.Integer)
    starttime = db.Column(db.DateTime)
    endtime = db.Column(db.DateTime)
    ishistory = db.Column(db.Boolean,default=False)
    # def new_value(self):
    #     days = (datetime.datetime.now().date()-self.starttime).days
    #     ratio = 0.00025
    #     new_value = self.value*(1+ratio)**days
    #     db.session.update(self.value)
    #     db.session.commit()
