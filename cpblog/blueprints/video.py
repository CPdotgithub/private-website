from flask import render_template,Blueprint
# flash, redirect, url_for, current_app,request, abort, 


video_bp = Blueprint('videos',__name__)
@video_bp.route('/')
def index():
    return render_template('videos/video.html')