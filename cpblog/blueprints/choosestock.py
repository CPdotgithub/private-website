import os
from flask import render_template, flash, redirect, url_for, current_app,request, abort, Blueprint,make_response

from flask_login import login_required, current_user
from cpblog.decorators import confirm_required, permission_required
from cpblog.extensions import db
from cpblog.models import Admin,Account,Order,LoanOrder, IndustryInfo,StockInfo,InstitutionInfo,InstitutionStockDaily,StockDaily
from cpblog.emails import send_new_order_email,send_week_report_email
blog_bp = Blueprint('stock', __name__)


@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['CPBLOG_STOCK_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('stock/index.html')